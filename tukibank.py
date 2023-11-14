#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 15:19:48 2023

@author: Oluwabukola Akanbi
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#method_1 (how to read json file)
#json_file = open('loan_data_json.json')
#data = json.load(json_file)

#method_2 (how to read json file) 
with open ('loan_data_json.json') as json_file:
    data = json.load(json_file)
    #print(data)

#transform to dataframe
loandata = pd.DataFrame(data)

#finding unique values for the purpose column
loandata['purpose'].unique()

#describe the data
loandata.describe() 

#describe the data for a specific column
loandata['fico'].describe() 
loandata['int.rate'].describe() 
loandata['fico'].describe() 

#using EXP() to get the annual income
income = np.exp(loandata['log.annual.inc'])

#add to the main data
loandata['annualincome'] = income

#FICO SCORE
fico = 700
#FICO Range
#fico >= 300 and < 400: 'Very Poor'
#fico >= 400 and ficoscore < 600: 'Poor'
#fico >= 601 and ficoscore < 660: 'Fair'
#fico >= 660 and ficoscore < 780: 'Good'
#fico >=780: 'Excellent'

if fico >= 300 and fico < 400:
    ficocat = 'very Poor'
elif fico >=400 and fico < 600:
    ficocat = 'Poor'
elif fico >= 601 and fico < 660:
    ficocat = 'Fair'
elif fico >= 660 and fico < 700:
    ficocat = 'Good'
elif fico >= 700:
    ficocat = 'Excellent'
else:
    ficocat = 'Unknown'
print(ficocat)

#applying for loop to loan data


length = len(loandata)
ficocats = []

for x in range(0,length):
    category = loandata['fico'][x]
    
    try:
        if category >= 300 and category < 400:
            cat = 'very poor'
        elif category >= 400 and category < 600:
            cat = 'poor'
        elif category >= 601 and category < 660:
            cat = 'fair'
        elif category >= 660 and category < 700:
            cat = 'good'
        elif category >= 700:
            cat = 'excellent'
        else:
            cat = 'unknown'
    except:
            cat = 'unknown'

    ficocats.append(cat)

ficocat = pd.Series(ficocats)

#Add to loandata column

loandata['fico.category']=ficocat

#df.loc as conditional statements
# df.loc[df[columnname] condition, newcolumnname] = 'value if the condition is met'

#for interest rates, a new column is wanted. rate >0.12 'that is high' and if <=0.12 'that is low'
loandata.loc[loandata['int.rate'] > 0.12, 'int.rate.type'] = 'High'
loandata.loc[loandata['int.rate'] <= 0.12,'int.rate.type'] = 'Low'


#Plotting 

#grouping
#number of loans/rows by fico.category

fico_category_count = loandata.groupby(['fico.category']).size()
fico_category_count.plot.bar(color='green', width=0.1)
plt.show()

purpose_category_count = loandata.groupby(['purpose']).size()
purpose_category_count.plot.bar(color='green', width=0.3)
plt.show()

#scatter plots

ypoint = loandata['annualincome']
xpoint = loandata['dti']
plt.scatter(xpoint, ypoint, color = '#4caf50')
plt.show()


colors = loandata['annualincome']

plt.scatter(xpoint, ypoint, c=colors, cmap='viridis')  # 'viridis' is just an example colormap, you can choose others
plt.colorbar()  # Add a colorbar to show the mapping of values to colors
plt.xlabel('DTI')  # Label for x-axis
plt.ylabel('Annual Income')  # Label for y-axis
plt.title('Scatter Plot of Annual Income vs DTI')  # Title for the plot
plt.show()

#Writing to CSV
loandata.to_csv('loan_cleaned.csv', index = True)








