import sqlite3
import pandas as pd

def load_csv_to_sqlite():
    print("Connecting to local SQLite database (market_data.db)...")
    # This automatically creates the file if it doesn't exist
    conn = sqlite3.connect('market_data.db')
    
    try:
        # 1. Load Crypto Metadata
        print("Uploading cryptocurrencies...")
        df_crypto = pd.read_csv("records.csv")
        df_crypto.to_sql('cryptocurrencies', conn, if_exists='replace', index=False)

        # 2. Load Crypto Prices
        print("Uploading crypto_prices...")
        df_prices = pd.read_csv("historical_prices.csv")
        df_prices.to_sql('crypto_prices', conn, if_exists='replace', index=False)

        # 3. Load Oil Prices
        print("Uploading oil_prices...")
        df_oil = pd.read_csv("oil_prices.csv")
        df_oil.to_sql('oil_prices', conn, if_exists='replace', index=False)

        # 4. Load Stock Prices
        print("Uploading stock_prices...")
        df_stocks = pd.read_csv("stock_prices.csv")
        df_stocks.to_sql('stock_prices', conn, if_exists='replace', index=False)
        
        print("\nAll CSV data successfully uploaded to SQLite Database!")
        
    except Exception as e:
        print(f"An error occurred while uploading to SQLite: {e}")
    finally:
        # Always good practice to close the connection
        conn.close()

if __name__ == "__main__":
    load_csv_to_sqlite()