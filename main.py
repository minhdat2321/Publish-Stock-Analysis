import pandas 
import streamlit as st
import numpy as np
import pandas as pd
import fmpsdk

from tabs import fundamental_tabs





st.set_page_config(page_title='Stock Analysis', layout='wide', page_icon=':chart_with_upwards_trend:')

tick = st.text_input("Enter ticker", "AAPL")

fundamental_tabs.fundamental_chart(ticker=tick)