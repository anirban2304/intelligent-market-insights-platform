import pandas as pd


def generate_market_insight(row):
    """
    Generate human-readable insight for a single stock-day.
    """
    sentiment = row.get("avg_sentiment_score", 0)
    daily_return = row.get("daily_return", 0)
    news_count = row.get("news_count", 0)

    if daily_return > 0 and sentiment > 0:
        return "Positive price movement supported by positive news sentiment."

    elif daily_return < 0 and sentiment < 0:
        return "Negative price movement aligned with negative news sentiment."

    elif daily_return > 0 and sentiment <= 0:
        return "Price increased despite neutral or negative news sentiment."

    elif daily_return < 0 and sentiment >= 0:
        return "Price declined despite neutral or positive news sentiment."

    elif news_count == 0:
        return "No relevant news signal available for this stock on this date."

    else:
        return "Market movement was neutral or inconclusive."


def run_reasoning_engine(df):
    """
    Apply reasoning logic across dataset.
    """
    result_df = df.copy()

    result_df["market_insight"] = result_df.apply(
        generate_market_insight,
        axis=1
    )
    result_df["recommendation_signal"] = result_df.apply(
        generate_recommendation,
        axis=1
    )

    return result_df

def generate_recommendation(row):
    """
    Generate simple recommendation label based on signal strength.
    """
    sentiment = row.get("avg_sentiment_score", 0)
    daily_return = row.get("daily_return", 0)
    news_count = row.get("news_count", 0)

    if daily_return > 0.02 and sentiment > 0 and news_count > 0:
        return "BUY_SIGNAL"

    elif daily_return < -0.02 and sentiment < 0 and news_count > 0:
        return "AVOID_SIGNAL"

    else:
        return "HOLD_SIGNAL"