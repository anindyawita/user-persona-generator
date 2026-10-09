from fastapi import FastAPI

from ..collection.app_reviews.scraper_appstore import search_reviews as search_appstore
from ..collection.app_reviews.scraper_playstore import search_reviews as search_playstore
from ..collection.news.scraper_news import search_news
from ..collection.twitter.scraper_x import search_tweets

app = FastAPI(title="Persona Generation API")


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/data-collection/twitter")
async def twitter_search(query: str = "student", limit: int = 5):
    results = await search_tweets(query, limit)
    return {"query": query, "limit": limit, "count": len(results), "results": results}


@app.get("/data-collection/news")
def news_search(query: str = "student", limit: int = 5):
    results = search_news(query, limit)
    return {"query": query, "limit": limit, "count": len(results), "results": results}


@app.get("/data-collection/app-reviews/appstore")
def appstore_search(app_id: str, limit: int = 5, country: str = "us"):
    results = search_appstore(app_id, limit, country)
    return {"app_id": app_id, "limit": limit, "count": len(results), "results": results}


@app.get("/data-collection/app-reviews/playstore")
def playstore_search(app_id: str, limit: int = 5):
    results = search_playstore(app_id, limit)
    return {"app_id": app_id, "limit": limit, "count": len(results), "results": results}
