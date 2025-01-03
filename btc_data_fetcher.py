import pandas as pd
import requests
import time

# Binance API endpoint
url = 'https://api.binance.com/api/v3/klines'

# Parameters for BTC/USDT 4-hour data
params = {
    'symbol': 'BTCUSDT',
    'interval': '4h',
    'limit': 1000  # Maximum allowed per request
}

# Fetch data for the past 2 years
end_time = int(time.time()) * 1000
start_time = end_time - (2 * 365 * 24 * 60 * 60 * 1000)  # Approx. 2 years in ms

all_data = []

while start_time < end_time:
    params['startTime'] = start_time
    response = requests.get(url, params=params)
    data = response.json()
    
    if not data or 'code' in data:
        print(f"API Error or Empty Data: {data}")
        break
    
    df = pd.DataFrame(data, columns=[
        'datetime', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'trades', 'taker_buy_base_asset_volume',
        'taker_buy_quote_asset_volume', 'ignore'
    ])
    
    if df.empty:
        print("No more data returned by API.")
        break
    
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    all_data.append(df)
    
    start_time = int(data[-1][6]) + 1  # Increment start time to avoid overlap

# Combine and save all data
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv('btc_4h_candles.csv', index=False)
    print("Data fetching complete. File saved as 'btc_4h_candles.csv'")
else:
    print("No data fetched. Please check your API parameters or connection.")

