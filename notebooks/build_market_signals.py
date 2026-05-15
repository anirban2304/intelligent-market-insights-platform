import yaml
import pandas as pd
import os

stock_gold_path = "data/gold/stock_prices/stock_prices_gold.csv"
news_silver_path = "data/silver/news/news_silver.csv"
market_signal_output_path = "data/gold/market_signals/market_signals.csv"

def read_input_data(stock_path, news_path):
    """
    Read stock gold data and sentiment-enriched news data.
    """
    stock_df = pd.read_csv(stock_path)
    news_df = pd.read_csv(news_path)

    return stock_df, news_df

def aggregate_news_sentiment(news_df):
    """
    Aggregate sentiment score by ticker and publish date.
    """
    df = news_df.copy()

    df["publish_date"] = pd.to_datetime(df["publish_date"]).dt.date
    df["ticker"] = df["ticker"].str.upper().str.strip()

    sentiment_df = (
        df.groupby(["ticker", "publish_date"])
        .agg(
            avg_sentiment_score=("sentiment_score", "mean"),
            news_count=("news_id", "count")
        )
        .reset_index()
    )

    sentiment_df = sentiment_df.rename(columns={
        "publish_date": "trade_date"
    })

    return sentiment_df

def build_market_signal_dataset(stock_df, sentiment_df):
    """
    Join stock market features with news sentiment features.
    """
    stock = stock_df.copy()

    stock["trade_date"] = pd.to_datetime(stock["trade_date"]).dt.date
    stock["ticker"] = stock["ticker"].str.upper().str.strip()

    market_signals = stock.merge(
        sentiment_df,
        on=["ticker", "trade_date"],
        how="left"
    )

    market_signals["avg_sentiment_score"] = (
        market_signals["avg_sentiment_score"].fillna(0)
    )

    market_signals["news_count"] = (
        market_signals["news_count"].fillna(0).astype(int)
    )

    return market_signals

def write_market_signals(df, output_path):
    """
    Write final market signal dataset locally.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path

if __name__ == "__main__":
    stock_df, news_df = read_input_data(
        stock_gold_path,
        news_silver_path
    )

    sentiment_df = aggregate_news_sentiment(news_df)
    market_signals_df = build_market_signal_dataset(stock_df, sentiment_df)
    print(market_signals_df.head())
    output_file = write_market_signals(
        market_signals_df,
        market_signal_output_path
    )
    print("MARKET SIGNALS FILE WRITTEN:", output_file)