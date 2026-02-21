import streamlit as st
import pandas as pd
import sqlite3
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="Cross-Market Analysis", page_icon="📈", layout="wide")

# Connect to the SQLite database
@st.cache_resource
def get_db_connection():
    conn = sqlite3.connect('market_data.db', check_same_thread=False)
    return conn

conn = get_db_connection()

# Sidebar navigation menu using streamlit-option-menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Data Exploration", "SQL Query Runner", "Crypto Analysis"],
        icons=["bar-chart", "database", "currency-bitcoin"],
        menu_icon="cast",
        default_index=0,
    )

# ==========================================
# 🔹 PAGE 1: Filters & Data Exploration
# ==========================================
if selected == "Data Exploration":
    st.title("🌍 Cross-Market Data Exploration")
    st.write("Compare the performance of Bitcoin, Oil, and Global Stock Indices.")

    # Date Filters
    st.subheader("Filter Data by Date")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", pd.to_datetime('2025-02-01'))
    with col2:
        end_date = st.date_input("End Date", pd.to_datetime('2026-02-18'))

    # Fetch Averages using SQL
    query_avg = f"""
    SELECT 
        (SELECT AVG(price_usd) FROM crypto_prices WHERE coin_id='bitcoin' AND date BETWEEN '{start_date}' AND '{end_date}') as avg_btc,
        (SELECT AVG(price_usd) FROM oil_prices WHERE date BETWEEN '{start_date}' AND '{end_date}') as avg_oil,
        (SELECT AVG(close) FROM stock_prices WHERE ticker='^GSPC' AND date BETWEEN '{start_date}' AND '{end_date}') as avg_sp500,
        (SELECT AVG(close) FROM stock_prices WHERE ticker='^NSEI' AND date BETWEEN '{start_date}' AND '{end_date}') as avg_nifty
    """
    avg_df = pd.read_sql_query(query_avg, conn)

    # Display Metrics
    st.subheader("📊 Average Prices for Selected Period")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Bitcoin (USD)", f"${avg_df['avg_btc'][0]:,.2f}" if pd.notna(avg_df['avg_btc'][0]) else "No Data")
    m2.metric("Oil WTI (USD)", f"${avg_df['avg_oil'][0]:,.2f}" if pd.notna(avg_df['avg_oil'][0]) else "No Data")
    m3.metric("S&P 500", f"{avg_df['avg_sp500'][0]:,.2f}" if pd.notna(avg_df['avg_sp500'][0]) else "No Data")
    m4.metric("NIFTY 50", f"{avg_df['avg_nifty'][0]:,.2f}" if pd.notna(avg_df['avg_nifty'][0]) else "No Data")

    # Daily Market Snapshot Table (SQL JOIN)
    st.subheader("📅 Daily Market Snapshot")
    st.write("A combined view of Bitcoin, Oil, S&P 500, and NIFTY prices using SQL JOINs.")
    query_snapshot = f"""
    SELECT 
        c.date, 
        c.price_usd as btc_price, 
        o.price_usd as oil_price, 
        s1.close as sp500_close,
        s2.close as nifty_close
    FROM crypto_prices c
    LEFT JOIN oil_prices o ON c.date = o.date
    LEFT JOIN stock_prices s1 ON c.date = s1.date AND s1.ticker = '^GSPC'
    LEFT JOIN stock_prices s2 ON c.date = s2.date AND s2.ticker = '^NSEI'
    WHERE c.coin_id = 'bitcoin' AND c.date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY c.date DESC
    """
    snapshot_df = pd.read_sql_query(query_snapshot, conn)
    st.dataframe(snapshot_df, use_container_width=True)


# ==========================================
# 🔹 PAGE 2: SQL Query Runner
# ==========================================
elif selected == "SQL Query Runner":
    st.title("🔎 SQL Query Runner")
    st.write("Execute predefined SQL analytics directly against the database.")

    # Dictionary of ALL predefined queries from queries.sql
    queries = {
        "Crypto: Top 3 cryptocurrencies by market cap": "SELECT id, symbol, name, market_cap FROM cryptocurrencies ORDER BY market_cap DESC LIMIT 3;",
        "Crypto: Coins where circulating supply > 90% total": "SELECT name, circulating_supply, total_supply FROM cryptocurrencies WHERE total_supply IS NOT NULL AND total_supply > 0 AND circulating_supply > (0.90 * total_supply);",
        "Crypto: Coins within 10% of ATH": "SELECT name, current_price, ath FROM cryptocurrencies WHERE current_price >= (0.90 * ath);",
        "Crypto: Avg market cap rank of coins with vol > $1B": "SELECT AVG(market_cap_rank) as avg_rank_high_volume FROM cryptocurrencies WHERE total_volume > 1000000000;",
        "Crypto: Most recently updated coin": "SELECT name, last_updated FROM cryptocurrencies ORDER BY last_updated DESC LIMIT 1;",

        "Crypto Prices: Highest daily price of Bitcoin (last 365 days)": "SELECT MAX(price_usd) as highest_btc_price_1yr FROM crypto_prices WHERE coin_id = 'bitcoin' AND date >= date('now', '-365 days');",
        "Crypto Prices: Average daily price of Ethereum (past 1 year)": "SELECT AVG(price_usd) as avg_eth_price_1yr FROM crypto_prices WHERE coin_id = 'ethereum';",
        "Crypto Prices: Daily price trend of Bitcoin in Jan 2025": "SELECT date, price_usd FROM crypto_prices WHERE coin_id = 'bitcoin' AND date BETWEEN '2025-01-01' AND '2025-01-31' ORDER BY date;",
        "Crypto Prices: Coin with highest average price over 1 year": "SELECT coin_id, AVG(price_usd) as avg_price FROM crypto_prices GROUP BY coin_id ORDER BY avg_price DESC LIMIT 1;",
        "Crypto Prices: % change in Bitcoin price between Sep 2024 and Sep 2025": "WITH sep2024 AS (SELECT AVG(price_usd) as p_start FROM crypto_prices WHERE coin_id = 'bitcoin' AND strftime('%Y-%m', date) = '2024-09'), sep2025 AS (SELECT AVG(price_usd) as p_end FROM crypto_prices WHERE coin_id = 'bitcoin' AND strftime('%Y-%m', date) = '2025-09') SELECT ((p_end - p_start) / p_start) * 100 as btc_percentage_change FROM sep2024, sep2025;",

        "Oil: Highest oil price in the last 5 years": "SELECT MAX(price_usd) as max_oil_price_5yrs FROM oil_prices WHERE date >= '2021-01-01';",
        "Oil: Average oil price per year": "SELECT strftime('%Y', date) as year, AVG(price_usd) as avg_oil_price FROM oil_prices GROUP BY year ORDER BY year;",
        "Oil: Oil prices during COVID crash (March-April 2020)": "SELECT date, price_usd FROM oil_prices WHERE date BETWEEN '2020-03-01' AND '2020-04-30' ORDER BY date;",
        "Oil: Lowest price of oil in the last 10 years": "SELECT MIN(price_usd) as min_oil_price FROM oil_prices;",
        "Oil: Volatility of oil prices (max-min difference per year)": "SELECT strftime('%Y', date) as year, (MAX(price_usd) - MIN(price_usd)) as price_volatility FROM oil_prices GROUP BY year ORDER BY year;",

        "Stocks: All stock prices for a given ticker (^GSPC)": "SELECT date, open, high, low, close, volume FROM stock_prices WHERE ticker = '^GSPC' ORDER BY date DESC;",
        "Stocks: Highest closing price for NASDAQ (^IXIC)": "SELECT MAX(close) as highest_nasdaq_close FROM stock_prices WHERE ticker = '^IXIC';",
        "Stocks: Top 5 days with highest price difference for S&P 500 (^GSPC)": "SELECT date, (high - low) as daily_volatility FROM stock_prices WHERE ticker = '^GSPC' ORDER BY daily_volatility DESC LIMIT 5;",
        "Stocks: Monthly average closing price for each ticker": "SELECT ticker, strftime('%Y-%m', date) as month, AVG(close) as avg_monthly_close FROM stock_prices GROUP BY ticker, month ORDER BY ticker, month;",
        "Stocks: Average trading volume of NSEI in 2024": "SELECT AVG(volume) as avg_nsei_volume_2024 FROM stock_prices WHERE ticker = '^NSEI' AND strftime('%Y', date) = '2024';",

        "Join: Compare Bitcoin vs Oil average price in 2025": "SELECT AVG(c.price_usd) as avg_btc_price, AVG(o.price_usd) as avg_oil_price FROM crypto_prices c JOIN oil_prices o ON c.date = o.date WHERE c.coin_id = 'bitcoin' AND strftime('%Y', c.date) = '2025';",
        "Join: Check if Bitcoin moves with S&P 500": "SELECT c.date, c.price_usd as btc_price, s.close as sp500_close FROM crypto_prices c JOIN stock_prices s ON c.date = s.date WHERE c.coin_id = 'bitcoin' AND s.ticker = '^GSPC' ORDER BY c.date DESC;",
        "Join: Compare Ethereum and NASDAQ daily prices for 2025": "SELECT c.date, c.price_usd as eth_price, s.close as nasdaq_close FROM crypto_prices c JOIN stock_prices s ON c.date = s.date WHERE c.coin_id = 'ethereum' AND s.ticker = '^IXIC' AND strftime('%Y', c.date) = '2025' ORDER BY c.date;",
        "Join: Days oil price spiked compared with Bitcoin": "SELECT o.date, o.price_usd as oil_price, c.price_usd as btc_price FROM oil_prices o LEFT JOIN crypto_prices c ON o.date = c.date AND c.coin_id = 'bitcoin' ORDER BY o.price_usd DESC LIMIT 10;",
        "Join: Compare top 3 coins vs Nifty (^NSEI)": "SELECT c.date, c.coin_id, c.price_usd as crypto_price, s.close as nifty_close FROM crypto_prices c JOIN stock_prices s ON c.date = s.date WHERE s.ticker = '^NSEI' ORDER BY c.date DESC;",
        "Join: Compare S&P 500 with crude oil prices": "SELECT s.date, s.close as sp500_close, o.price_usd as oil_price FROM stock_prices s JOIN oil_prices o ON s.date = o.date WHERE s.ticker = '^GSPC' ORDER BY s.date DESC;",
        "Join: Correlate Bitcoin with crude oil closing price": "SELECT c.date, c.price_usd as btc_price, o.price_usd as oil_price FROM crypto_prices c JOIN oil_prices o ON c.date = o.date WHERE c.coin_id = 'bitcoin' ORDER BY c.date DESC;",
        "Join: Compare NASDAQ with Ethereum price trends": "SELECT s.date, s.close as nasdaq_close, c.price_usd as eth_price FROM stock_prices s JOIN crypto_prices c ON s.date = c.date WHERE s.ticker = '^IXIC' AND c.coin_id = 'ethereum' ORDER BY s.date DESC;",
        "Join: Top 3 crypto coins with stock indices for 2025": "SELECT c.date, c.coin_id, c.price_usd, s.ticker, s.close as index_close FROM crypto_prices c JOIN stock_prices s ON c.date = s.date WHERE strftime('%Y', c.date) = '2025' ORDER BY c.date DESC;",
        "Join: Multi-join - Stock, Oil, and Bitcoin daily comparison": "SELECT c.date, c.price_usd as btc_price, o.price_usd as oil_price, s.close as sp500_close FROM crypto_prices c JOIN oil_prices o ON c.date = o.date JOIN stock_prices s ON c.date = s.date WHERE c.coin_id = 'bitcoin' AND s.ticker = '^GSPC' ORDER BY c.date DESC;"
    }

    query_name = st.selectbox("Select a query to run:", list(queries.keys()))
    selected_query = queries[query_name]

    st.markdown("**SQL Code:**")
    st.code(selected_query, language="sql")

    if st.button("Run Query", type="primary"):
        try:
            result_df = pd.read_sql_query(selected_query, conn)
            st.success("Query executed successfully!")
            st.dataframe(result_df, use_container_width=True)
        except Exception as e:
            st.error(f"An error occurred: {e}")


# ==========================================
# 🔹 PAGE 3: Top 5 Crypto Analysis
# ==========================================
elif selected == "Crypto Analysis":
    st.title("🪙 Cryptocurrency Analysis")
    st.write("Deep dive into the daily price trends of top cryptocurrencies.")
    
    # Get the Top 3 coins by market cap directly from the database
    top_coins_query = "SELECT id, name FROM cryptocurrencies ORDER BY market_cap DESC LIMIT 3"
    try:
        top_coins_df = pd.read_sql_query(top_coins_query, conn)
        # Map the formatted name to the raw coin_id
        coin_dict = dict(zip(top_coins_df['name'], top_coins_df['id']))
        coin_names = list(coin_dict.keys())
    except Exception:
        # Fallback list just in case the table isn't populated
        coin_names = ['Bitcoin', 'Ethereum', 'Tether']
        coin_dict = {'Bitcoin': 'bitcoin', 'Ethereum': 'ethereum', 'Tether': 'tether'}
    
    selected_coin_name = st.selectbox("Select Cryptocurrency (Top 3 by Market Cap)", coin_names)
    selected_coin_id = coin_dict[selected_coin_name]
    
    # Date Filters for this specific page
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", pd.to_datetime('2025-02-01'), key='c_start')
    with col2:
        end_date = st.date_input("End Date", pd.to_datetime('2026-02-18'), key='c_end')

    # Fetch data for the selected coin and date range
    query_crypto = f"""
    SELECT date, price_usd 
    FROM crypto_prices 
    WHERE coin_id = '{selected_coin_id}' AND date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY date
    """
    crypto_df = pd.read_sql_query(query_crypto, conn)

    if not crypto_df.empty:
        st.subheader(f"{selected_coin_name} Daily Price Trend")
        
        # Ensure date is parsed as a proper datetime object for the line chart
        crypto_df['date'] = pd.to_datetime(crypto_df['date'])
        
        # Render the interactive Line Chart
        st.line_chart(crypto_df.set_index('date')['price_usd'])
        
        # Render the Raw Data Table
        st.subheader("Daily Price Table")
        st.dataframe(crypto_df, use_container_width=True)
    else:
        st.warning("No data available for the selected coin and date range. Try adjusting the dates.")