# Databricks notebook source
# MAGIC %md
# MAGIC # Financial News Ingestion - Bronze Layer

# COMMAND ----------

import yaml
import os
import pandas as pd
from datetime import datetime

# COMMAND ----------

config_path = "config/source_news.yaml"

with open(config_path, "r") as file:
    config = yaml.safe_load(file)

# COMMAND ----------

def read_news_data(input_path):
    """
    Read financial news data from local CSV.
    """
    return pd.read_csv(input_path)

def transform_news_data(raw_df):
    """
    Standardize and clean news data.
    """
    df = raw_df.copy()

    # Standardize column names (safety step)
    df.columns = [col.strip().lower() for col in df.columns]

    # Rename for consistency
    df = df.rename(columns={
        "publish_date": "publish_date",
        "title": "title",
        "content": "content",
        "ticker": "ticker",
        "source": "source",
        "news_id": "news_id"
    })

    # Convert date
    df["publish_date"] = pd.to_datetime(df["publish_date"], errors="coerce")

    # Clean text fields
    df["title"] = df["title"].astype(str).str.strip()
    df["content"] = df["content"].astype(str).str.strip()

    # Normalize ticker
    df["ticker"] = df["ticker"].str.upper().str.strip()

    return df

def apply_news_quality_checks(df, config):
    """
    Apply data quality rules from config to news data.
    """
    rules = config.get("data_quality_rules", [])

    valid_df = df.copy()
    failed_df = pd.DataFrame()

    for rule in rules:
        column = rule["column"]
        rule_type = rule["rule"]

        if rule_type == "not_null":
            failed = valid_df[valid_df[column].isnull() | (valid_df[column] == "")]
            valid_df = valid_df[~(valid_df[column].isnull() | (valid_df[column] == ""))]

        else:
            continue

        failed["failed_rule"] = f"{column}_{rule_type}"
        failed_df = pd.concat([failed_df, failed], ignore_index=True)

    return valid_df, failed_df

def write_news_to_bronze(df, output_path):
    """
    Write news data to Bronze layer locally.
    """
    os.makedirs(output_path, exist_ok=True)

    output_file = os.path.join(output_path, "news_bronze.csv")
    df.to_csv(output_file, index=False)

    return output_file

def add_sentiment_score(df):
    """
    Simple rule-based sentiment scoring (no external dependencies).
    """
    positive_words = ["rise", "growth", "surge", "gain", "strong", "positive"]
    negative_words = ["drop", "fall", "decline", "weak", "loss", "pressure"]

    scores = []

    for text in df["content"]:
        text_lower = str(text).lower()

        score = 0

        for word in positive_words:
            if word in text_lower:
                score += 1

        for word in negative_words:
            if word in text_lower:
                score -= 1

        scores.append(score)

    df["sentiment_score"] = scores

    return df

def write_news_to_silver(df, output_path):
    """
    Write sentiment-enriched news data to Silver layer locally.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path

def create_news_audit_log(source_name, total_records, clean_records, failed_records):
    """
    Create audit log for news ingestion.
    """
    audit = {
        "source_name": source_name,
        "run_timestamp": datetime.utcnow(),
        "total_records": total_records,
        "clean_records": clean_records,
        "failed_records": failed_records,
        "status": "SUCCESS" if failed_records == 0 else "PARTIAL_SUCCESS"
    }

    return audit

if __name__ == "__main__":
    raw_news = read_news_data(config["landing_path"] + "news_sample.csv")

    transformed_news = transform_news_data(raw_news)

    clean_news, failed_news = apply_news_quality_checks(transformed_news, config)
    sentiment_news = add_sentiment_score(clean_news)

    silver_file = write_news_to_silver(
    sentiment_news,
    config["silver_local_path"]
)

    print("NEWS SILVER FILE WRITTEN:", silver_file)

    print(sentiment_news[["title", "sentiment_score"]].head())

    audit_log = create_news_audit_log(
        source_name=config["source_name"],
        total_records=len(transformed_news),
        clean_records=len(clean_news),
        failed_records=len(failed_news)
    )

    print("AUDIT LOG:", audit_log)

    output_file = write_news_to_bronze(
        clean_news,
        config["landing_path"]
    )

    print("NEWS BRONZE FILE WRITTEN:", output_file)