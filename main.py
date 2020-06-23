from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import time
import timeit
from functools import lru_cache

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
}

@lru_cache(2)
def NewsSearchApiReq(q):
    x = requests.get('https://newsapi.org/v2/everything?q='+q+'&apiKey=dd97e3a712ef4d4d9f4465c3a5a2abf7')
    json_response = x.json()
    articles =[ {"headline": x["title"], "link":x["url"], "source": "NewsApi"} for x in json_response['articles']]
    return articles

@lru_cache(2)
def RedditSearchApiReq(q):
    reddit = requests.get('https://www.reddit.com/search.json?q='+q,headers=headers)
    json_response = reddit.json()
    articles =[ {"headline": x['data']['title'], "link":x['data']['url'], "source": "Reddit"} for x in json_response['data']['children']]
    return articles


def NewsApiReq():
    x = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=dd97e3a712ef4d4d9f4465c3a5a2abf7')
    json_response = x.json()
    articles =[ {"headline": x["title"], "link":x["url"], "source": "NewsApi"} for x in json_response['articles']]
    return articles

def RedditApiReq():
    reddit = requests.get('https://www.reddit.com/search.json?q=news',headers=headers)
    json_response = reddit.json()
    articles =[ {"headline": x['data']['title'], "link":x['data']['url'], "source": "Reddit"} for x in json_response['data']['children']]
    return articles



@app.get("/")
async def root(request:Request):
    
    resNewsApi=NewsApiReq()

    resRedditApi=RedditApiReq()

    res= resNewsApi + resRedditApi

    return templates.TemplateResponse("item.html", {"request": request, "items": res})

@app.get("/news")
async def news(request:Request, q: str = ""):

    resNewsApi=NewsSearchApiReq(q)

    resRedditApi=RedditSearchApiReq(q)

    res= resNewsApi + resRedditApi

    return templates.TemplateResponse("item.html", {"request": request, "items": res})
