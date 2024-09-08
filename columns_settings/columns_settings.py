asset_setting_val = {
  
    'cols_val':
        {'cashAndCashEquivalents': '#2adaf3',
        'shortTermInvestments': '#17c684',
        'longTermInvestments': '#4062df',
        'netReceivables': '#e91ddc',
        'inventory': '#f7e016',
        'propertyPlantEquipmentNet': '#d6455d',
        'goodwillAndIntangibleAssets': 'red',
        'otherCurrentAssets': '#047246',
        'otherNonCurrentAssets': '#996908',
        "Unamortization R&D" : "pink"
        },

    'line_val':{
    }

}


cashflow_setting_val = {
    'cols_val':

        {'netCashProvidedByOperatingActivities': '#4062df',
        'netCashUsedForInvestingActivites': 'green',
        'netCashUsedProvidedByFinancingActivities': '#f7e016',},
    'line_val': {
            "cashAtEndOfPeriod": "red"

    }

}

revenue_setting_val = {
        'cols_val':
            {'revenue': '#2adaf3',},

        'line_val':{
          'revenue_pct_change': 'blue'
        }

}

income_setting_val = {
      'cols_val':
            {'netIncome': '#2adaf3',},

        'line_val':{
          'netIncome_pct_change': 'yellow'
        }

}


liabilities_setting_val = {
  
  'cols_val':
        {'shortTermDebt': '#e43753',
        'longTermDebt': '#f7e016',
        'accountPayables': '#e91ddc',
        'otherCurrentLiabilities': '#1f4b43',
        'otherLiabilities': '#cc6095',
        'preferredStock': '#a93e52',
        'othertotalStockholdersEquity':'#4062df',
        'retainedEarnings': '#12df91',
        'accumulatedOtherComprehensiveIncomeLoss': '#4f2d3c',
        'otherNonCurrentLiabilities':'brown',
        "Unamortization R&D" : "pink",
        'commonStock': '#4062df',

        },

  'line_val':{}

}


cost_break_down_setting_val = {
  'cols_val':
        { 
        'researchAndDevelopmentExpenses':'#4062df',
        'sellingGeneralAndAdministrativeExpenses':'#f7e016',
        'otherExpenses':'#996805',
        'costOfRevenue':'#e43753',

        },
    'line_val':{'revenue': '#2adaf3'}

}


income_breakdown_color_mapping = {
  'cols_val':
        {
        'operatingIncome':'#4062df',
        'totalOtherIncomeExpensesNet':'#e98ef5',
        },
    'line_val':{}
}



profit_mrg_color_mapping = {
    'cols_val':

        {

        },

    'line_val':{
        'grossProfitRatio':'#4062df',
        'ebitdaratio':'#f7e016',
        'incomeBeforeTaxRatio':'#e98ef5',
        'netIncomeRatio' : 'green'
    }
}

capex_depr_setting_val = {
    'cols_val':
        {
        'capitalExpenditure':'#4062df',
        'depreciationAndAmortization':'#f7e016',
        'researchAndDevelopmentExpenses': 'orange'
        },
    'line_val':{
      'net_capex':'#e98ef5'
    }
}


stock_ratio_color_mapping = {
    'cols_val':
        {
        'priceEarningsRatio':'red',
        'enterpriseValueMultiple':'#f7e016',
        'priceToBookRatio':'#e98ef5'
        },

    'line_val':{}
}

dupoint_setting_val = {
  'cols_val':
        {    
        'returnOnEquity':'green',

        },
    'line_val':{
        'assetTurnover':'#f7e016',
        'netProfitMargin':'#e98ef5',
        'TotalAssetToEquity':'#e98ef5',
    }

}

profit_margin_dupoint_break_setting_val = {
    'cols_val':

        { 
        'netIncomePerEBT': 'Tax burden',
        'ebtPerEbit': 'Interest Burden',
        'ebitPerRevenue': 'EBIT margin'
        },
    'line_val': {}
}


operating_cycle_setting_val = {
    'cols_val':

        { 
        'daysOfInventoryOutstanding':'yellow',
        'daysOfPayablesOutstanding':'pink',
        'daysOfSalesOutstanding':'green',
        },

    'line_val':{}
}