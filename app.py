import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import requests
import matplotlib.pyplot as plt


from services.predictor import market_prediction
from services.summarizer import summarize_news
from services.crypto_prices import get_crypto_prices
from streamlit_autorefresh import st_autorefresh
from wordcloud import WordCloud


def get_fear_greed():

    try:

        data = requests.get(
            "https://api.alternative.me/fng/"
        ).json()

        return (
            data["data"][0]["value"],
            data["data"][0]["value_classification"]
        )

    except:

        return "N/A", "Unavailable"

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="CryptoWatch",
    page_icon="🚀",
    layout="wide"
)

# ----------------------------------
# AUTO REFRESH
# ----------------------------------

st_autorefresh(
    interval=300000,
    key="crypto_refresh"
)

# ----------------------------------
# COIN SELECTOR
# ----------------------------------

coin = st.selectbox(
    "Select Cryptocurrency",
    ["Bitcoin", "Ethereum", "Solana"]
)

# ----------------------------------
# LOAD DATA
# ----------------------------------

df, trend, score = market_prediction(coin)
if df.empty:
    st.warning("No news available.")
    st.stop()

btc_price, eth_price = get_crypto_prices()

# ----------------------------------
# SIDEBAR
# ----------------------------------

with st.sidebar:

    st.header("🚀 CryptoWatch")

    st.write(
        "Real-Time Crypto Market Intelligence"
    )

    st.write(
        "Powered by NewsAPI + Groq + NLP"
    )

    st.divider()

    st.write(
        f"Selected Coin: {coin}"
    )
st.sidebar.subheader("News Filter")

filter_option = st.sidebar.selectbox(
    "Sentiment",
    ["All", "POSITIVE", "NEGATIVE"]
)

if filter_option != "All":
    df = df[df["sentiment"] == filter_option]
# ----------------------------------
# HEADER
# ----------------------------------

st.title("🚀 CryptoWatch")

st.caption(
    "Real-Time Cryptocurrency Market Sentiment Tracker"
)

# ----------------------------------
# METRIC CARDS
# ----------------------------------

positive_pct = round(
    (df["sentiment"] == "POSITIVE").mean() * 100,
    1
)

negative_pct = round(
    (df["sentiment"] == "NEGATIVE").mean() * 100,
    1
)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("₿ Bitcoin", f"${btc_price:,.0f}")

with col2:
    st.metric("Ξ Ethereum", f"${eth_price:,.0f}")

with col3:
    st.metric("Trend", trend)

with col4:
    st.metric("Score", round(score, 2))

with col5:
    st.metric("Positive %", f"{positive_pct}%")

with col6:
    st.metric("Negative %", f"{negative_pct}%")

fear_value, fear_label = get_fear_greed()

# KPI SECTION
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📰 Articles", len(df))

with col2:
    st.metric("😨 Fear & Greed", fear_value)

with col3:
    st.metric("📈 Trend", trend)

with col4:
    st.metric("💡 Recommendation",
              "BUY" if score > 0.3
              else "SELL" if score < -0.3
              else "HOLD")


st.subheader("😨 Fear & Greed Index")

st.info(
    f"{fear_value} - {fear_label}"
)

st.divider()
st.subheader("🎯 Market Sentiment Gauge")

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Sentiment Score"},
        gauge={
            "axis": {"range": [-1, 1]},
            "bar": {"color": "lightgreen"}
        }
    )
)

st.plotly_chart(
    gauge,
    use_container_width=True
)

# ----------------------------------
# SENTIMENT PIE CHART
# ----------------------------------

st.subheader("📊 Sentiment Distribution")

sentiment_counts = (
    df["sentiment"]
    .value_counts()
    .reset_index()
)

sentiment_counts.columns = [
    "Sentiment",
    "Count"
]

fig = px.pie(
    sentiment_counts,
    values="Count",
    names="Sentiment",
    hole=0.4,
    title="Crypto News Sentiment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# BITCOIN PRICE CHART
# ----------------------------------

st.subheader("📈 Bitcoin 7-Day Price Trend")

btc = yf.download(
    "BTC-USD",
    period="7d",
    interval="1h"
)

# flatten columns
btc.columns = btc.columns.get_level_values(0)

btc = btc.reset_index()

fig = px.line(
    btc,
    x="Datetime",
    y="Close",
    title="Bitcoin 7-Day Price Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.subheader("📈 Ethereum 7-Day Price Trend")

eth = yf.download(
    "ETH-USD",
    period="7d",
    interval="1h"
)

eth.columns = eth.columns.get_level_values(0)

eth = eth.reset_index()

fig = px.line(
    eth,
    x="Datetime",
    y="Close",
    title="Ethereum 7-Day Price Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("🔥 Top Headlines")

for headline in df["title"].head(5):
    st.info(headline)

st.subheader("📰 Latest Crypto News")

st.dataframe(
    df,
    use_container_width=True
)
# ----------------------------------
# AI SUMMARY
# ----------------------------------

with st.spinner("🤖 Generating AI Market Summary..."):

    combined_text = " ".join(
        df["title"].tolist()
    )

    summary = summarize_news(
        combined_text
    )

st.subheader("🤖 AI Market Summary")

st.success(summary)
st.subheader("☁️ Trending Crypto Topics")

text = " ".join(
    df["title"].astype(str)
)

wordcloud = WordCloud(
    width=1000,
    height=400,
    background_color="white",
    colormap="viridis"
).generate(text)

fig, ax = plt.subplots(
    figsize=(12, 5)
)

ax.imshow(wordcloud)

ax.axis("off")

st.pyplot(fig)

st.subheader("💡 AI Recommendation")

if score > 0.3:

    st.success(
        "BUY / BULLISH\n\nPositive market sentiment detected."
    )

elif score < -0.3:

    st.error(
        "SELL / BEARISH\n\nNegative sentiment dominates."
    )

else:

    st.warning(
        "HOLD / NEUTRAL\n\nMarket sentiment mixed."
    )

st.subheader("📊 Market Status")

if score > 0.3:
    st.success("Bullish Market")

elif score < -0.3:
    st.error("Bearish Market")

else:
    st.warning("Neutral Market")



# ----------------------------------
# DOWNLOAD REPORT
# ----------------------------------

report = f"""
CryptoWatch AI Report
=====================

Coin: {coin}

Market Trend: {trend}

Sentiment Score: {score}

Fear & Greed Index:
{fear_value} - {fear_label}

AI Recommendation:
{"BUY / BULLISH" if score > 0.3 else "SELL / BEARISH" if score < -0.3 else "HOLD / NEUTRAL"}

AI Market Summary:

{summary}
"""

st.download_button(
    label="📥 Download AI Report",
    data=report,
    file_name="crypto_report.txt",
    mime="text/plain"
)

# ----------------------------------
# FOOTER
# ----------------------------------

st.divider()

st.markdown("---")

st.markdown(
"""
### 🚀 CryptoWatch

Real-Time Cryptocurrency Market Intelligence Platform

Features:
- NLP Sentiment Analysis
- Fear & Greed Index
- AI Market Summary
- Bitcoin & Ethereum Tracking
- Word Cloud Analytics
- AI Trading Recommendations

Built using Streamlit, NewsAPI, Transformers, Groq, Plotly and yFinance.
"""
)