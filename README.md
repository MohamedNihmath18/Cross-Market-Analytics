# 📈 Cross-Market Analytics  
### Crypto vs Oil vs Global Stock Indices  
Built with Python, SQL & Streamlit  

An end-to-end Financial Data Engineering & Analytics platform designed to analyze behavioral relationships between cryptocurrencies, commodities, and global stock indices.

This project investigates whether crypto behaves like “digital gold”, a risk asset, or an independent asset class.

---

## 🎯 Project Objective

Cryptocurrencies are often compared with traditional financial assets — but:

- Does Bitcoin move with the S&P 500?
- Is crypto correlated with oil prices?
- Does Ethereum behave like tech stocks (NASDAQ)?
- How do global indices like NIFTY compare?

This project uncovers:

- Cross-market correlations  
- Volatility comparisons  
- Relative performance analysis  
- Macro-event impact insights  
- SQL-driven financial analytics  

---

## 💼 Business Use Cases

### 📊 Investment Research
- Identify whether crypto markets move with or against traditional markets  
- Evaluate diversification potential  

### ⚠️ Risk Management
- Compare crypto volatility vs stocks and oil  
- Analyze drawdowns during crisis periods  

### 🌍 Macro-Economic Analysis
- Study how global events impact crypto vs traditional assets  
- Understand cross-market reaction patterns  

### 📈 Strategy Testing
- Test hedging ideas (e.g., S&P 500 vs Bitcoin)  
- Identify correlated and non-correlated asset pairs  

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Programming | Python |
| Data Processing | Pandas |
| Database | SQLite (Relational Schema Design) |
| Frontend | Streamlit |
| APIs | CoinGecko API, Yahoo Finance |
| Version Control | Git & GitHub |

---

## 🔄 ETL Pipeline Architecture

This project follows a structured ETL workflow:

### 1️⃣ Extract
- Fetched Top 3 cryptocurrencies by market cap using CoinGecko API (with pagination)
- Retrieved stock index data:
  - ^GSPC (S&P 500)
  - ^IXIC (NASDAQ)
  - ^NSEI (NIFTY 50)
- Collected WTI Crude Oil historical prices (2020–2026)

### 2️⃣ Transform
- Standardized date formats  
- Cleaned missing values  
- Normalized schema structure  
- Prepared relational mapping  

### 3️⃣ Load
Data stored in SQLite tables:

- `cryptocurrencies`
- `crypto_prices`
- `oil_prices`
- `stock_prices`

All automated using Python DB API.

---

## 🗄️ Database Schema
cryptocurrencies (id, name, symbol, market_cap)
crypto_prices (coin_id, date, price)
oil_prices (date, oil_price)
stock_prices (symbol, date, close_price)


Supports:

- Multi-table JOIN queries  
- Time-based aggregations  
- Cross-asset comparisons  
- Analytical SQL queries  

---

## 📊 Streamlit Dashboard Modules

### 🔹 1. Market Explorer
- Date range filters  
- Cross-market comparison table  
- SQL JOIN-based daily snapshot combining:
  - Bitcoin
  - Oil
  - S&P 500
  - NIFTY 50  

---

### 🔹 2. SQL Analytics Runner
Interactive SQL execution inside the app.

Includes 25+ predefined analytical queries such as:

- Highest oil price in last 5 years  
- Bitcoin vs S&P 500 comparison  
- Ethereum vs NASDAQ price trends  
- Multi-market daily price joins  
- Cross-market performance comparisons  

---

### 🔹 3. Top Crypto Deep Dive
- Interactive daily price trend charts  
- Raw dataset exploration  
- Market cap ranking analysis  
- Performance visualization  

---

## 🚀 How to Run Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/MohamedNihmath18/Cross-Market-Analytics.git
cd Cross-Market-Analytics

 ---

### 2️⃣ Create Virtual Environment (Optional but Recommended)

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

### 3️⃣ Install Dependencies

pip install -r requirements.txt

### 4️⃣ Run ETL Pipeline

python data_extraction.py
python database_setup.py

### 5️⃣ Launch Streamlit App

streamlit run app.py

```bash


