import streamlit as st
import numpy as np
import pandas as pd
import fmpsdk
from function import fmp_function


#api_key = st.secrets["FMP_API_KEY"]
api_key= "xxUbfrh3hsbcydCGtbYZxqpH1jaufUzB"

def fundamental_chart():

  df_final, company_dt, revenue_product, Revenue_region = fmp_function.load_data(apikey=api_key, Ticker='AAPL', period='quarter', limit=10)
  st.write(df_final)