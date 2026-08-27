import streamlit as st

from tabs import fundamental_tabs





st.set_page_config(page_title='Stock Analysis', layout='wide', page_icon=':chart_with_upwards_trend:')

tick = st.text_input("Enter ticker", "AAPL")

fundamental_tabs.fundamental_chart(ticker=tick)
