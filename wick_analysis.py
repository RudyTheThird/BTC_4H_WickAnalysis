"""
📌 Task 2025-01-03_04:17__SM32
Date: 03 Jan 2025 04:17
Priority: 900

Description:
This script analyzes Bitcoin 4-hour candlestick data to quantify wick retracement patterns.
It calculates the percentage of wicks exceeding 1% of the candle body retraced within the next 3 candles.
Separate analysis is conducted for upper and lower wicks, with statistical significance tests applied.
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Load dataset
data_path = 'btc_4h_candles.csv'
df = pd.read_csv(data_path)
df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime', inplace=True)

# Analyze wicks
def analyze_wicks(df):
    results = {
        'upper_wick_retraced': 0,
        'lower_wick_retraced': 0,
        'upper_wick_total': 0,
        'lower_wick_total': 0
    }
    for i in range(len(df) - 3):
        row = df.iloc[i]
        body = abs(row['close'] - row['open'])
        if body == 0:
            body = row['high'] - row['low']
        
        upper_wick = row['high'] - max(row['close'], row['open'])
        lower_wick = min(row['close'], row['open']) - row['low']
        
        if body > 0:
            if (upper_wick / body) > 0.01:
                results['upper_wick_total'] += 1
                retraced = any(df.iloc[i + j]['high'] >= row['high'] for j in range(1, 4))
                if retraced:
                    results['upper_wick_retraced'] += 1
            
            if (lower_wick / body) > 0.01:
                results['lower_wick_total'] += 1
                retraced = any(df.iloc[i + j]['low'] <= row['low'] for j in range(1, 4))
                if retraced:
                    results['lower_wick_retraced'] += 1
    
    return results

# Perform statistical tests
def perform_statistical_tests(results):
    contingency = [
        [results['upper_wick_retraced'], results['upper_wick_total'] - results['upper_wick_retraced']],
        [results['lower_wick_retraced'], results['lower_wick_total'] - results['lower_wick_retraced']]
    ]
    chi2, p, _, _ = chi2_contingency(contingency)
    return chi2, p

# Visualization
def visualize_results(results):
    labels = ['Upper Wick Retraced', 'Upper Wick Not Retraced', 'Lower Wick Retraced', 'Lower Wick Not Retraced']
    sizes = [
        results['upper_wick_retraced'], results['upper_wick_total'] - results['upper_wick_retraced'],
        results['lower_wick_retraced'], results['lower_wick_total'] - results['lower_wick_retraced']
    ]
    colors = ['#66b3ff', '#ffcc99', '#99ff99', '#ff9999']
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, sizes, color=colors)
    plt.title('Wick Retracement Analysis')
    plt.ylabel('Number of Occurrences')
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig('wick_retracement_chart.png')
    plt.show()

# Main Execution
if __name__ == '__main__':
    results = analyze_wicks(df)
    chi2, p = perform_statistical_tests(results)
    print("Analysis Results:")
    print(results)
    print(f"Chi-Squared Test Statistic: {chi2:.4f}, P-Value: {p:.4f}")
    visualize_results(results)
