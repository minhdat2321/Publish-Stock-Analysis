import streamlit as st
import numpy as np
import pandas as pd
import fmpsdk
from function import fmp_function, plot_chart_function
from tabs.header_dashboard import header_chart
from columns_settings import columns_settings
import os
import config
from data_handling import data_manipulation

api_key = st.secrets["FMP_API_KEY"]



def fundamental_chart(  ticker = 'AAPL'):
  # Header
  df_header, company_dt = fmp_function.header_data(apikey=api_key, Ticker=ticker)
  header_chart(df_header,company_dt=company_dt, tick=ticker)




  fin_chart_tab, fin_num_tab, analyst_tab_main, insider_tab = st.tabs(['Chart','Financial statement','Research report','Insider'])

  with fin_chart_tab:
      box1, box2, box3, box4, box5,box6 = st.columns([0.1,0.1,0.1,0.1,0.1,0.6])
      with box1:
          period_option = st.selectbox("Period Report",[ "Quarter","Annual"])
          period_option = period_option.lower()

      with box2:
          number_period = st.selectbox("Number Period", [20,30,50,100],index=1)

      with box3:
          type_dt = st.selectbox("Data type", ['Normal', "TTM"])

      with box4:
          adjust_bs = st.selectbox("Correct data", ['Reported', 'Adjusted'])

      with box5:
          roe_type = st.selectbox("ROE Type", ["Cash", "Non Cash"])



  # Chart data
  df_final  = fmp_function.load_data(apikey=api_key, Ticker=ticker, period=period_option, limit=number_period)
  df_final = data_manipulation.calc_data(df_final, type_dt=type_dt, roe_type=roe_type, adjust_bs=adjust_bs, period_option=period_option)

  c1,c2,c3 = st.columns([1,1,1])
  chart_dict = {
    c1: [

          ["Asset",
           columns_settings.asset_setting_val,
           ],
          ["Revenue",columns_settings.revenue_setting_val,'y2'],
          ['Profit Margin', columns_settings.profit_mrg_color_mapping],
          ['Dupoint Model', columns_settings.dupoint_setting_val,'y2']
          
          ],


    c2: [
      
          ["Liabilities",columns_settings.liabilities_setting_val],
          ["Income break down",columns_settings.income_breakdown_color_mapping],
          ["Capital Expenditure",columns_settings.capex_depr_setting_val],
         
         ],
         


    c3: [
          ["Cash Flow",columns_settings.cashflow_setting_val,],
          ["Cost Break down",columns_settings.cost_break_down_setting_val, 'y1'],
          ["Income", columns_settings.income_setting_val,'y2']

         ],
  }

  def merge_color_mapping(settings_dict):
      merged_dict = settings_dict['cols_val'].copy()  # Start with cols_val
      if settings_dict['line_val']:
          merged_dict.update({key: None for key in settings_dict['line_val'] if key})
      return merged_dict
  
  for chart in chart_dict.keys():
      with chart:
          cols_chart = chart_dict[chart]

          for i in range(len(cols_chart)):
              # Creating the col and line lists
              col_mapping = merge_color_mapping(cols_chart[i][1])
              title_chart = cols_chart[i][0]
              y_axis = cols_chart[i][2] if len(cols_chart[i]) > 2 else None

              st.plotly_chart(
                  plot_chart_function.create_stacked_bar_chart(
                      df_final,
                      title=title_chart,
                      bar_col=list(cols_chart[i][1]['cols_val'].keys()),  # Create col list
                      line_col=list(cols_chart[i][1]['line_val']),  # Create line list
                      color_mapping=col_mapping,
                        line_axis=y_axis  # Merged color mapping
                  )
              )

  numeric_cols = df_final.select_dtypes(include='number')
  pct_change_df = numeric_cols.pct_change()
  pct_change_df = pct_change_df.add_suffix('_pct_change')
  merge_dt = pd.merge(df_final, pct_change_df, how='left', left_index=True, right_index=True)
  st.write(merge_dt)

