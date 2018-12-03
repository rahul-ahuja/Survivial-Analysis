# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 20:47:27 2016

@author: Rahul Ahuja
"""
from lifelines import CoxPHFitter
cf = CoxPHFitter()
import pandas as pd
import numpy as np
import grade



ProcessedData = pd.read_csv('C:/Users/abmm832/Downloads/ProcessedData.csv', index_col = False)

cf.fit(ProcessedData, 'Time', event_col = 'loan_status')

cf.print_summary()

#should have made the module of this function as well. Anyways I ve done it for loan grade module. 
def get_non_negative_int(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Invalid entry")
            continue

        if value < 0:
            print("Invalid entry")
            continue
        else:
            break
    return value
    
def home(prompt):
    dict2 = {}
    while True:
        value = input(prompt)
        if value == 'ANY':
            dict2 = {'ANY':1,'OWN':0,'RENT':0,'MORTGAGE':0}
            break
        if value == 'Own':
            dict2 = {'ANY':0,'OWN':1,'RENT':0,'MORTGAGE':0}
            break
        if value == 'Mortgage':
            dict2 = {'ANY':0,'OWN':0,'RENT':0,'MORTGAGE':1}
            break
        if value == 'Rent':
            dict2 = {'ANY':0,'OWN':0,'RENT':1,'MORTGAGE':0}
            break
    return dict2


inc = get_non_negative_int("Loanholder's annual income? ")
loan = get_non_negative_int("What is the loan amount?" )
delinq_2yrs = get_non_negative_int("What are the delinq years?" )
loan_grade = grade.grading("what is the loan grade? Choose from the following Grade 'A','B','C','D','E','F','G'" )
#loan_grade = grading("what is the loan grade? Choose from the following Grade 'A','B','C','D','E','F','G'" )
ownership = home("Loanholder's house ownership. Is it 'Mortgage', 'Own', 'Rent' or 'Any'?" )


d = {'annual_inc':inc, 'loan_amnt':loan, 'delinq_2yrs':delinq_2yrs, 'Grade':loan_grade}

d.update(ownership)


Test = pd.DataFrame([d])

survivalProb = pd.DataFrame(np.array(cf.predict_survival_function(Test)))
time = pd.DataFrame(cf.predict_survival_function(Test).index.values).rename(columns={0:'Time'})
hazard = 1 - pd.DataFrame(cf.predict_survival_function(Test))

payment_term = get_non_negative_int('What is the payment term? ')
payments = get_non_negative_int('What are the series of loan payments? ')

ExpTerms = pd.DataFrame(time * survivalProb * payment_term).astype(int) 

def npv(rate, cashflows):
    total = 0.0
    for i, cashflow in enumerate(cashflows):
        total += cashflow / (1 + rate)**i
    return total

def irr(cashflows, iterations=100):  #secant method
    rate = 1.0
    investment = cashflows[0]
    for i in range(1, iterations+1):
        rate *= (1 - npv(rate, cashflows) / investment)
    return rate
    
#ExpTerms.iat[0,0]
ExpRet = []
for i in range(ExpTerms.shape[0]):
    ExpReturn = float((1+irr([-loan] + [payments]*ExpTerms.iat[i,0]))**11) #takes out the scalar value, following the formula given in the blogs
    ExpRet.append(ExpReturn)  # I am not sure abt the formula of monthly return given in the article.
    
ExpectedReturnRate = pd.DataFrame(ExpRet).rename(columns={0:'Expected Rate of Return'})

Frame2 = [time,ExpectedReturnRate]

Return_of_the_loan = pd.concat(Frame2, axis=1)

print(Return_of_the_loan)
    
    

