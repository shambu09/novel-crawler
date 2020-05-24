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

    def __init__(self, node, url=None):
        self.allowed_domains = ['https://m.wuxiaworld.co/']
        self.nextLink = None
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'
        }
        self.url = url
        self.prevLink = None
        self.paths = node
        self.issueTracker = Issues(None, None, None, None)

    def get_response(self):
        self.response = requests.get(self.url, headers=self.headers).content

    def parse(self, link=None):
        if link is not None:
            self.url = link

        if not self.issueTracker.end:
            self.get_response()

            # converting html to some delicious soup!
            soup = BeautifulSoup(self.response, "html.parser")

            for s in soup.select('script'):
                s = s.extract()

            prevLink = soup.select("#pt_prev")
            prevLink = prevLink[0]["href"]
            prevLink = requests.compat.urljoin(self.url, prevLink)

            nextLink = soup.select("#pt_next")
            nextLink = nextLink[0]["href"]
            nextLink = requests.compat.urljoin(self.url, nextLink)

            text = soup.find_all(id="chaptercontent")[0].text
            title = soup.find_all("span", class_="title")[0].text
            text = sub(text)
            text = title + text

        self.issueTracker.curr = self.url
        self.issueTracker.prev = prevLink
        self.issueTracker.next = nextLink
        self.issueTracker.text = text
        self.issueTracker.validate_response(self.allowed_domains[0])

        save_text(self.paths.next, nextLink)
        save_text(self.paths.prev, prevLink)
        save_text(self.paths.text, self.issueTracker.text)
        save_text(self.paths.curr, self.url)
