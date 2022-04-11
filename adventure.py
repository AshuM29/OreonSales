# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 18:43:30 2022

@author: Ashu Maheshwari
"""



import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import openpyxl


st.set_page_config(page_title="Oreon Sales Dashboard", page_icon=":bar_chart:", layout="wide")


stp=r"‪‪D:\New folder\Adventure Works 2005.xlsx" 
sales = pd.read_excel(stp.strip("‪u202a"),sheet_name='Sales')

#sales.head(10)

calendar = pd.read_excel(stp.strip("‪u202a"),sheet_name='Calendar')
customer = pd.read_excel(stp.strip("‪u202a"),sheet_name='Customers')
product = pd.read_excel(stp.strip("‪u202a"),sheet_name='Products')
teritory = pd.read_excel(stp.strip("‪u202a"),sheet_name='Territory')
prod_cat = pd.read_excel(stp.strip("‪u202a"),sheet_name='dimProductCategory')
prod_sub_cat = pd.read_excel(stp.strip("‪u202a"),sheet_name='dimProductSubCategory')

#sales['OrderDay']=""
#sales.set_index("OrderDate",inplace=True)
#sales['OrderDay']=sales.index.map(calendar['DayName'])

#sales['SubCategory']=""
#sales['Category']=""
#sales.set_index("ProductKey",inplace=True)
#sales['SubCategory']=sales.index.map(product['SubCategory'])
#sales['Category']=sales.index.map(product['Category'])

new_data=sales.merge(product,on="ProductKey",how='left')
calendar.rename(columns = {'Date':'OrderDate'}, inplace = True)

new_data=new_data.merge(calendar,on="OrderDate",how='left')

teritory.rename(columns = {'Territory Key':'SalesTerritoryKey'}, inplace = True)
new_data=new_data.merge(teritory,on="SalesTerritoryKey",how='left')

new_data=new_data.merge(customer,on="CustomerKey",how='left')

#new_data.columns

#for col in new_data.columns:
#    print(col)

#new_data.to_excel(r'D:\New folder\Adventure Compile.xlsx', index=False, header=True)

#https://www.webfx.com/tools/emoji-cheat-sheet/

st.header(":department_store: Oreon Sales Trend",anchor=None)

st.sidebar.header("Filter By Year")

fiscal_year=st.sidebar.multiselect(
    "Select The Year:",
    options=new_data["FiscalYear"].unique(),
    default=new_data["FiscalYear"].unique()
    )

#st.sidebar.header("Filter By Group")
group=st.sidebar.multiselect(
    "Select The Group:",
    options=new_data["Group"].unique(),
    default=new_data["Group"].unique()
    )

new_data_selection = new_data.query(
    "FiscalYear ==@fiscal_year and Group ==@group"
    )

total_sales=int(new_data_selection["SalesAmount"].sum())
order_quantity=int(new_data_selection["OrderQuantity"].sum())
total_profit=int((new_data_selection["SalesAmount"] - new_data["TotalProductCost"]).sum())
 
left_column, middle_column, right_column=st.columns(3)

with left_column:
    st.subheader("Total Sales,")
    st.subheader(f"US $ {total_sales:,}")

with middle_column:
    st.subheader("Order Quantity")
    st.subheader(f"{order_quantity}")
    
with right_column:
    st.subheader("Total Profit")
    st.subheader(f"US $ {total_profit:,}")

st.markdown("""---""")

sales_country=new_data_selection.groupby(by=["Country"]).sum()[["SalesAmount"]].sort_values(by="SalesAmount")


sales_category=new_data_selection.groupby(by=["Category"]).sum()[["SalesAmount"]].sort_values(by="SalesAmount")



sales_by_country=alt.Chart(new_data_selection).mark_bar().encode(
    x='Country:O', 
    y='sum(SalesAmount)',
    color='Country',
    tooltip=['sales_country:Q']
    ).properties(width=400,height=200)

sales_by_category=alt.Chart(new_data_selection).mark_bar().encode(
    x='Category:O', 
    y='sum(SalesAmount)',
    color='Category',
    tooltip=['sales_category:Q']
    ).properties(width=400,height=200)
    

#left_column, right_column=st.columns(2)
#left_column.altair_chart(sales_by_country, use_container_width=True)
#right_column.altair_chart(sales_by_category, use_container_width=True)

concat=alt.hconcat(sales_by_category,sales_by_country).configure_axis(
grid=False).resolve_scale(color='independent')
st.altair_chart(concat)

sales_by_gender=alt.Chart(new_data_selection).mark_bar().encode(
    x='Gender:O', 
    y='sum(SalesAmount)',
    color='Gender',
    tooltip=['sales_country:Q']
    ).properties(width=400,height=200)

sales_by_month=alt.Chart(new_data_selection).mark_bar().encode(
    x='MonthName:O', 
    y='sum(SalesAmount)',
    color='MonthName',
    tooltip=['sales_country:Q']
    ).properties(width=400,height=200)

concat1=alt.hconcat(sales_by_gender,sales_by_month).configure_axis(
grid=False).resolve_scale(color='independent')
st.altair_chart(concat1)

#concat2=alt.vconcat(concat,concat1).configure_axis(
#grid=False)
#st.altair_chart(concat2)

