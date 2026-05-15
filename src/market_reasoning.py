import pandas as pd


def generate_market_insight(row):
    """
    Generate human-readable insight for a single stock-day.
    """
    sentiment = row.get("avg_sentiment_score", 0)
    daily_return = row.get("daily_return", 0)
    news_count = row.get("news_count", 0)

    ticker = row.get("ticker", "UNKNOWN")

    if news_count == 0:
        return f"{ticker}: No significant news coverage. Price movement driven by market factors."

    if daily_return > 0.02 and sentiment > 0:
        return f"{ticker}: Strong upward movement backed by positive sentiment across {news_count} news articles."

    elif daily_return < -0.02 and sentiment < 0:
        return f"{ticker}: Decline aligned with negative sentiment observed in {news_count} news articles."

    elif daily_return > 0 and sentiment <= 0:
        return f"{ticker}: Price increased despite weak or neutral sentiment signals."

    elif daily_return < 0 and sentiment >= 0:
        return f"{ticker}: Price dropped even though sentiment remained neutral or positive."

    else:
        return f"{ticker}: Mixed signals with no clear directional trend."

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

    result_df["confidence_score"] = result_df.apply(
    calculate_confidence_score,
    axis=1
    )

    result_df["risk_classification"] = result_df.apply(
        classify_risk,
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

def calculate_confidence_score(row):
    """
    Calculate confidence score for recommendation.
    """
    sentiment = abs(row.get("avg_sentiment_score", 0))
    daily_return = abs(row.get("daily_return", 0))
    news_count = row.get("news_count", 0)

    confidence = 0

    confidence += min(sentiment * 30, 30)
    confidence += min(daily_return * 1000, 40)
    confidence += min(news_count * 10, 30)

    return round(confidence, 2)

def classify_risk(row):
    """
    Classify risk based on volatility proxy and sentiment uncertainty.
    """
    daily_return = abs(row.get("daily_return", 0))
    sentiment = abs(row.get("avg_sentiment_score", 0))
    news_count = row.get("news_count", 0)

    if daily_return > 0.04 and news_count <= 1:
        return "HIGH_RISK"

    elif daily_return > 0.02 or sentiment < 0.2:
        return "MEDIUM_RISK"

    else:
        return "LOW_RISK"