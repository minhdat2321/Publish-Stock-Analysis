import pandas as pd
import streamlit as st
from plotly import graph_objects as go
import fmpsdk
from function.common_function import json_flatton_data, transform_to_percentage


@st.cache_data
def load_data(apikey, Ticker='AAPL', period='quarter', limit=10):

    bsheet = pd.DataFrame(fmpsdk.balance_sheet_statement(apikey=apikey, symbol=Ticker, period=period, limit=limit))
    cashflow = pd.DataFrame(fmpsdk.cash_flow_statement(apikey=apikey, symbol=Ticker, period=period, limit=limit))
    income = pd.DataFrame(fmpsdk.income_statement(apikey=apikey, symbol=Ticker, period=period, limit=limit))
    ratio = pd.DataFrame(fmpsdk.financial_ratios(apikey=apikey, symbol=Ticker, period=period, limit=limit))
    financial_growth = pd.DataFrame(fmpsdk.financial_growth(apikey=apikey, symbol=Ticker,period=period, limit=limit))

    company_profile = pd.DataFrame(fmpsdk.company_profile(apikey=apikey, symbol=Ticker))


    ttm_ratio = pd.DataFrame(fmpsdk.financial_ratios_ttm(apikey=apikey, symbol=Ticker))


    segment_product = fmpsdk.revenue_product_by_segments(apikey, symbol=Ticker,period=period, limit=limit, structure='flat')
    segment_product = json_flatton_data(segment_product)
    try:
        segment_product = segment_product.drop('Product', axis=1)
    except KeyError:
        segment_product = segment_product
    segment_regions = fmpsdk.revenue_geographic_segmentation(apikey, symbol=Ticker,period=period, limit=limit, structure='flat')
    segment_regions = json_flatton_data(segment_regions)


    df_concat = pd.concat([bsheet,cashflow,income,ratio,financial_growth,ttm_ratio],axis=1)
    df_final = df_concat.loc[:, ~df_concat.columns.duplicated()]
   # df_final['date'] = pd.to_datetime(df_final['date'])r
    df_final['fiscal_date'] = df_final['period'].astype(str) + "-" +  df_final['calendarYear'].astype(str)
    df_final = df_final.set_index('fiscal_date')
    df_final = df_final[::-1]


    return df_final,company_profile, segment_product,segment_regions


@st.cache_data
def financial_num_data(apikey,tick='AAPL',period='annual'):

    bsr = pd.DataFrame(fmpsdk.balance_sheet_statement_as_reported(apikey=apikey,symbol=tick,period=period)).T
    incomer = pd.DataFrame(fmpsdk.income_statement_as_reported(apikey=apikey, symbol=tick,period=period)).T
    cashflowr = pd.DataFrame(fmpsdk.cash_flow_statement_as_reported(apikey=apikey, symbol=tick,period=period)).T
    try:
        bsr.columns = bsr.loc['date']
        incomer.columns = incomer.loc['date']
        cashflowr.columns = cashflowr.loc['date']

        bsr = bsr.drop(['date','symbol','period'])
        incomer = incomer.drop(['date','symbol','period'])
        cashflowr = cashflowr.drop(['date','symbol','period'])
    except KeyError:
        bsr = bsr
        incomer = incomer
        cashflowr = cashflowr


    return bsr, incomer, cashflowr

@st.cache_data
def valuation_data(apikey,tick='AAPL', period='quarter', limit= 30):

    pTarget = pd.DataFrame(fmpsdk.earnings_surprises(apikey, tick))
    estimate_dt = pd.DataFrame(fmpsdk.analyst_estimate(apikey, tick, period=period, limit=limit))

    return pTarget, estimate_dt

@st.cache_data
def analyst_data(apikey, tick='AAPL'):
    dt = pd.DataFrame(fmpsdk.analyst_recommendation(apikey=apikey, symbol=tick ))
    dt = dt.set_index("date")
    dt = dt.drop("symbol", axis=1)

    avg_price = pd.DataFrame(fmpsdk.price_target_summary(apikey, tick))
    return dt, avg_price