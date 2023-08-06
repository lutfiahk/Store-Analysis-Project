# Import Library 
import pandas as pd
import numpy as np
import plotly.express as py
# import random
import scipy.stats as stats
import streamlit as st
from statsmodels.stats.multicomp import pairwise_tukeyhsd



# Data import
customer = pd.read_csv('Dataset/customerbydate.csv', sep = ';')
transaction = pd.read_csv('Dataset/transactionbydate.csv', sep = ';')
maindata = pd.read_csv('Dataset/main_table.csv', sep = ',')
transaction2 = pd.read_csv('Dataset/Case Study - Transaction.csv', sep = ';')
# transaction2['Date'] = pd.to_datetime(transaction2['Date'])
transactionbydate = transaction2.groupby('Date').agg({'TransactionID': 'nunique','CustomerID':'nunique', 'TotalAmount':'sum', 'Qty':'sum'}).reset_index()
transactionbydate = transactionbydate.rename(columns = {'TransactionID':'Total_Transaction', 'CustomerID':'Total_Customer', 'Qty':'Total_Qty'})


# Build App
st.set_page_config(layout="wide")
st.image('Dataset\store.jpg', use_column_width=True)
col1, col2= st.columns([1, 5])
col1.write('')
col1.image('Dataset\image.png', width = 140)
col2.header('Kalbe Nutritionals Store Analysis')
col2.subheader('Final Project of Data Scientist VIX')
col2.text('by : Lutfia Husna Khoirunnisa (https://github.com/lutfiahk)')

st.subheader('Introduction')
st.markdown('''A company needs to perform data analysis which can then provide insight that is useful for making future decisions.
This project aims to analyze the business activities of **Kalbe Nutritionals Store**. 
This analysis is divided into three parts: store and product analysis, customer analysis, and trend prediction model.
The data that will be used in this project is sales activity data from 14 stores that sell products from Kalbe Nutritionals in **2022.**
''')

st.write('''
    **Goal** : Answer the following questions:
    * How was the sales performance of the company in 2022?
    * What are the characteristics of the company's customers?
    * What are the sales predictions and many customers in the future?
    * What business recommendations can be done?

    **Result**: Using exploratory data analysis and dashboard data, you can see how sales will be in 2022, 
         then by using machine learning we can predict how the customer group of the company will be, 
         and how to forecast sales in the next 30 days. Then, with the results obtained, good actionable recommendations 
         can be made for the company.
''')

st.write('****')
st.write("<h3 style='text-align: center; color: white;'>Store and Product Analysis</h3>", unsafe_allow_html=True)


st.write('In addition to the analysis presented in this article, you can access the data dashboard through this link: [link](https://public.tableau.com/views/KalbeDashboard/Dashboard2?:language=en-US&:display_count=n&:origin=viz_share_link)')


# Grouped Data by Store
store_group = maindata.groupby(['storeid', 'storename', 'latitude', 'longitude']).agg({'customerid':'nunique', 'totalamount':'sum'}).reset_index().rename(columns={'customerid':'Total Customer', 'totalamount':'Total Amount'}).sort_values('Total Amount', ascending = True)
x = []
for i in store_group['storename']:
    i = i.strip()
    x.append(i)
store_group['storename'] = x
lingga_indices = store_group[store_group['storename'] == 'Lingga'].index
for i in lingga_indices:
    store_group.loc[i, 'storename'] = f"Lingga {store_group.loc[i, 'storeid']}"
SH_indices = store_group[store_group['storename'] == 'Sinar Harapan'].index
for i in SH_indices:
    store_group.loc[i, 'storename'] = f"Sinar Harapan {store_group.loc[i, 'storeid']}"

st.markdown('''
    Products from Kalbe Nutritionals are sold in 14 stores across Indonesia and Malaysia. 
    Where most of these stores are on the islands of Java and Sumatra. It is known that the stores that have 
    the most customers are Lingga on the island of Sulawesi and Buana on Kalimantan.
''')

# Store Map
store_map = py.scatter_mapbox(store_group, lat="latitude", lon="longitude", color = "storename", size="Total Customer" ,hover_name="storename", zoom=9, height=300, color_discrete_sequence=py.colors.qualitative.G10)
store_map.update_layout(mapbox_style="open-street-map")
store_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(store_map)


# Store Trend
transaction2['Date'] = pd.to_datetime(transaction2['Date'])
transaction2['Month'] = pd.to_datetime(transaction2['Date']).dt.month
transaction2['Monthname'] = transaction2['Month'].replace({1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6: 'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'})
transactionbydate = transaction2.groupby(['Month','Monthname']).agg({'TransactionID': 'nunique','CustomerID':'nunique', 'TotalAmount':'sum', 'Qty':'sum'}).reset_index()
transactionbydate = transactionbydate.rename(columns = {'TransactionID':'Total_Transaction', 'CustomerID':'Total_Customer', 'Qty':'Total_Qty'})
transactionbydate['Total Amount (in 10000)'] = transactionbydate['TotalAmount'] / 100000

transaction_trend = py.line(transactionbydate, x='Monthname', y=['Total_Transaction', 'Total_Customer', 'Total Amount (in 10000)'], title='<b>Total Transaction Trend</b>', color = 'variable', markers = True,  width = 750, color_discrete_sequence=py.colors.qualitative.G10)

min_value1 = transactionbydate['Total_Transaction'].min()
max_value1 = transactionbydate['Total_Transaction'].max()

min_value2 = transactionbydate['Total_Customer'].min()
max_value2 = transactionbydate['Total_Customer'].max()

min_value3 = transactionbydate['Total Amount (in 10000)'].min()
max_value3 = transactionbydate['Total Amount (in 10000)'].max()

transaction_trend.update_layout(annotations=[
     dict(x=transactionbydate.loc[transactionbydate['Total_Transaction'] == min_value1, 'Monthname'].iloc[0],
         y=min_value1,
         xref="x", yref="y",
         text=f"Min: {min_value1}",
         ax=0, ay=20),
    dict(x=transactionbydate.loc[transactionbydate['Total_Transaction'] == max_value1, 'Monthname'].iloc[0],
         y=max_value1,
         xref="x", yref="y",
         text=f"Max: {max_value1}",
         ax=0, ay=-20),
    dict(x=transactionbydate.loc[transactionbydate['Total_Customer'] == min_value2, 'Monthname'].iloc[0],
         y=min_value2,
         xref="x", yref="y",
         text=f"Min: {min_value2}",
         ax=0, ay=20),
    dict(x=transactionbydate.loc[transactionbydate['Total_Customer'] == max_value2, 'Monthname'].iloc[0],
         y=max_value2,
         xref="x", yref="y",
         text=f"Max: {max_value2}",
         ax=0, ay=-20),
     dict(x=transactionbydate.loc[transactionbydate['Total Amount (in 10000)'] == min_value3, 'Monthname'].iloc[0],
         y=min_value3,
         xref="x", yref="y",
         text=f"Min: {min_value3}",
         ax=0, ay=20),
    dict(x=transactionbydate.loc[transactionbydate['Total Amount (in 10000)'] == max_value3, 'Monthname'].iloc[0],
         y=max_value3,
         xref="x", yref="y",
         text=f"Max: {max_value3}",
         ax=0, ay=-20)
])
transaction_trend.update_layout(legend=dict(orientation="h", yanchor="top", y=1.15, xanchor="center", x=0.5))
st.plotly_chart(transaction_trend, use_container_width = True)

st.markdown('''
    Based from the trend line, we know that both total customers and total transactions and the highest total amount are in 
            January and September, and the lowest is in October. In the new year, customers tend to shop for a lot of goods, 
            but sales tend to be stable, up and down every month.

    In the range from June to August, there is an interesting trend. In June, the number of customers increased compared to 
            the previous month, but the total transactions and the number that occurred decreased. In July, although there was 
            an increase in total transactions and numbers, the number of customers decreased compared to June. Although it looks 
            positive because there is an increase in transactions, this actually indicates a decrease in customer loyalty to our 
            products, especially because the previous month's sales were low. This was also proven by the decrease in transactions 
            in August.
    
''')

col111, col112, col113 = st.columns([2,2,0.1])

# Store Chart
store_chart = py.bar(store_group, x = 'Total Amount', y = 'storename', color = 'storename',text = store_group['Total Amount'], orientation = 'h',color_discrete_sequence=py.colors.qualitative.G10, height = 400, width = 550)
store_chart.update_layout(title="<b>Total Amount from each Stores</b>", title_font=dict(size=16), showlegend=False, )
store_chart.update_layout(yaxis={'categoryorder':'total ascending'})
col111.plotly_chart(store_chart)

# Product Chart
product_group = maindata.groupby('productname').agg(total_qty = ('qty', 'sum')).reset_index().rename(columns = {'total_qty':'Total Qty'})
x = []
for i in product_group['productname']:
    i = i.strip()
    x.append(i)
product_group['productname'] = x
product_chart = py.bar(product_group, x = 'Total Qty', y = 'productname', text = product_group['Total Qty'], orientation = 'h', height = 400, width = 550)
product_chart.update_layout(title="<b>Total Qty from each Products</b>", title_font=dict(size=16), showlegend=False, )
product_chart.update_layout(yaxis={'categoryorder':'total ascending'})
col112.plotly_chart(product_chart)

st.markdown('''
    The highest sales were at the Lingga store in the Ambon area, and Prestasi Utama in the Sumatra area. The most sold products are 
            Thai tea, Ginger Candy, and Choco bar. The top 3 most sold products are sweet food products.
''')

st.write('****')

# Customer Analysis
st.write("<h3 style='text-align: center; color: white;'>Customer Analysis</h3>", unsafe_allow_html=True)
pdf = pd.read_csv('pdf.csv').drop('Unnamed: 0', axis = 1)

st.markdown('''
    A company can achieve great success when it understands its customers' behavior and preferences, enabling it to provide enhanced 
            services and advantages to potential loyal customers. By analyzing customers' transaction histories, we can uncover 
            patterns in their shopping behavior.

    In this sub project, we will conduct a **customer segmentation** model with Kmeans clustering algorithm. We will use
            customer data such as **age, income, total transaction, and the time elapsed since their last purchase**.    
''')

col1, col2= st.columns([1.2,2.5])

col1.image('Dataset\output.png', width = 320)
col2.write('\n')
col2.markdown('''To determine the most suitable number of clusters or groups for segmenting the data, we'll carry out an elbow test 
            and silhouette test. These tests help pinpoint the optimal number of customer segments. From these tests, we find that 
            there are 4 distinct customer groups based on their characteristics. Subsequently, we employ a clustering model using 
            the Kmeans algorithm.''')

st.markdown("<h5 style='text-align: center; color: white;'>The average of each variable based on clusters</h5>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.5,3,0.5])
c2.table(pdf.drop('customerid', axis = 1).groupby('CLUSTER').agg('mean').round(2).reset_index())

st.markdown('**Based on the obtained cluster groups, there are 4 clients characteristics:**')
c1, c2, c3 = st.columns([1,0.1,1])
with c1.container():
   c1, c2 = st.columns([0.3,2])
   c1.image('Dataset\img1.png')
   c2.markdown('''
  *  Customers in the Cluster 0 tend to have high income and medium transaction activity. This group of customers also 
tends to be older compared to the other groups.
               \n\n\n
''')
   c1, c2 = st.columns([0.3,2])
   c1.image('Dataset\img2.png')
   c2.markdown('''
  *  Customers in the Cluster 1 tends to have low income with low transaction activity. This group of customers also 
tends to be younger compared to the other groups.
''')

with c3.container():
   c1, c2 = st.columns([0.3,2])
   c1.image('Dataset\img3.png')
   c2.markdown('''
  *  Customers in the Cluster 2 tend to have medium income and medium transaction activity. This group of customers also 
tends to have not made transactions for a long time or are inactive customers.
''')
   c1, c2 = st.columns([0.3,2])
   c1.image('Dataset\img4.png')
   c2.markdown('''
  * Customers in the Cluster 3 tend to have low income with high transaction activity. This group of customers also tends 
to be in the middle age and are active customers.
''')   

col11, col12 = st.columns([2,3])
cluster_group = pdf.groupby('CLUSTER').agg(count = ('customerid', 'nunique')).reset_index()
cluster_group['CLUSTER'] = cluster_group['CLUSTER'].astype(str)
cluster_chart = py.bar(cluster_group, x = 'CLUSTER', y = 'count', color = 'CLUSTER',text = cluster_group['count'], color_discrete_sequence=py.colors.qualitative.G10, width = 400, height = 450)
cluster_chart.update_layout(title="<b>Number of Customer each Cluster</b>", title_font=dict(size=16), showlegend=False, )
cluster_chart.update_layout(yaxis={'categoryorder':'total ascending'})
col11.plotly_chart(cluster_chart)
col12.write('\n')
col12.write('\n')
col12.write('\n')
col12.write('''
From the results of the obtained customer segmentation, it is known that the majority of customers belong to cluster 0 and 1. 
\n
\n
\n

To determine whether there is indeed a difference in the total amount spent by customers in each cluster, 
we will attempt to conduct a one-way ANOVA to investigate this.
''')
# ANOVA
total_amount = maindata.groupby('customerid').agg(total_amount = ('totalamount', 'sum'))
# total_amount_clust = pdf.merge(total_amount, on = 'customerid', how = 'left')
# cl0 = total_amount_clust[total_amount_clust['CLUSTER'] == 0]['total_amount']
# cl1 = total_amount_clust[total_amount_clust['CLUSTER'] == 1]['total_amount']
# cl2 = total_amount_clust[total_amount_clust['CLUSTER'] == 2]['total_amount']
# cl3 = total_amount_clust[total_amount_clust['CLUSTER'] == 3]['total_amount']

# samp0 = random.sample(list(cl0), 97)
# samp1 = random.sample(list(cl1), 97)
# samp2 = random.sample(list(cl2), 97)
# samp3 = random.sample(list(cl3), 97)
# result = stats.f_oneway(samp0, samp1, samp2, samp3)

# if result.pvalue < 0.05:
#     res = ("There is a statistically significant difference in total amount spent among the clusters.")
# else:
#     res = ("There is no statistically significant difference in total amount spent among the clusters.")

col12.write(f'''
    One-way ANOVA test to see if there is a difference in total amount spent by customers:
         \n
p-value: 0.05

* H0: There is no statistically significant difference in total amount spent among the clusters.
* H1: There is a statistically significant difference in total amount spent among the clusters.

So, based on the test we conducted, we obtained a p-value 1.036034774282926e-34  < 0.05, 
\n allowing us to reject H0, or conclude that **There is a statistically significant difference in total amount spent among the clusters**''')

st.markdown('''
Next, a **Tukey test** will be conducted to determine whether the total amount spent by customers is statistically different 
            between each other. The following are the results obtained from the Tukey test conducted:
''')
st.image('Dataset/tukey_totalamount.png', width = 400)

st.markdown('''

From the obtained Tukey test result, we can conclude that there is a statistically significant difference 
between the total amount spent by customers from each cluster, except for cluster 0 and cluster 2, 
which do not have a statistically significant difference between them. 
Therefore, it can be said that the total amount spent by customers in cluster 0 and 2 is the same. 
\n
However, after conducting separate Tukey tests to observe the differences in age and income between
cluster 0 and 2, they are statistically different.
            ''')


st.write('****')
# Trend Analysis
st.write("<h3 style='text-align: center; color: white;'>Trend Analysis</h3>", unsafe_allow_html=True)

st.markdown('''
Next, we will proceed with trend prediction by comparing ARIMA, ARIMA with hyperparameter tuning, and Prophet models.
We will predict the total quantity of products sold and the number of customers for the next 30 days.
''')


col11, col12 = st.columns(2)

with col11.expander("Transaction Trend"):
    transaction_trend = py.line(transaction, x = 'date', y = 'sum', width = 500)
    transaction_trend.update_layout(title = "Transaction Trend (2022)")
    st.plotly_chart(transaction_trend)
with col12.expander("Customer Trend"):
    customer_trend = py.line(customer, x = 'date', y = 'count', width = 500)
    customer_trend.update_layout(title = "Customer Trend (2022)")
    st.plotly_chart(customer_trend)

