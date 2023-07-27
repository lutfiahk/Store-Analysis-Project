# Import Library 
import pandas as pd
import plotly.express as py

# Data import
customer = pd.read_csv('Dataset/customerbydate.csv', sep = ';')
transaction = pd.read_csv('Dataset/transactionbydate.csv', sep = ';')

# Build App
import streamlit as st
st.set_page_config(layout="wide")
st.image('Dataset\store.jpg', use_column_width=True)
col1, col2= st.columns([1, 5])
col1.write('')
col1.image('Dataset\image.png', width = 140)
col2.header('Kalbe Nutritionals Store Analysis')
col2.subheader('Final Project of Data Scientist VIX')
col2.text('by : Lutfia Husna Khoirunnisa (https://github.com/lutfiahk)')

st.subheader('Introduction')
st.markdown('text')

col11, col12 = st.columns(2)

with col11.expander("Transaction Trend"):
    transaction_trend = py.line(transaction, x = 'date', y = 'sum', width = 500)
    transaction_trend.update_layout(title = "Transaction Trend (2022)")
    st.plotly_chart(transaction_trend)
with col12.expander("Customer Trend"):
    customer_trend = py.line(customer, x = 'date', y = 'count', width = 500)
    customer_trend.update_layout(title = "Customer Trend (2022)")
    st.plotly_chart(customer_trend)
