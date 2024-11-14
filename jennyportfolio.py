import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Portfolio data from the attached PDF
portfolio_data = {
    'Ticker': ['IWN', 'ICLR', 'GMED', 'HLI', 'EWBC', 'NRG', 'BND', 'MEDP', 'ACLS', 
               'NMIH', 'COKE', 'OLED', 'ESNT', 'MTRN', 'CALM', 'BMI'],
    'Company Name': ['iShares:Russ 2000 Vl ETF', 'ICON PUBLIC LIMITED COMPANY', 'GLOBUS MEDICAL, INC.', 
                     'HOULIHAN LOKEY, INC.', 'EAST WEST BANCORP, INC.', 'NRG ENERGY, INC.', 'Vanguard Tot Bd;ETF', 'MEDPACE HOLDINGS, INC.', 
                     'AXCELIS TECHNOLOGIES, INC.', 'NMI HOLDINGS, INC.', 'COCA-COLA CONSOLIDATED, INC.', 'UNIVERSAL DISPLAY CORPORATION', 'ESSENT GROUP LTD', 
                     'MATERION CORPORATION', 'CAL-MAINE FOODS, INC.', 'BADGER METER, INC.'],
    'Main Holding': [2180, 206, 655, 483, 552, 530, 275, 177, 362, 1941, 36, 291, 829, 202, 1001, 269],
    'Board Holding': [28636, 1672, 5178, 4364, 5220, 5235, 0, 1716, 3506, 18837, 360, 2904, 9964, 2017, 10001, 2905],
    'Purchase Price': [137.99, 172.28, 47.60, 117.40, 69.43, 43.93, 69.93, 236.62, 121.31, 24.03, 589.46, 143.40, 54.24, 137.80, 57.45, 209.08],
    'Purchase Date': ['2014-09-25', '2020-01-29', '2020-02-20',  '2021-11-11', '2022-09-30', '2022-10-28', '2022-11-04', '2023-02-04', '2023-02-24', '2023-03-02', 
                      '2023-04-28', '2023-03-09', '2024-03-10', '2023-03-10', '2024-03-01', '2024-03-02'],
}

# Convert to DataFrame
portfolio = pd.DataFrame(portfolio_data)

# Function to fetch live data using yfinance
def get_live_data(ticker):
    stock = yf.Ticker(ticker)
    current_price = stock.history(period='1d')['Close'].iloc[-1]
    one_week_ago = datetime.now() - timedelta(days=7)
    week_ago_price = stock.history(start=one_week_ago, period='1d')['Close'].iloc[0]
    percent_change = ((current_price - week_ago_price) / week_ago_price) * 100
    return current_price, percent_change

# Function to calculate and update the portfolio table
def update_portfolio_table(portfolio):
    # Calculate total holding if it doesn't exist
    portfolio['Total Holding'] = portfolio['Main Holding'] + portfolio['Board Holding']
    
    # Create lists to store calculated data
    current_prices = []
    weekly_changes = []
    total_values = []

    # Update portfolio with live data
    for index, row in portfolio.iterrows():
        current_price, percent_change = get_live_data(row['Ticker'])
        current_prices.append(current_price)
        weekly_changes.append(percent_change)
        total_value = current_price * row['Total Holding']
        total_values.append(total_value)

    # Add the calculated data to the DataFrame
    portfolio['Current Price'] = current_prices
    portfolio['Weekly Change (%)'] = weekly_changes
    portfolio['Total Value'] = total_values

    return portfolio

# Streamlit UI
st.title("Live Portfolio Dashboard")

# Update portfolio with live data
portfolio = update_portfolio_table(portfolio)

# Display the portfolio as a table
st.subheader("Portfolio Holdings")
st.dataframe(portfolio[['Ticker', 'Company Name', 'Total Holding', 'Current Price', 'Weekly Change (%)', 'Total Value']])

# Calculate and display total portfolio value and overall weekly change
total_portfolio_value = sum(portfolio['Total Value'])
weighted_weekly_change = sum((portfolio['Total Value'] / total_portfolio_value) * portfolio['Weekly Change (%)'])

st.write(f"**Total Portfolio Value:** ${total_portfolio_value:,.2f}")
st.write(f"**Weekly Change:** {weighted_weekly_change:.2f}%")

