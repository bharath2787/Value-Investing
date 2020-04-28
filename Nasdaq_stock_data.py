#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:10:36 2020

@author: bharathmadhavaram
"""


""" FinViz Workput  """

#import finviz
#print(dir(finviz))
# Pull Verizon data 

#verizon = finviz.get_stock('VZ') #Dictionary of current stock values 
#dat = finviz.Screener(tickers="VZ", filters = ["Price", "Dividend Yield"])

""" Fetch Baance Sheet Data  """

import requests 
import json
import pandas as pd 
import numpy as np


stock_list = pd.read_csv('nasdaq_listed.csv', sep=',') 
 
stocks = stock_list.set_index("Symbol")    
  
Debt_to_Equity=[]    #blank lists
Assets = []
Cash_eq = []
Goodwill_intagible = []

for ticker in stocks.index[2594:]:

   # URL = https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/VZ?period=quarter'

   # ticker = 'VNOM'

    bs = requests.get('https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/'+ticker+'?period=quarter')
    bs = bs.json()    

    if bs == {}:    
        DoE = 0
        TA = 0
        Cash = 0
        Goodwill = 0
        
    else:     
        bs = bs['financials']    
        dat = pd.DataFrame.from_dict(bs)    
        dat = dat.T    
        dat.columns = dat.iloc[0]
        dat = dat[dat.columns.max()]     # most recent quarter 
        
        dat = dat.replace('',0,regex=True)
        
        if dat.loc['Total shareholders equity'] == '' :
            DoE = 0 
        elif float(dat.loc['Total shareholders equity']) == 0:
            DoE = 0
        else:    
            DoE = float(dat.loc['Total debt'])/float(dat.loc['Total shareholders equity'])
            TA = float(dat.loc['Total assets'])
            Cash = float(dat.loc['Cash and cash equivalents'])
            Goodwill = float(dat.loc['Goodwill and Intangible Assets'])

    Assets.append(TA)
    Cash_eq.append(Cash)
    Goodwill_intagible.append(Goodwill)
    Debt_to_Equity.append(DoE)  


stocks["Debt_to_Equity"] = Debt_to_Equity
stocks["Total Assets"] = Assets
stocks["Cash"] = Cash_eq
stocks["Goodwill & Intangible"] = Goodwill_intagible

stocks.to_csv("Nasdaq_data_pull_1.csv")


Net_Income = []

for ticker in stocks.index:
         
    IS = requests.get('https://financialmodelingprep.com/api/v3/financials/income-statement/'+ticker+'?period=annual')
    IS = IS.json()
        
    if IS == {}:
        NI = 0
  
    else: 
        IS = IS['financials']
        IS = pd.DataFrame.from_dict(IS)
        IS = IS.T            
        IS.columns = IS.iloc[0]
        IS = IS[IS.columns.max()]
    
        if IS.loc['Net Income'] == '':
            NI = 0
        else:    
            NI = float(IS.loc['Net Income'])
    
    #print("Debt to Equity Ratio for "+ticker+" is = "+str(round(Debt_to_Equity,2)))
              
    Net_Income.append(NI)



stocks["Net Income"] = Net_Income

stocks.to_csv("Nasdaq_data_pull.csv")

#Net Income / (Assets - Cash&Cash Equivalents - Goodwill - Intangible Assets)

stocks['Return_on_TangibleAssets'] = stocks['Net Income']/(stocks['Total Assets']-stocks['Cash']-stocks['Goodwill & Intangible'])


#Filter ROTA > 0.2 

value_stocks = stocks[stocks['Return_on_TangibleAssets']>=0.2]

stocks.to_csv("Nasdaq_stocks_data.csv")

value_stocks.iloc[:,0:1]


#https://financialmodelingprep.com/api/v3/financials/income-statement/VZ?period=annual'

