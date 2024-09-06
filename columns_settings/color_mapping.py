asset_color_mapping = {
    'cashAndCashEquivalents': '#2adaf3',
    'shortTermInvestments': '#17c684',
    'longTermInvestments': '#4062df',
    'netReceivables': '#e91ddc',
    'inventory': '#f7e016',
    'propertyPlantEquipmentNet': '#d6455d',
    'goodwillAndIntangibleAssets': 'red',
    'otherCurrentAssets': '#047246',
    'otherNonCurrentAssets': '#996908',
    # "Unamortization R&D": "pink"
}


cashflow_color_mapping = {
    'netCashProvidedByOperatingActivities': '#4062df',
    'netCashUsedForInvestingActivites': 'green',
    'netCashUsedProvidedByFinancingActivities': '#f7e016',
}

revenue_color_mapping = {
    'revenue': '#2adaf3',
}

income_color_mapping = {
  "netIncome":'#e91ddc'
}

liabilities_color_mapping = {
    'shortTermDebt': '#e43753',
    'longTermDebt': '#f7e016',
    'accountPayables': '#e91ddc',
    'otherCurrentLiabilities': '#1f4b43',
    'otherLiabilities': '#cc6095',
    'preferredStock': '#a93e52',
    'othertotalStockholdersEquity':'#4062df',
    'retainedEarnings': '#12df91',
    'accumulatedOtherComprehensiveIncomeLoss': '#4f2d3c',
    'commonStock': '#4062df',
    'otherNonCurrentLiabilities':'brown',
    # "Unamortization R&D" : "pink"

}


cost_color_mapping = {
    'costOfRevenue':'#e43753',
    'researchAndDevelopmentExpenses':'#4062df',
    'sellingGeneralAndAdministrativeExpenses':'#f7e016',
    'otherExpenses':'#996805'
}


income_breakdown_color_mapping = {
    'operatingIncome':'#4062df',
    'totalOtherIncomeExpensesNet':'#e98ef5',
}



profit_mrg_color_mapping = {
    'operatingIncome':'#4062df',
    'interestIncome':'#f7e016',
    'totalOtherIncomeExpensesNet':'#e98ef5',
    'incomeBeforeTaxRatio' : 'green'
}

capex_invest_color_mapping = {
    'capitalExpenditure':'green',
    'depreciationAndAmortization':'#f7e016',
    'researchAndDevelopmentExpenses': 'orange'

}

stock_ratio_color_mapping = {
    'priceEarningsRatio':'red',
    'enterpriseValueMultiple':'#f7e016',
    'priceToBookRatio':'#e98ef5'
}

dupoint_color_mapping = {
    'returnOnEquity':'red',
    'assetTurnover':'#f7e016',
    'netProfitMargin':'#e98ef5',
    'TotalAssetToEquity':'#e98ef5',

}

profit_margin_break_down_cols = {
    'netIncomePerEBT': 'Tax burden',
    'ebtPerEbit': 'Interest Burden',
    'ebitPerRevenue': 'EBIT margin'
}


operating_cycle_color_mapping = {
    'daysOfInventoryOutstanding':'yellow',
    'daysOfPayablesOutstanding':'pink',
    'daysOfSalesOutstanding':'green',
}