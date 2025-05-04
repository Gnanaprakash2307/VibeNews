import requests

API_KEY = "news-api-key"

def fetch_news(query):
    url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&q={query}&language=en"
    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("results", [])
        if not articles:
            return "No news articles found."

        news_text = "\n\n".join(
            [f"Title: {a['title']}\nDescription: {a['description']}" for a in articles[:3]]
        )
        return news_text

    except Exception as e:
        return f"Error fetching news: {e}"
