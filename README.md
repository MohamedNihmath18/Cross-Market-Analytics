# Cross-Market-Analytics
# 📈 Cross-Market Analysis: Crypto, Oil & Stocks with SQL and Streamlit

[cite_start]An end-to-end data engineering and Financial Analytics platform built to investigate the behavioral relationships between digital assets, traditional commodities, and global stock indices[cite: 5, 13, 15]. 


## ❓ Problem Statement
[cite_start]Cryptocurrency is frequently compared to traditional assets, but is it truly behaving like "digital gold" or does it represent a completely different class of asset[cite: 15, 16]? [cite_start]This project aims to uncover patterns, correlations, and relative performance between top cryptocurrencies, WTI crude oil, and major stock indices over the past few years[cite: 18, 19, 20, 21].

## 💼 Business Use Cases
This analytics platform serves several real-world financial applications:
* [cite_start]**Investment Research:** Determine whether assets like Bitcoin move with or against traditional oil and stock markets[cite: 25].
* [cite_start]**Risk Management:** Evaluate the volatility of the crypto market compared to traditional, established assets[cite: 26, 28, 29].
* [cite_start]**Macro-Economic Analysis:** Study how global events, such as the 2020 COVID-19 crash, impact cryptocurrency prices[cite: 30, 137].
* [cite_start]**Cross-Market Trading:** Test hypotheses for trading strategies, such as hedging with the S&P 500 during crypto downturns[cite: 31].

## 🛠️ Technical Stack
* [cite_start]**Language:** Python [cite: 276]
* [cite_start]**Data Processing:** Pandas [cite: 11]
* [cite_start]**Database:** SQLite (Relational Database Design) [cite: 77, 276]
* [cite_start]**Frontend:** Streamlit [cite: 10]
* [cite_start]**APIs & Data Sources:** CoinGecko API, Yahoo Finance API, GitHub Raw CSVs [cite: 276]

## 🚀 ETL Workflow & Architecture
[cite_start]This project utilizes a robust ETL (Extract, Transform, Load) workflow[cite: 9]:

1. [cite_start]**Data Collection (Extract):** * Harvested cryptocurrency metadata and 1-year historical prices for the Top 3 coins via the CoinGecko API with proper pagination[cite: 37, 50, 278, 280].
   * [cite_start]Fetched daily WTI Crude Oil prices (2020–2026) from a raw GitHub dataset[cite: 59, 60, 64].
   * [cite_start]Downloaded historical daily stock data (`^GSPC`, `^IXIC`, `^NSEI`) using the Yahoo Finance endpoint[cite: 67, 68].
2. [cite_start]**Data Cleaning (Transform):** Standardized dates, cleaned missing values, and mapped data structures using Pandas[cite: 11, 276].
3. [cite_start]**Database Insertion (Load):** Automated the creation of a relational schema and inserted the transformed records into SQLite tables (`cryptocurrencies`, `crypto_prices`, `oil_prices`, `stock_prices`) using Python's DB API[cite: 78, 79, 84, 99, 110, 285].

## 📊 Streamlit Dashboard Features

[cite_start]The interactive web application consists of three main analytical modules[cite: 161, 162]:

* [cite_start]**🔹 Page 1: Filters & Data Exploration:** Users can apply date filters to view average prices and a daily market snapshot table that combines Bitcoin, Oil, S&P 500, and NIFTY prices using complex SQL `JOIN` queries[cite: 163, 164, 169, 174].
* **🔹 Page 2: SQL Query Runner:** Demonstrates SQL analytics directly inside the app. [cite_start]Users can select from 25 predefined queries (e.g., finding the highest oil price in 5 years or comparing Ethereum vs. NASDAQ) and execute them directly against the backend database[cite: 115, 230, 231, 237].
* [cite_start]**🔹 Page 3: Top Crypto Analysis:** Provides a deep dive into the top 3 cryptocurrencies by market cap, featuring interactive daily price trend line charts and raw data tables[cite: 253, 254, 257, 258].

## 💻 Local Setup & Installation
To run this project locally, follow these steps:

**1. Clone the repository**
```bash
git clone [https://github.com/MohamedNihmath18/Cross-Market-Analytics.git] 
cd Cross-Market-Analytics