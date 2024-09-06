import streamlit as st
import numpy as np
import pandas as pd
import fmpsdk
from function import fmp_function, plot_chart_function
from tabs.header_dashboard import header_chart
from columns_settings import color_mapping
import os

api_key = st.secrets["FMP_API_KEY"]
# api_key= "xxUbfrh3hsbcydCGtbYZxqpH1jaufUzB"

def fundamental_chart(  ticker = 'AAPL'):

  df_final, company_dt, revenue_product, Revenue_region = fmp_function.load_data(apikey=api_key, Ticker=ticker, period='quarter', limit=10)

  header_chart(df_final,company_dt=company_dt, tick=ticker)

  c1,c2,c3 = st.columns([1,1,1])
  chart_dict = {
    c1: [["Asset",color_mapping.asset_color_mapping],
          ["Revenue",color_mapping.revenue_color_mapping],
          ["Cash Flow",color_mapping.cashflow_color_mapping]],

    c2: [["Liabilities",color_mapping.liabilities_color_mapping],
         ["Income break down",color_mapping.income_breakdown_color_mapping],
         ["Capital Expenditure",color_mapping.capex_invest_color_mapping],
         
         ],
         

    c3: [
      ["Cash Flow",color_mapping.cashflow_color_mapping], 
         ["Cost Break down",color_mapping.cost_color_mapping],
         ["Income", color_mapping.income_color_mapping, ['netIncome_pct_change']]

         ],
  }

  
  for chart in chart_dict.keys():
    with chart:
      cols_chart = chart_dict[chart]

      for i in range(len(cols_chart)):
        col = list(cols_chart[i][1].keys())
        col_mapping = cols_chart[i][1]
        title_chart = cols_chart[i][0]
        line = cols_chart[i][2] if len(cols_chart[i]) > 2 else None
        st.plotly_chart(plot_chart_function.create_stacked_bar_chart(df_final, title=title_chart,bar_col=col,line_col=line, color_mapping=col_mapping ))

  numeric_cols = df_final.select_dtypes(include='number')
  pct_change_df = numeric_cols.pct_change()
  pct_change_df = pct_change_df.add_suffix('_pct_change')
  merge_dt = pd.merge(df_final, pct_change_df, how='left', left_index=True, right_index=True)
  st.write(merge_dt)

