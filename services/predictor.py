from services.news_fetcher import fetch_news
from services.sentiment import analyze_sentiment


def market_prediction(coin):

    df = fetch_news(coin)

    sentiments = []

    for title in df["title"]:

        try:
            sentiment = analyze_sentiment(title)
            sentiments.append(sentiment)

        except Exception:
            sentiments.append("NEUTRAL")

    df["sentiment"] = sentiments

    positive = len(
        df[df["sentiment"] == "POSITIVE"]
    )

    negative = len(
        df[df["sentiment"] == "NEGATIVE"]
    )

    total = len(df)

    score = (positive - negative) / total

    if score > 0.30:
        trend = "🚀 Bullish"

    elif score < -0.30:
        trend = "🔻 Bearish"

    else:
        trend = "⚖️ Neutral"

    return df, trend, score