# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
try:
    from blocks import *
except Exception:
    from .blocks import *


class NovelsCrawlSpider:
    name = 'novels_crawl'
    allowed_domains = ['m.wuxiaworld.co']

    def __init__(self, node, url=None):
        self.nextLink = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        self.url = url
        self.prevLink = None
        self.paths = node

    def get_response(self):
        self.response = requests.get(self.url, headers=self.headers).content

    def parse(self, link=None):
        if link is not None:
            self.url = link

        self.get_response()

        # converting html to some delicious soup!
        soup = BeautifulSoup(self.response, "html.parser")

        for s in soup.select('script'):
            s = s.extract()

        text = soup.find_all(id="chaptercontent")[0].text

        title = soup.find_all("span", class_="title")[0].text

        prevLink = soup.select("#pt_prev")
        prevLink = prevLink[0]["href"]
        prevLink = requests.compat.urljoin(self.url, prevLink)
        save_text(self.paths.prev, prevLink)

        nextLink = soup.select("#pt_next")
        nextLink = nextLink[0]["href"]
        nextLink = requests.compat.urljoin(self.url, nextLink)
        save_text(self.paths.next, nextLink)

        text = sub(text)
        text = title + text
        save_text(self.paths.text, text)

        save_text(self.paths.curr, self.url)
