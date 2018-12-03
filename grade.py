# -*- coding: utf-8 -*-
"""
Created on Sun Feb 07 23:17:58 2016

@author: Rahul Ahuja
"""

#it could have also impemented by using dictionary
def grading(prompt):
       while True:
           value = raw_input(prompt)
           if value == 'A':
               value = 0
               break
           if value == 'B':
               value = 1
               break
           if value == 'C':
               value = 2
               break
           if value == 'D':
               value = 3
               break
           if value == 'E':
               value = 4
               break
           if value == 'F':
               value = 5
               break
           if value == 'F':
               value = 6
               break
           print value
       return value 