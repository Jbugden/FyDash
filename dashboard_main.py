from matplotlib import container
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import datetime
import Stock
import numpy as np
import pymongo


#Getting list of tickers
#in future will be webscrapped




asx_list = pd.read_csv('asx_list.csv')
asx_list['Index_Code']= asx_list['ASX code']
asx_list.set_index('Index_Code', inplace=True)
asx_dict=asx_list.to_dict('index')

#Config dashboard
st.set_page_config(layout="wide")





with st.sidebar:
    st.title("Stock Evaluation Dashboard")
    ticker_select =st.selectbox('ASX Ticker',list(asx_dict.keys()))
    chosen_stock=Stock.Stock(ticker_select)
    st.subheader('Recent News')
    news=chosen_stock.get_news()
    for n in news:
        temp=dict(n)
        st.write(temp['publisher'])
        st.write(temp['title'])
        link_a =str(temp['link'])
        
        st.write("[Article Link](%s)"% (link_a))




#Title
with st.container():
    st.title(asx_dict[ticker_select]['Company name'])
    

first_container =st.container()

#Top Container
fc1,fc2 =first_container.columns((1,1))

with fc1:
    
    summary_info =chosen_stock.get_summary()

    #Current Price
    st.write('Ticker:   ', summary_info['Ticker'])
    st.write('Current Price:    ', '${:,.2f}'.format(np.round(summary_info['Current Price'],2)))
    st.write('Last Updated Date:    ', summary_info['Last Update'])
    st.write('Sector:   ', summary_info['Company Name'])
    st.write('Industry:   ',summary_info['Industry'])
    st.write('Market Cap:   ','${:,.2f}'.format(np.round(summary_info['Market Cap'],2)))

with fc2:
    st.line_chart(chosen_stock.close_data())

with st.container():
    st.subheader('Business Summary')
    st.write(chosen_stock.business_summary())



with st.container():
    st.subheader('Notes')
    mongo_string ="mongodb+srv://"+ st.secrets.mongo.username +":"+st.secrets.mongo.password+"@asset-cluster.gg8sr.mongodb.net/?retryWrites=true&w=majority"
    st.write(mongo_string)


  




