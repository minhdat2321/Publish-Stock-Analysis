import pandas as pd
import numpy as np
from columns_settings import adjust_columns


def calc_data(data,type_dt,roe_type,adjust_bs, period_option):
  ttm_cols = adjust_columns.cf_cols + adjust_columns.cols_income
  cols_average = adjust_columns.bs_cols


  data['TotalAssetToEquity'] = data['totalAssets']/data['totalEquity']
  rd_capitalize = data[['researchAndDevelopmentExpenses']]
  rd_capitalize = rd_capitalize.reset_index()

  # Amortization period (in quarters)
  amortization_period = 20

  # Create an amortization schedule
  amortization_schedule = []

  # Iterate over each quarter and compute amortization for each R&D expense
  for i in range(len(rd_capitalize)):
      for j in range(amortization_period):
          amortization_amount = rd_capitalize.loc[i, "researchAndDevelopmentExpenses"] / amortization_period
          unamortization_amt = rd_capitalize.loc[i, "researchAndDevelopmentExpenses"] - amortization_amount

          amortization_schedule.append({
              "Quarter": i+j,
              "Amortization R&D Expenses": amortization_amount,
              "Unamortization R&D": unamortization_amt,
          })

  amortization_df = pd.DataFrame(amortization_schedule)

  # Aggregate amortization expenses by quarter
  amortization_summary = amortization_df.groupby("Quarter").sum().reset_index()

  # Create a list of all possible quarters in the range
  all_quarters = pd.date_range(start='2017-07-01', periods=len(rd_capitalize)+amortization_period, freq='Q').to_period('Q')

  # Map the quarters to the amortization summary
  amortization_summary["Quarter Name"] = amortization_summary["Quarter"].apply(lambda x: all_quarters[x].strftime('Q%q-%Y'))

  # Display the amortization summary with quarter names
  amortization_summary = amortization_summary[["Quarter Name", "Amortization R&D Expenses","Unamortization R&D"]]
  amortization_summary = amortization_summary.set_index("Quarter Name")


  data = data.merge(amortization_summary, how='left', right_index=True, left_index=True)
  data['FCFE'] = data['netCashProvidedByOperatingActivities'] \
      - (data['capitalExpenditure'].map(lambda x : np.abs(x))) - data['researchAndDevelopmentExpenses'].map(lambda x : np.abs(x)) - (data['acquisitionsNet'].map(lambda x : np.abs(x))) \
      + data['depreciationAndAmortization'].map(lambda x : np.abs(x)) \
      - (data['debtRepayment'])   
  

  data['net_capex'] = data['capitalExpenditure'].apply(lambda x :np.abs(x)) \
      + data['researchAndDevelopmentExpenses'].apply(lambda x :np.abs(x)) \
          - data['depreciationAndAmortization'].apply(lambda x :np.abs(x))
  
  data['Non-cash Working Capital'] = data['netReceivables'] +  data['inventory'] + data['otherCurrentAssets'] \
                                          - data['shortTermDebt']
  
  data['Change in NCWC'] = data['Non-cash Working Capital'].diff()
  data['Debt Ratio'] = data['totalDebt']/data['totalEquity']
  data['Tax rate'] = data['incomeTaxExpense']/ data['netIncome']


  data['Reinvestment Rate'] = (data['net_capex'] + data['Change in NCWC'])* data['Debt Ratio'].apply(lambda x: 1-x) /data['operatingIncome'].apply(lambda x: x*(1-0.25))
  data['ROIC'] = data['operatingIncome'] * data['Tax rate'].apply(lambda x: 1-x )/(data['totalDebt'] +data['totalEquity'])

  
  if adjust_bs == 'Adjusted':

      


      data['Different R&D reportedAdjusted'] = data['researchAndDevelopmentExpenses'] - data['Amortization R&D Expenses']
      data['netCashProvidedByOperatingActivities'] = data['netCashProvidedByOperatingActivities'] + data['researchAndDevelopmentExpenses'] + data['Amortization R&D Expenses']
      data['netCashUsedForInvestingActivites'] = data['netCashUsedForInvestingActivites'] - data['researchAndDevelopmentExpenses']
      data['operatingIncome'] = data['operatingIncome'] + data['Different R&D reportedAdjusted']


      data['netIncome'] = data['netIncome'] + data['Different R&D reportedAdjusted']
      data['ebitda'] = data['ebitda'] + data['Different R&D reportedAdjusted']
      data['incomeBeforeTax'] = data['incomeBeforeTax'] + data['Different R&D reportedAdjusted']
      data['totalAssets'] = data['totalAssets'] + data['Unamortization R&D']


      data['FCFE'] = data['netCashProvidedByOperatingActivities'] \
          - (data['capitalExpenditure'].map(lambda x : np.abs(x))) - data['researchAndDevelopmentExpenses'].map(lambda x : np.abs(x)) - (data['acquisitionsNet'].map(lambda x : np.abs(x))) \
          + data['depreciationAndAmortization'].map(lambda x : np.abs(x)) \
          + (data['debtRepayment'])   

      data['totalEquity'] = data['totalEquity'] + data['Unamortization R&D'] 


      data['researchAndDevelopmentExpenses'] = data['Amortization R&D Expenses']
  else:
      data['Unamortization R&D'] = 0

  if type_dt == "TTM" and period_option == "quarter":

      
      data[ttm_cols] =  data[ttm_cols].rolling(window=4).sum()
      data[cols_average] = data[cols_average].rolling(window=4).mean()
  
  period = 4 if type_dt == "Normal" else 1
  data['FCFE Growth YoY'] = data['FCFE'].pct_change(periods=period).map(lambda x: round(x*100,2))
  data['net_capex'] = data['capitalExpenditure'].apply(lambda x :np.abs(x)) \
  + data['researchAndDevelopmentExpenses'].apply(lambda x :np.abs(x)) \
      - data['depreciationAndAmortization'].apply(lambda x :np.abs(x))
  

  data['net_capex Growth YoY'] = data['net_capex'].pct_change(periods=period).map(lambda x: round(x*100,2))

  
  
  data['Debt Ratio'] = data['totalDebt']/data['totalEquity']
  # Dupoint
  if roe_type == "Non Cash":
      data['totalEquity'] = data['totalEquity'] - data['cashAndCashEquivalents']


  data['TotalAssetToEquity'] = data['totalAssets'] / data['totalEquity']
  data['returnOnEquity'] = data['netIncome'] / data['totalEquity']
  data['netProfitMargin'] = data['netIncome'] / data['revenue']
  data['assetTurnover'] = data['revenue'] / data['totalAssets']
  data['netIncomePerEBT'] = data['netIncome'] / data['incomeBeforeTax']
  data['ebtPerEbit'] = data['incomeBeforeTax'] / data['operatingIncome']
  data['ebitPerRevenue'] = data['operatingIncome'] / data['revenue']
  
  # Profit margin
  data['grossProfitRatio'] = data['grossProfit'] / data['revenue'] 
  data['ebitdaratio'] = data['ebitda'] / data['revenue']
  data['incomeBeforeTaxRatio'] = data['incomeBeforeTax'] / data['revenue']
  data['netIncomeRatio'] = data['netIncome'] / data['revenue']

  # Percent change 
  data['revenueGrowth'] = data['revenue'].pct_change(periods=period).map(lambda x: round(x*100, 2))
  data['netIncomeGrowth'] = data['netIncome'].pct_change(periods=period).map(lambda x: round(x*100, 2))

  data['Tax rate'] = data['incomeTaxExpense']/ data['netIncome']

  data['Reinvestment Rate'] = (data['net_capex'] + data['Change in NCWC'])* data['Debt Ratio'].apply(lambda x: 1-x) /data['operatingIncome'].apply(lambda x: x*(1-0.25))
  data['ROIC'] = data['operatingIncome'] * data['Tax rate'].apply(lambda x: 1-x )/(data['totalDebt'] +data['totalEquity'])
  data['Interest Expense Ratio'] = data['interestExpense'] / data['totalDebt']
  data['ROE pumped'] = data['ROIC'] + data['Debt Ratio']* (data['ROIC'] - data['Interest Expense Ratio'] *data['Tax rate'].apply(lambda x : 1- x)  )
  data['Expected EBIT growth rate'] = data['ROIC'] * data['Reinvestment Rate']

  # Valuation

  data['epsdiluted'] = data['netIncome'] / data['weightedAverageShsOutDil']
  data['daysOfPayablesOutstanding'] = -data['daysOfPayablesOutstanding']





  return data