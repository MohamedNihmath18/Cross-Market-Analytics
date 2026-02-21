-- ==========================================
-- 1️⃣ CRYPTOCURRENCIES
-- ==========================================

-- 1. Find the top 3 cryptocurrencies by market cap.
SELECT id, symbol, name, market_cap 
FROM cryptocurrencies 
ORDER BY market_cap DESC 
LIMIT 3;

-- 2. List all coins where circulating supply exceeds 90% of total supply.
SELECT name, circulating_supply, total_supply 
FROM cryptocurrencies 
WHERE total_supply IS NOT NULL 
  AND total_supply > 0 
  AND circulating_supply > (0.90 * total_supply);

-- 3. Get coins that are within 10% of their all-time-high (ATH).
SELECT name, current_price, ath 
FROM cryptocurrencies 
WHERE current_price >= (0.90 * ath);

-- 4. Find the average market cap rank of coins with volume above $1B.
SELECT AVG(market_cap_rank) as avg_rank_high_volume 
FROM cryptocurrencies 
WHERE total_volume > 1000000000;

-- 5. Get the most recently updated coin.
SELECT name, last_updated 
FROM cryptocurrencies 
ORDER BY last_updated DESC 
LIMIT 1;


-- ==========================================
-- 2️⃣ CRYPTO_PRICES (Daily prices of top coins)
-- ==========================================

-- 1. Find the highest daily price of Bitcoin in the last 365 days.
SELECT MAX(price_usd) as highest_btc_price_1yr 
FROM crypto_prices 
WHERE coin_id = 'bitcoin' 
  AND date >= date('now', '-365 days'); 
  -- Note: If running on static older data, remove the date filter to just get MAX overall.

-- 2. Calculate the average daily price of Ethereum in the past 1 year.
SELECT AVG(price_usd) as avg_eth_price_1yr 
FROM crypto_prices 
WHERE coin_id = 'ethereum';

-- 3. Show the daily price trend of Bitcoin in January 2025.
SELECT date, price_usd 
FROM crypto_prices 
WHERE coin_id = 'bitcoin' 
  AND date BETWEEN '2025-01-01' AND '2025-01-31' 
ORDER BY date;

-- 4. Find the coin with the highest average price over 1 year.
SELECT coin_id, AVG(price_usd) as avg_price 
FROM crypto_prices 
GROUP BY coin_id 
ORDER BY avg_price DESC 
LIMIT 1;

-- 5. Get the % change in Bitcoin’s price between Sep 2024 and Sep 2025.
-- Using Common Table Expressions (CTEs) to isolate the months.
WITH 
  sep2024 AS (SELECT AVG(price_usd) as p_start FROM crypto_prices WHERE coin_id = 'bitcoin' AND strftime('%Y-%m', date) = '2024-09'),
  sep2025 AS (SELECT AVG(price_usd) as p_end FROM crypto_prices WHERE coin_id = 'bitcoin' AND strftime('%Y-%m', date) = '2025-09')
SELECT 
  ((p_end - p_start) / p_start) * 100 as btc_percentage_change 
FROM sep2024, sep2025;


-- ==========================================
-- 3️⃣ OIL_PRICES
-- ==========================================

-- 1. Find the highest oil price in the last 5 years.
SELECT MAX(price_usd) as max_oil_price_5yrs 
FROM oil_prices 
WHERE date >= '2021-01-01';

-- 2. Get the average oil price per year.
SELECT strftime('%Y', date) as year, AVG(price_usd) as avg_oil_price 
FROM oil_prices 
GROUP BY year 
ORDER BY year;

-- 3. Show oil prices during COVID crash (March–April 2020).
SELECT date, price_usd 
FROM oil_prices 
WHERE date BETWEEN '2020-03-01' AND '2020-04-30' 
ORDER BY date;

-- 4. Find the lowest price of oil in the last 10 years.
SELECT MIN(price_usd) as min_oil_price 
FROM oil_prices;

-- 5. Calculate the volatility of oil prices (max-min difference per year).
SELECT strftime('%Y', date) as year, 
       (MAX(price_usd) - MIN(price_usd)) as price_volatility 
FROM oil_prices 
GROUP BY year 
ORDER BY year;


-- ==========================================
-- 4️⃣ STOCK_PRICES
-- ==========================================

-- 1. Get all stock prices for a given ticker (e.g., S&P 500).
SELECT date, open, high, low, close, volume 
FROM stock_prices 
WHERE ticker = '^GSPC' 
ORDER BY date DESC;

-- 2. Find the highest closing price for NASDAQ (^IXIC).
SELECT MAX(close) as highest_nasdaq_close 
FROM stock_prices 
WHERE ticker = '^IXIC';

-- 3. List top 5 days with highest price difference (high - low) for S&P 500 (^GSPC).
SELECT date, (high - low) as daily_volatility 
FROM stock_prices 
WHERE ticker = '^GSPC' 
ORDER BY daily_volatility DESC 
LIMIT 5;

-- 4. Get monthly average closing price for each ticker.
SELECT ticker, strftime('%Y-%m', date) as month, AVG(close) as avg_monthly_close 
FROM stock_prices 
GROUP BY ticker, month 
ORDER BY ticker, month;

-- 5. Get average trading volume of NSEI in 2024.
SELECT AVG(volume) as avg_nsei_volume_2024 
FROM stock_prices 
WHERE ticker = '^NSEI' 
  AND strftime('%Y', date) = '2024';


-- ==========================================
-- 🔗 JOIN QUERIES (CROSS-MARKET ANALYSIS)
-- ==========================================

-- 1. Compare Bitcoin vs Oil average price in 2025.
SELECT 
    AVG(c.price_usd) as avg_btc_price, 
    AVG(o.price_usd) as avg_oil_price 
FROM crypto_prices c
JOIN oil_prices o ON c.date = o.date
WHERE c.coin_id = 'bitcoin' 
  AND strftime('%Y', c.date) = '2025';

-- 2. Check if Bitcoin moves with S&P 500 (correlation idea).
SELECT c.date, c.price_usd as btc_price, s.close as sp500_close
FROM crypto_prices c
JOIN stock_prices s ON c.date = s.date
WHERE c.coin_id = 'bitcoin' AND s.ticker = '^GSPC'
ORDER BY c.date DESC;

-- 3. Compare Ethereum and NASDAQ daily prices for 2025.
SELECT c.date, c.price_usd as eth_price, s.close as nasdaq_close
FROM crypto_prices c
JOIN stock_prices s ON c.date = s.date
WHERE c.coin_id = 'ethereum' 
  AND s.ticker = '^IXIC' 
  AND strftime('%Y', c.date) = '2025'
ORDER BY c.date;

-- 4. Find days when oil price spiked (top 10 highest days) and compare with Bitcoin price.
SELECT o.date, o.price_usd as oil_price, c.price_usd as btc_price
FROM oil_prices o
LEFT JOIN crypto_prices c ON o.date = c.date AND c.coin_id = 'bitcoin'
ORDER BY o.price_usd DESC 
LIMIT 10;

-- 5. Compare top 3 coins daily price trend vs Nifty (^NSEI).
SELECT c.date, c.coin_id, c.price_usd as crypto_price, s.close as nifty_close
FROM crypto_prices c
JOIN stock_prices s ON c.date = s.date
WHERE s.ticker = '^NSEI'
ORDER BY c.date DESC;

-- 6. Compare stock prices (^GSPC) with crude oil prices on the same dates.
SELECT s.date, s.close as sp500_close, o.price_usd as oil_price 
FROM stock_prices s
JOIN oil_prices o ON s.date = o.date
WHERE s.ticker = '^GSPC'
ORDER BY s.date DESC;

-- 7. Correlate Bitcoin closing price with crude oil closing price (same date).
SELECT c.date, c.price_usd as btc_price, o.price_usd as oil_price
FROM crypto_prices c
JOIN oil_prices o ON c.date = o.date
WHERE c.coin_id = 'bitcoin'
ORDER BY c.date DESC;

-- 8. Compare NASDAQ (^IXIC) with Ethereum price trends.
SELECT s.date, s.close as nasdaq_close, c.price_usd as eth_price
FROM stock_prices s
JOIN crypto_prices c ON s.date = c.date
WHERE s.ticker = '^IXIC' AND c.coin_id = 'ethereum'
ORDER BY s.date DESC;

-- 9. Join top 3 crypto coins with stock indices for 2025.
SELECT c.date, c.coin_id, c.price_usd, s.ticker, s.close as index_close
FROM crypto_prices c
JOIN stock_prices s ON c.date = s.date
WHERE strftime('%Y', c.date) = '2025'
ORDER BY c.date DESC;

-- 10. Multi-join: stock prices, oil prices, and Bitcoin prices for daily comparison.
SELECT 
    c.date, 
    c.price_usd as btc_price, 
    o.price_usd as oil_price, 
    s.close as sp500_close
FROM crypto_prices c
JOIN oil_prices o ON c.date = o.date
JOIN stock_prices s ON c.date = s.date
WHERE c.coin_id = 'bitcoin' 
  AND s.ticker = '^GSPC'
ORDER BY c.date DESC;