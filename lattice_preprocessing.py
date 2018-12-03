# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 10:44:12 2016

@author: Rahul Ahuja
"""

import pandas as pd
import datetime
import numpy as np
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
import zipfile
import re


def datazip(Path, Filename):
    zf = zipfile.ZipFile(Path) # having First.csv zipped file.
    Dataframe = pd.read_csv(zf.open(Filename) , skiprows =1, index_col = False)
    #Dataframe = pd.read_csv('D:/LoanStats3d.csv', skiprows =1, index_col = False)
    Dataframe = Dataframe.dropna(axis = 1, how = 'all')
    #Dataframe[0:10]
    WorkingDataFrame = Dataframe[['term', 'loan_amnt', 'grade','loan_status',
                              'issue_d', 'annual_inc','home_ownership',
                              'delinq_2yrs']].dropna()

    return WorkingDataFrame

WorkingDataFrame = datazip('D:/LoanStats3d.csv.zip','LoanStats3d.csv')

# variable selections and then putting into the separate dataframe

#WorkingDataFrame[0:10]

def reVar(Column):
    empty = []
    for i in range(Column.shape[0]):
        empty.append(re.findall(r'\d+', Column[i]))
    return pd.DataFrame(empty)[0].astype('int')
    
Term = reVar(WorkingDataFrame['term'])

#type(Term) 
#Term = WorkingDataFrame['term']

# \D+ represents anything except for number and replaces with blank.


Issue = pd.to_datetime(pd.Series(WorkingDataFrame['issue_d']))
date = datetime.date.today()
Duration = (date - Issue).astype('object').astype(str)

Duration = reVar(Duration)/12


Time = pd.DataFrame(Duration/Term).rename(columns={0:'Time'}) #Time has been normalised as stated in the blogs

home = pd.get_dummies(WorkingDataFrame['home_ownership']) # one-hot-encoding

le.fit(np.array((WorkingDataFrame['grade']).unique()))

grade = pd.DataFrame(le.transform(np.array(WorkingDataFrame['grade']))).rename(columns={0:'Grade'})



#WorkingDataFrame['loan_status'].unique()

dict = {'Current':0,'Late (31-120 days)':1,'Fully Paid':0,
        'Late (16-30 days)':1,'In Grace Period':1,
        'Charged Off':1,'Default':1}

Status = pd.DataFrame(WorkingDataFrame['loan_status']).replace(dict).rename(columns={0:'loan_status'})

#Status.unique()

RemainVar = WorkingDataFrame[['loan_amnt','annual_inc','delinq_2yrs']]

Frame = [RemainVar, Status, grade, home, Time]

ProcessedData = pd.concat(Frame, axis =1)

ProcessedData.to_csv('D:/ProcessedData.csv', index = False, sep =',')