# Stock Analysis Dashboard

A Python and Streamlit project for **fundamental stock analysis and financial-data visualization**. The application retrieves company financial data, combines key statements and ratios, calculates period-over-period changes, and presents the results through an interactive dashboard.

## Why I Built This

Financial statements contain a large amount of information, but reviewing them manually across many periods can be time-consuming. This project explores how Python can be used to consolidate financial data and turn it into a more accessible analytical dashboard.

The project reflects my interest in combining **finance, data analytics, reporting, and automation**.

## Key Features

- Search and analyze a company by ticker symbol
- Retrieve financial data through the Financial Modeling Prep API
- Consolidate balance sheet, income statement, cash-flow, and financial-ratio data
- Compare quarterly and annual reporting periods
- Calculate period-over-period percentage changes
- Visualize assets, liabilities, revenue, income, cash flow, margins, and capital expenditure
- Analyze ROIC and DuPont-related metrics
- Review operating-cycle metrics
- Explore revenue by product and geographic segment when data is available
- Display interactive charts with Streamlit and Plotly

## Tech Stack

- **Python**
- **Pandas** for data transformation and consolidation
- **NumPy** for numerical operations
- **Streamlit** for the interactive web application
- **Plotly** for financial-data visualization
- **Financial Modeling Prep API** for company financial data

## Project Structure

```text
Publish-Stock-Analysis/
├── main.py                  # Streamlit application entry point
├── tabs/                    # Dashboard sections and financial-analysis views
├── function/                # API, utility, and visualization functions
├── data_handling/           # Data transformation and calculation logic
├── columns_settings/        # Dashboard metric and chart configuration
├── ModifiedModule/          # Supporting API module
├── requirements.txt
└── README.md
```

## How the Data Pipeline Works

```text
Financial Modeling Prep API
          ↓
Balance Sheet / Income Statement / Cash Flow / Ratios
          ↓
Python + Pandas data consolidation
          ↓
Financial calculations and percentage-change analysis
          ↓
Streamlit + Plotly dashboard
          ↓
Interactive financial insights
```

## Example Analytical Areas

The dashboard is designed to support analysis of areas such as:

- Revenue and income trends
- Asset and liability structure
- Profitability and margins
- Cash-flow development
- Capital expenditure
- Return on invested capital
- DuPont analysis
- Operating cycle
- Product and geographic revenue mix

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/minhdat2321/Publish-Stock-Analysis.git
cd Publish-Stock-Analysis
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

The application requires a Financial Modeling Prep API key. Keep credentials outside version control, for example through Streamlit secrets or a local configuration file that is ignored by Git.

### 5. Run the dashboard

```bash
streamlit run main.py
```

## Skills Demonstrated

This project demonstrates practical experience with:

- Financial statement analysis
- Financial-data consolidation
- Data cleaning and transformation
- Python-based reporting workflows
- Dashboard development
- Interactive data visualization
- API integration
- Modular application development

## Future Improvements

- Add clearer KPI summaries and variance-analysis views
- Improve exception handling and data validation
- Expand valuation and analyst-estimate functionality
- Add automated tests for financial calculations
- Add dashboard screenshots and a live demonstration
- Improve deployment and configuration documentation

## Author

**Minh Dat**  
Finance & Data Analytics  
GitHub: [@minhdat2321](https://github.com/minhdat2321)
