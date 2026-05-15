# Databricks notebook source
# MAGIC %md
# MAGIC # Stock Prices Ingestion - Bronze Layer

# COMMAND ----------

# Step 1: Imports
import yaml
import os
import yfinance as yf
import pandas as pd

# COMMAND ----------

# Step 2: Load config
config_path = "config/source_stock_prices.yaml"

with open(config_path, "r") as file:
    config = yaml.safe_load(file)

# COMMAND ----------

# Step 3: Extract parameters from config
tickers = config["tickers"]
lookback_period = config["lookback_period"]
interval = config["interval"]
landing_path = config["landing_path"]
bronze_table = config["bronze_table"]

# COMMAND ----------

# Step 4: Fetch data
def fetch_stock_data(tickers, period, interval):
    """
    Fetch stock data from yfinance.
    """
    all_data = []

    for ticker in tickers:
        ticker_df = yf.download(
            ticker,
            period=period,
            interval=interval,
            progress=False
        )

        ticker_df = ticker_df.reset_index()
        ticker_df["ticker"] = ticker

        all_data.append(ticker_df)

    return pd.concat(all_data, ignore_index=True)

# COMMAND ----------

# Step 5: Transform data (to be implemented)
def transform_data(raw_df):
    """
    Standardize column names and schema.
    """
    pass

# COMMAND ----------

# Step 6: Load to Bronze (to be implemented)
def load_to_bronze(df, table_name):
    """
    Write data to Delta Bronze table.
    """
    pass

# COMMAND ----------

# Step 7: Orchestration (main flow)
def run_pipeline():
    raw_data = fetch_stock_data(tickers, lookback_period, interval)
    transformed_data = transform_data(raw_data)
    load_to_bronze(transformed_data, bronze_table)

# COMMAND ----------

#if __name__ == "__main__":
#    run_pipeline()

if __name__ == "__main__":
    data = fetch_stock_data(tickers, lookback_period, interval)
    print(data.head())
    print(data.shape)