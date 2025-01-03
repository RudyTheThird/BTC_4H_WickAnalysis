import pandas as pd
import requests
import time

# CoinGecko API endpoint
url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'

# Parameters for BTC/USDT data
params = {
    'vs_currency': 'usd',
    'days': '365',  # Approx. 1 year
    'interval': 'daily'  # Use daily if hourly is unavailable
}

# Fetch data from CoinGecko
response = requests.get(url, params=params)
print(f"HTTP Status Code: {response.status_code}")

try:
    data = response.json()
    print("API Response Sample:")
    print(data)  # Print the response for debugging

    if 'prices' not in data:
        raise KeyError("'prices' key not found in API response")

    # Process data
    timestamps = [entry[0] for entry in data['prices']]
    prices = [entry[1] for entry in data['prices']]
    highs = [entry[1] * 1.01 for entry in data['prices']]  # Mock high (as CoinGecko lacks OHLC for daily)
    lows = [entry[1] * 0.99 for entry in data['prices']]  # Mock low
    volumes = [entry[1] * 0.1 for entry in data['prices']]  # Mock volume

    df = pd.DataFrame({
        'datetime': pd.to_datetime(timestamps, unit='ms'),
        'open': prices,
        'high': highs,
        'low': lows,
        'close': prices,
        'volume': volumes
    })

    # Resample to 4-hour intervals
    df = df.resample('4H', on='datetime').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()

    # Save to CSV
    df.to_csv('btc_4h_candles.csv', index=True)
    print("Data fetching complete. File saved as 'btc_4h_candles.csv'")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

except KeyError as e:
    print(f"Key Error: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
