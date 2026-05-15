# Databricks notebook source
# MAGIC %md
# MAGIC # Stock Prices Ingestion - Bronze Layer

# COMMAND ----------

# Step 1: Imports
import yaml
import os
import yfinance as yf
import pandas as pd
from datetime import datetime

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
    all_data = []

    for ticker in tickers:
        ticker_df = yf.Ticker(ticker).history(
            period=lookback_period,
            interval=interval,
            auto_adjust=False
        )

        ticker_df = ticker_df.reset_index()
        ticker_df["ticker"] = ticker

        all_data.append(ticker_df)

    return pd.concat(all_data, ignore_index=True)

# COMMAND ----------

# Step 5: Transform data
def transform_data(raw_df):
    """
    Standardize column names and handle schema variability.
    """
    df = raw_df.copy()

    df = df.rename(columns={
        "Date": "trade_date",
        "Open": "open_price",
        "High": "high_price",
        "Low": "low_price",
        "Close": "close_price",
        "Adj Close": "adjusted_close_price",
        "Volume": "volume"
    })

    # Handle missing adjusted_close_price
    if "adjusted_close_price" not in df.columns:
        df["adjusted_close_price"] = df["close_price"]

    expected_columns = [
        "ticker",
        "trade_date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "adjusted_close_price",
        "volume"
    ]

    df = df[expected_columns]
    df["trade_date"] = pd.to_datetime(df["trade_date"])

    return df


def apply_data_quality_checks(df, config):
    """
    Apply data quality rules from config.
    Returns clean_df and failed_records_df
    """
    rules = config.get("data_quality_rules", [])

    valid_df = df.copy()
    failed_df = pd.DataFrame()

    for rule in rules:
        column = rule["column"]
        rule_type = rule["rule"]

        if rule_type == "not_null":
            failed = valid_df[valid_df[column].isnull()]
            valid_df = valid_df[valid_df[column].notnull()]

        elif rule_type == "greater_than":
            threshold = rule["value"]
            failed = valid_df[valid_df[column] <= threshold]
            valid_df = valid_df[valid_df[column] > threshold]

        elif rule_type == "greater_than_or_equal":
            threshold = rule["value"]
            failed = valid_df[valid_df[column] < threshold]
            valid_df = valid_df[valid_df[column] >= threshold]

        else:
            continue

        failed["failed_rule"] = f"{column}_{rule_type}"
        failed_df = pd.concat([failed_df, failed], ignore_index=True)

    return valid_df, failed_df

def create_audit_log(source_name, total_records, clean_records, failed_records):
    """
    Create audit log for pipeline execution
    """
    audit = {
        "source_name": source_name,
        "run_timestamp": datetime.now(),
        "total_records": total_records,
        "clean_records": clean_records,
        "failed_records": failed_records,
        "status": "SUCCESS" if failed_records == 0 else "PARTIAL_SUCCESS"
    }

    return audit

# COMMAND ----------

# Step 6: Load to Bronze (to be implemented)
def write_to_local_bronze(df, output_path):
    """
    Write clean data locally in a Bronze-like structure.
    """
    os.makedirs(output_path, exist_ok=True)

    output_file = os.path.join(output_path, "stock_prices_bronze.csv")
    df.to_csv(output_file, index=False)

    return output_file

# COMMAND ----------

# Step 7: Orchestration (main flow)
def run_pipeline():
    raw_data = fetch_stock_data(tickers, lookback_period, interval)
    transformed_data = transform_data(raw_data)
    #load_to_bronze(transformed_data, bronze_table)

# COMMAND ----------

#if __name__ == "__main__":
#    run_pipeline()

if __name__ == "__main__":
    raw_data = fetch_stock_data(tickers, lookback_period, interval)
    transformed_data = transform_data(raw_data)

    clean_data, failed_data = apply_data_quality_checks(transformed_data, config)

    audit_log = create_audit_log(
        source_name=config["source_name"],
        total_records=len(transformed_data),
        clean_records=len(clean_data),
        failed_records=len(failed_data)
    )

    print("AUDIT LOG:", audit_log)
    output_file = write_to_local_bronze(
    clean_data,
    config["landing_path"]
)

print("BRONZE FILE WRITTEN:", output_file)