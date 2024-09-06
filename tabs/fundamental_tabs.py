import pandas 
import streamlit as st
import numpy as np
import pandas as pd

from dotenv import load_dotenv
import os
import fmpsdk
import config

def test_call():
  load_dotenv()
  api_key = config.API_KEY_FMP

  dt = fmpsdk.balance_sheet_statement(apikey=api_key, symbol='AAPL')
  st.write(dt)