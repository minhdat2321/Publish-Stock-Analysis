import pandas as pd
import streamlit as st
from function.common_function import json_flatton_data
from ModifiedModule import fmpsdk


class FMPDataError(RuntimeError):
    """Raised when Financial Modeling Prep does not return usable records."""


_ERROR_KEYS = {"error", "error message", "information", "message", "status", "code"}
_DATA_KEYS = ("data", "results", "result", "historical", "financials")


def response_records(response, endpoint):
    """Normalize the response shapes returned by old and new FMP endpoints.

    FMP normally returns a list of records, but newer endpoints may wrap records
    in a ``data``/``results`` object or return a single record.  API errors are
    dictionaries too; passing one directly to ``DataFrame`` produces Pandas'
    misleading "all scalar values" exception, so identify those first.
    """
    if response is None:
        raise FMPDataError(f"{endpoint} did not return a response.")

    if isinstance(response, list):
        records = response
    elif isinstance(response, dict):
        lower_keys = {str(key).lower() for key in response}
        if lower_keys & _ERROR_KEYS and not any(key in response for key in _DATA_KEYS):
            detail = next(
                (
                    response[key]
                    for key in response
                    if str(key).lower() in {"error", "error message", "information", "message"}
                ),
                "The API rejected the request.",
            )
            raise FMPDataError(f"{endpoint}: {detail}")

        wrapped = next((response[key] for key in _DATA_KEYS if key in response), None)
        if wrapped is not None:
            records = wrapped if isinstance(wrapped, list) else [wrapped]
        else:
            records = [response]
    else:
        raise FMPDataError(f"{endpoint} returned an unsupported response type.")

    records = [record for record in records if isinstance(record, dict)]
    if not records:
        raise FMPDataError(f"No data was returned by {endpoint}.")
    return records


def response_frame(response, endpoint):
    """Return a DataFrame from any supported FMP response shape."""
    return pd.DataFrame.from_records(response_records(response, endpoint))


def _add_legacy_aliases(frame, aliases):
    """Expose old column names used by the dashboard from Stable API fields."""
    for old_name, stable_name in aliases.items():
        if old_name not in frame and stable_name in frame:
            frame[old_name] = frame[stable_name]
    return frame

@st.cache_data
def load_data(apikey, Ticker='AAPL', period='quarter', limit=10):

    bsheet = response_frame(fmpsdk.balance_sheet_statement(apikey=apikey, symbol=Ticker, period=period, limit=limit), "balance sheet")

    cashflow = response_frame(fmpsdk.cash_flow_statement(apikey=apikey, symbol=Ticker, period=period, limit=limit), "cash flow statement")

    income = response_frame(fmpsdk.income_statement(apikey=apikey, symbol=Ticker, period=period, limit=limit), "income statement")
    
    ratio = response_frame(fmpsdk.financial_ratios(apikey=apikey, symbol=Ticker, period=period, limit=limit), "financial ratios")

    # ttm_ratio = pd.DataFrame(fmpsdk.financial_ratios_ttm(apikey=apikey, symbol=Ticker))

    segment_product = fmpsdk.revenue_product_by_segments(apikey, symbol=Ticker,period=period, limit=limit, structure='flat')
    segment_product = json_flatton_data(segment_product)
    try:
        segment_product = segment_product.drop('Product', axis=1)
    except KeyError:
        segment_product = segment_product
    segment_regions = fmpsdk.revenue_geographic_segmentation(apikey, symbol=Ticker,period=period, limit=limit, structure='flat')
    segment_regions = json_flatton_data(segment_regions)


    df_concat = pd.concat([bsheet,cashflow,income,ratio],axis=1)
    df_final = df_concat.loc[:, ~df_concat.columns.duplicated()]
    df_final = _add_legacy_aliases(df_final, {
        "calendarYear": "fiscalYear",
        "priceEarningsRatio": "priceToEarningsRatio",
        "priceEarningsToGrowthRatio": "priceToEarningsGrowthRatio",
    })


   # df_final['date'] = pd.to_datetime(df_final['date'])r
    df_final['fiscal_date'] = df_final['period'].astype(str) + "-" +  df_final['calendarYear'].astype(str)
    df_final = df_final.set_index('fiscal_date')
    df_final = df_final[::-1]
    period_shift = 4 if period == 'quarter' else 1
    numeric_cols = df_final.select_dtypes(include='number')
    pct_change_df = numeric_cols.pct_change(fill_method=None,periods=period_shift).map(lambda x: round(x, 4))

    pct_change_df = pct_change_df.add_suffix('_pct_change')
    merge_dt = pd.merge(df_final, pct_change_df, how='left', left_index=True, right_index=True)

    return merge_dt, segment_product, segment_regions


@st.cache_data
def header_data(apikey, Ticker='AAPL', period='quarter', limit=10):
    company_profile = response_frame(fmpsdk.company_profile(apikey=apikey, symbol=Ticker), "company profile")
    company_profile = _add_legacy_aliases(company_profile, {
        "changes": "change",
        "exchangeShortName": "exchange",
        "mktCap": "marketCap",
        "volAvg": "averageVolume",
    })

    ratio = response_frame(fmpsdk.financial_ratios(apikey=apikey, symbol=Ticker, period=period, limit=limit), "financial ratios")
    ratio = _add_legacy_aliases(ratio, {
        "priceEarningsRatio": "priceToEarningsRatio",
        "priceEarningsToGrowthRatio": "priceToEarningsGrowthRatio",
    })
    ttm_ratio = response_frame(fmpsdk.financial_ratios_ttm(apikey=apikey, symbol=Ticker), "TTM financial ratios")
    ttm_ratio = _add_legacy_aliases(ttm_ratio, {"peRatioTTM": "priceToEarningsRatioTTM"})

    df_concat = pd.concat([ ratio, ttm_ratio], axis=1)
    return df_concat, company_profile


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
