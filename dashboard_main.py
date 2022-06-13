from matplotlib import container
from sklearn.tree import plot_tree
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import datetime
import Stock
import numpy as np
import pymongo
from pymongo import MongoClient
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt



#Getting list of tickers
#in future will be webscrapped
asx_list = pd.read_csv('asx_list.csv')
asx_list['Index_Code']= asx_list['ASX code']
asx_list.set_index('Index_Code', inplace=True)
asx_dict=asx_list.to_dict('index')

#Config dashboard
st.set_page_config(layout="wide")


#Config Mongo Client
mongo_string ="mongodb+srv://"+ st.secrets.mongo.username +":"+st.secrets.mongo.password+"@asset-cluster.gg8sr.mongodb.net/?retryWrites=true&w=majority"
cluster = MongoClient(mongo_string)
db =cluster['AssetEvaluations']
collection_notes =db['Notes']


#Current Date
current_date = datetime.datetime.now().strftime("%Y-%m-%d")



with st.sidebar:
    st.title("Stock Evaluation Dashboard")
    ticker_select =st.selectbox('ASX Ticker',list(asx_dict.keys()))
    chosen_stock=Stock.Stock(ticker_select)


results =collection_notes.find({"Ticker": ticker_select})
Notes_list=[]
for note in results:
    note_dic ={}
    note_dic['Date'] =note["Date"]
    note_dic['Note'] =note["Note"]
    Notes_list.append(note_dic)


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

secndc1,secndc2 =first_container.columns((1,1))

with secndc1.container():
    with st.expander('Business Summary'):
        st.subheader('Business Summary')
        st.write(chosen_stock.business_summary())
    
    with st.expander('Recent News'):
        news=chosen_stock.get_news()
        for n in news:
            temp=dict(n)
            st.write(temp['publisher'])
            st.write(temp['title'])
            link_a =str(temp['link'])
            
            st.write("[Article Link](%s)"% (link_a))
    
    st.subheader("Beta Values")
    
    data = chosen_stock.get_beta_list()
    if len(data) >0:
        beta_chart =pd.DataFrame(data, index=[0])
        st.dataframe(beta_chart)
        
    else:
        st.write("Unable to get beta data- not enough close data")
    
    st.subheader("Comparison vs Market")
    market = Stock.Stock('STW')
    stock_data =chosen_stock.close_data().to_frame()
    stock_data.reset_index(inplace=True)
    market_data =market.close_data().to_frame()
    market_data.reset_index(inplace=True)

    market_data['Ticker']="Market"
    stock_data['Ticker']=ticker_select

    market_data['Change'] =market_data['Close'].pct_change().cumsum()
    stock_data['Change'] =stock_data['Close'].pct_change().cumsum()

    market_data['Date'] =market_data['Date'].astype(str)
    stock_data['Date'] =stock_data['Date'].astype(str)

    market_data['Date'] =market_data['Date'].astype(str)
    stock_data['Date'] =stock_data['Date'].astype(str)
    
    combined = market_data.merge(stock_data, on ='Date', how ='left')

    combined.set_index('Date')
    combined.dropna()
    combined.renamed(columns={'Change_x':'Market','Change_y':ticker_select}, inplace = True)
    
    fin_combined =combined[['Market',ticker_select]]



    st.write(fin_combined)



with secndc2.container():
    st.subheader('Notes')

    if len(Notes_list)<1:
        st.write("No notes currently on stock")
    
    else:
        idx=0
        for stock_note in Notes_list:
            st.write(stock_note['Date'],": ", stock_note['Note'])
            delete_button =st.button("Delete Note",key = idx)
            if delete_button:
                collection_notes.delete_one({"Date": stock_note['Date'], "Note": stock_note['Note']})
                
            idx= idx+ 1
    
    note = st.text_area('Add a note..', '''
     ''')
    
    add_button =st.button("Add Note")
    if add_button:
        post={"Ticker": ticker_select,"Note": note, "Date": current_date}
        collection_notes.insert_one(post)


        


    
    


  




