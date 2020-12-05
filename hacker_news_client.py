import requests
import json
import html

class HackerNewsClient:

    URL_MAX_ITEM = "https://hacker-news.firebaseio.com/v0/maxitem.json"
    URL_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"

    @staticmethod
    def getMaxItem():
        return int(requests.get(HackerNewsClient.URL_MAX_ITEM).text)

    @staticmethod
    def getItem(itemId):
        response = json.loads(requests.get(HackerNewsClient.URL_ITEM.format(itemId)).text)
        return HackerNewsItem(**response)

class HackerNewsItem:

    def __init__(self, id=None, deleted=None, type=None, by=None, time=None, text=None,
            dead=None, parent=None, poll=None, kids=None, url=None, score=None,
            title=None, parts=None, descendants=None):
        self.id = id
        self.deleted = deleted
        self.type = type
        self.by = by
        self.time = time 
        self.text = html.unescape(text) if text != None else None
        self.dead = dead
        self.parent = parent
        self.poll = poll
        self.kids = kids
        self.url = url
        self.score = score
        self.title = title
        self.parts = parts
        self.descendants= descendants

    def __str__(self):
        return "<{}, id = {} by {}>".format(self.type, self.id, self.by)
