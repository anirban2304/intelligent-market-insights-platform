import pandas as pd
import os
import sys

sys.path.append("src")

from market_reasoning import run_reasoning_engine

input_path = "data/gold/market_signals/market_signals.csv"
output_path = "data/gold/market_insights/market_insights.csv"

def write_market_insights(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    market_signals = pd.read_csv(input_path)

    market_insights = run_reasoning_engine(market_signals)

    output_file = write_market_insights(
        market_insights,
        output_path
    )

    print("MARKET INSIGHTS FILE WRITTEN:", output_file)
    print(market_insights[["ticker", "trade_date", "market_insight"]].head())