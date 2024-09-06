import pandas 
import streamlit as st
import numpy as np
import pandas as pd

import fmpsdk


dt = fmpsdk.balance_sheet_statement(apikey="xxUbfrh3hsbcydCGtbYZxqpH1jaufUzB", symbol='AAPL')
st.write(dt)