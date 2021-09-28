from newsapi import NewsApiClient
from eventregistry import *

# NEWS_API_KEY = 'd161fdcfcaed4789989a8e3ead3a5077'
NEWS_API_KEY = 'd0a5be8a25c444c1869232272935370a'  # api cua thanh

CNN = 'cnn'
DEFAULT_SOURCES = CNN


# def getNewsFromSource(source=DEFAULT_SOURCES):
#     articles = []
#     # Init
#     newsapi = NewsApiClient(api_key=NEWS_API_KEY)
#
#     # /v2/top-headlines
#     top_headlines = newsapi.get_top_headlines(sources=source)
#
#     # Extract info from response
#     if top_headlines is not None and top_headlines['status'] == 'ok':
#         articles.extend(top_headlines['articles'])
#     print(articles)
#     return articles


def getNewsFromSource(source):
    er = EventRegistry(apiKey='9f2df3b8-aab4-4d51-ac5a-492f056fd824')
    qStr = """
    {
        "$query": {
            "lang": "vie"
        },
        "$filter": {
            "forceMaxDataTimeWindow": "31",
            "dataType": [
                "news"
            ]
        }
    }
    """
    q = QueryArticlesIter.initWithComplexQuery(qStr)
    # change maxItems to get the number of results that you want
    articles = []
    for article in q.execQuery(er, maxItems=10):
        new_article_format = {'author': article['source']['title'], 'title': article['title'], 'description': article['body'],
                              'url': article['url'], 'urlToImage': article['image'],
                              'publishedAt': article['dateTime'], 'content': article['body'],
                              'source': {}}
        new_article_format['source']['id'] = article['source']['uri']
        new_article_format['source']['name'] = article['source']['title']
        articles.append(new_article_format)
    print(articles)
    return articles


# getNewsVietnamese()
# getNewsFromSource()
