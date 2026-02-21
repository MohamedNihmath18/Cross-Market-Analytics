import requests
import time
from datetime import datetime
import pandas as pd
import yfinance as yf

def extract_crypto_metadata():
    print("Fetching crypto metadata (5 pages)...")
    all_records = []
    
    # Looping through 5 pages to collect 1,250 coins
    for i in range(1, 6):
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&per_page=250&order=market_cap_desc&page={i}&sparkline=False"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            all_records.extend(data)
            print(f"Page {i} added. Total records: {len(all_records)}")
        else:
            print(f"Failed to fetch data from page {i}. {response.status_code}")
        time.sleep(15)
        
    records = []
    for i in all_records:
        # Using a try-except because some lesser-known coins might have a missing 'last_updated' field
        try:
            date_only = datetime.strptime(i['last_updated'], "%Y-%m-%dT%H:%M:%S.%fZ").date().isoformat()
        except:
            date_only = None
            
        records.append(dict(
            id = i['id'],
            symbol = i['symbol'],
            name = i['name'],
            current_price = i['current_price'],
            market_cap = i['market_cap'],
            market_cap_rank = i['market_cap_rank'],
            total_volume = i['total_volume'],
            circulating_supply = i['circulating_supply'],
            total_supply = i['total_supply'],
            ath = i['ath'],
            atl = i['atl'],
            last_updated = date_only
        ))
        
    records_df = pd.DataFrame(records)
    records_df.to_csv("records.csv", index=False)
    print("Saved records.csv\n")
    return records_df

def extract_crypto_prices(records_df):
    top3 = records_df.sort_values("market_cap_rank").head(3)["id"].tolist()
    print(f"Fetching historical prices for: {top3}")
    
    historical_records = []
    for coin in top3:
        url = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=inr&days=365'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            for price in data['prices']:
                date = datetime.fromtimestamp(price[0] / 1000).date().isoformat()
                price_val = price[1]
                
                historical_records.append({
                    "coin_id": coin,
                    "date": date,
                    "price_usd": price_val  # Must match the SQLite schema column name
                })
            print(f"{coin} data collected successfully")
        else:
            print(f"Failed for {coin}: {response.status_code}")
        time.sleep(10)  
        
    hist_df = pd.DataFrame(historical_records)
    hist_df.to_csv("historical_prices.csv", index=False)
    print("Saved historical_prices.csv\n")

def extract_oil_prices():
    print("Fetching Oil Prices...")
    oil_df = pd.read_csv('https://raw.githubusercontent.com/datasets/oil-prices/main/data/wti-daily.csv')
    oil_df['Date'] = pd.to_datetime(oil_df['Date'])
    
    oil_filtered = oil_df[
        (oil_df['Date'] >= '2020-01-01') &
        (oil_df['Date'] <= '2026-01-01')
    ].copy()
    
    oil_filtered = oil_filtered.rename(columns={'Date': 'date', 'Price': 'price_usd'})
    oil_filtered['date'] = oil_filtered['date'].dt.date
    
    oil_filtered.to_csv("oil_prices.csv", index=False)
    print("Saved oil_prices.csv\n")

def extract_stock_prices():
    print("Fetching Stock Prices...")
    tickers = ["^GSPC", "^IXIC", "^NSEI"]
    all_stocks = []
    
    for ticker in tickers:
        df = yf.download(ticker, start="2020-01-01", end="2025-12-31", progress=False).reset_index()
        df['ticker'] = ticker
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        all_stocks.append(df)
        
    final_stock_df = pd.concat(all_stocks, ignore_index=True).dropna()
    final_stock_df = final_stock_df.rename(columns={
        'Date': 'date', 'Open': 'open', 'High': 'high', 
        'Low': 'low', 'Close': 'close', 'Volume': 'volume'
    })
    final_stock_df['date'] = pd.to_datetime(final_stock_df['date']).dt.date
    final_stock_df = final_stock_df[['date', 'open', 'high', 'low', 'close', 'volume', 'ticker']]
    
    final_stock_df.to_csv("stock_prices.csv", index=False)
    print("Saved stock_prices.csv\n")

if __name__ == "__main__":
    records_df = extract_crypto_metadata()
    extract_crypto_prices(records_df)
    extract_oil_prices()
    extract_stock_prices()
    print("All data successfully extracted and staged as CSVs!")