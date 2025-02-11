import streamlit as st
import pandas as pd
import plotly.express as px

# Load your data
df_cleaned = pd.read_csv('df_cleaned.csv', index_col='date', parse_dates=True)

# Convert 'month_year' to datetime if needed
df_cleaned['month_year'] = pd.to_datetime(df_cleaned['month_year'])

# Sidebar for filters
st.sidebar.title('Filters')

# Time Frame Filter
time_frame = st.sidebar.selectbox(
    'Select Time Frame',
    ('All', 'Last 3 Months', 'Last 6 Months', 'Last Year')
)

# Filter Dataframe by Time Frame
if time_frame == 'Last 3 Months':
    df_filtered = df_cleaned[df_cleaned.index >= df_cleaned.index.max() - pd.DateOffset(months=3)]
elif time_frame == 'Last 6 Months':
    df_filtered = df_cleaned[df_cleaned.index >= df_cleaned.index.max() - pd.DateOffset(months=6)]
elif time_frame == 'Last Year':
    df_filtered = df_cleaned[df_cleaned.index >= df_cleaned.index.max() - pd.DateOffset(years=1)]
else:
    df_filtered = df_cleaned

# Category Filter
categories = df_filtered['anonymized_category'].unique()
selected_category = st.sidebar.selectbox('Select Category', ['All'] + list(categories))

# Filter Dataframe by Category
if selected_category != 'All':
    df_filtered = df_filtered[df_filtered['anonymized_category'] == selected_category]

# Total Quantity and Value by Anonymized Category
st.title('Sales Dashboard')

st.header('1. Total Quantity and Value by Anonymized Category')
category_summary = df_filtered.groupby('anonymized_category').agg({
    'quantity': 'sum',
    'total_value': 'sum'
}).reset_index()

fig1 = px.bar(category_summary, x='anonymized_category', y=['quantity', 'total_value'], 
              barmode='group', title='Total Quantity and Value by Category')
st.plotly_chart(fig1)

# Top-performing Products and Businesses
st.header('2. Top-performing Products and Businesses')

# Top Products by Total Value
top_products = df_filtered.groupby('anonymized_product')['total_value'].sum().nlargest(10).reset_index()
fig2 = px.bar(top_products, x='anonymized_product', y='total_value', 
              title='Top 10 Performing Products by Total Value')
st.plotly_chart(fig2)

# Top Businesses by Total Value
top_businesses = df_filtered.groupby('anonymized_business')['total_value'].sum().nlargest(10).reset_index()
fig3 = px.bar(top_businesses, x='anonymized_business', y='total_value', 
              title='Top 10 Performing Businesses by Total Value')
st.plotly_chart(fig3)

# Time-series Chart of Sales Trends
st.header('3. Sales Trends Over Time')
sales_trend = df_filtered.groupby('month_year').agg({
    'quantity': 'sum',
    'total_value': 'sum'
}).reset_index()

fig4 = px.line(sales_trend, x='month_year', y=['quantity', 'total_value'], 
               title='Sales Trends Over Time')
st.plotly_chart(fig4)

# Customer Segmentation Summary
st.header('4. Customer Segmentation Summary')

# Segmentation by business total value
business_segmentation = df_filtered.groupby('anonymized_business')['total_value'].sum()
business_segmentation = pd.qcut(business_segmentation, q=3, labels=['Low Value', 'Medium Value', 'High Value']).to_frame('Segment').reset_index()

# Count of businesses per segment
segment_summary = business_segmentation['Segment'].value_counts().reset_index()
segment_summary.columns = ['Segment', 'Count']

fig5 = px.pie(segment_summary, values='Count', names='Segment', title='Customer Segmentation by Business Value')
st.plotly_chart(fig5)