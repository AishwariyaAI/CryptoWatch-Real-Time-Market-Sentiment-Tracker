from newsapi import NewsApiClient
import pandas as pd

API_KEY = "f354618a4b0446d9a0d6a567f895e7d1"

newsapi = NewsApiClient(api_key=API_KEY)

def fetch_news(coin):

    articles = newsapi.get_everything(
        q=f"{coin} cryptocurrency OR blockchain",
        language='en',
        sort_by='publishedAt',
        page_size=20
    )

    news_data = []

    for article in articles['articles']:
        news_data.append({
            "title": article['title'],
            "description": article['description']
        })

    return pd.DataFrame(news_data)