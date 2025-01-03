# BTC 4H Wick Retracement Analysis

## Overview

This project analyzes Bitcoin's 4-hour candlestick data to quantify wick retracement patterns. The analysis identifies upper and lower wick retracements exceeding 1% of the body and evaluates retracement within the next 3 candles.

## Files

- **btc_data_fetcher_coingecko.py:** Fetches Bitcoin data from the CoinGecko API.
- **wick_analysis.py:** Analyzes wick retracement patterns and performs statistical significance tests.
- **btc_4h_candles.csv:** Dataset containing 4-hour candlestick data.
- **wick_retracement_chart.png:** Visualization of retracement patterns.

## Results

- **Upper Wick Retraced:** 71.1%  
- **Lower Wick Retraced:** 64.2%  
- **Statistical Significance (p-value):** 0.0569  

## Setup

1. Install dependencies:  
   ```bash
   pip install pandas requests matplotlib scipy
