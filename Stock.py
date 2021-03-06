import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

#import pymongo
#from pymongo import MonoClient

class Stock(object):
    def __init__(self,ticker):
        """
        Create object with a ticker passed through
        """
        self.ticker =ticker

        self.current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.thirty_days_ago =(datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        self.ten_years_ago =(datetime.datetime.now() - datetime.timedelta(days=10*365)).strftime("%Y-%m-%d")

        #self.cluster =MongoClient("mongodb+srv://jbugdenAssetEvaluations:qLYejb2AHuTeWD5Z@asset-cluster.gg8sr.mongodb.net/?retryWrites=true&w=majority")
        
        #Creating yFinance Object
        self.yf_data =yf.Ticker((str(ticker)+".ax"))
    
    def get_summary(self):
        summary={}
        #Current Price    
        yf_summary_df =self.yf_data.history(period='id', start= self.thirty_days_ago, end= self.current_date)
        summary['Current Price']=yf_summary_df['Close'].iloc[-1]
        #Last Update Date
        yf_summary_df['Date']=yf_summary_df.index
        summary['Last Update'] =yf_summary_df['Date'].astype(str).iloc[-1]


        yf_summary_dict =self.yf_data.info
        #Name
        summary['Company Name'] =yf_summary_dict['longName']

        #Sector
        summary['Company Name'] =yf_summary_dict['sector']

        #Ticker
        summary['Ticker'] =self.ticker

        #Industry
        summary['Industry'] =yf_summary_dict['industry']

        #Market Cap
        summary['Market Cap'] =yf_summary_dict['marketCap']

        return summary
    
    def earliest_date(self):
        data=self.yf_data.history(period='id', start =self.ten_years_ago, end =self.current_date)

        return

    def close_data(self):

        close_data =self.yf_data.history(period='id', start =self.ten_years_ago, end =self.current_date)


        return (close_data.Close)
    
    def business_summary(self):
        summary =self.yf_data.info

        return summary['longBusinessSummary']

    def get_news(self):
        return self.yf_data.news

    
    # ******NEED TO DO
    def get_key_stats(self):
        key_stats={}
        info=self.yf_data.info

        #Profitability
        key_stats['Profit Margin']= info['profitMargins']
        key_stats['Operating Margin'] =info['operatingMargins']

        #Return on Assets/Equity
        key_stats['ROA-Yahoo'] =info['returnOnAssets']
        key_stats['ROE-Yahoo'] =info['returnOnEquity']

        key_stats['Trailing P/E'] = info['trailingPE']

        key_stats['Forward P/E'] = info['forwardPE']
        key_stats['Quarterly Revenue Growth']=info['revenueGrowth']
        key_stats['Dilute EPS'] =info['trailingEps']
        key_stats['Forward EPS'] = info['forwardEps']

        key_stats['Payout Ratio']= info['payoutRatio']

        key_stats['Trailing Annual Dividend Yield'] =info['trailingAnnualDividendYield']
        key_stats['Dividend Yield'] =info['dividendYield']
        #Total Debt
        #Shares Outstanding





        return key_stats
    
    def return_cashflow(self):
        return self.yf_data.cashflow
    

    def return_Balance_sheet(self):
        return self.yf_data.balance_sheet

    def get_beta(self, date):
        tickers =[(str(self.ticker)+".ax"), 'STW.AX']
        data =yf.download(tickers, date)['Adj Close']

        price_change =data.pct_change()
        df = price_change.drop(price_change.index[0])

        stock =np.array(df.iloc[:,0]).reshape((-1,1))
        market =np.array(df.iloc[:,1])

        model = LinearRegression().fit(stock, market)

        return model.coef_[0]

    

    def get_beta_list(self):
        ten_years_ago =(datetime.datetime.now() - datetime.timedelta(days=10*365)).strftime("%Y-%m-%d")
        five_years_ago =(datetime.datetime.now() - datetime.timedelta(days=5*365)).strftime("%Y-%m-%d")
        three_years_ago =(datetime.datetime.now() - datetime.timedelta(days=3*365)).strftime("%Y-%m-%d")
        one_years_ago =(datetime.datetime.now() - datetime.timedelta(days=1*365)).strftime("%Y-%m-%d")
        
        betas ={}
        
        try:
            betas['10 Year'] =self.get_beta(ten_years_ago)
            
        except:
            print("10 Year didnt work")
        try:
             betas['5 Year'] =self.get_beta(five_years_ago)
        except:
            print("5 Year didnt work")
        try:
            betas['3 Year'] =self.get_beta(three_years_ago)
        except:
            print("3 Year didnt work")
        try:
            betas['1 Year'] =self.get_beta(one_years_ago)
        except:
            print("1 Year didnt work")


        return (betas)




    

        
