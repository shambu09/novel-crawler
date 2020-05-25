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
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'
        }
        self.url = url
        self.paths = node
        self.issueTracker = Issues(None, None, None, None)
        self.prevLink = None
        self.nextLink = None
        self.nextTemp = None
        self.issueTracker.net = True
        self.response = None

    def get_response(self):
        try:
            self.response = requests.get(self.url,
                                         headers=self.headers).content
            self.issueTracker.net = True
        except Exception:
            pass

    def parse(self, link=None):
        if link is not None:
            self.url = link

        self.issueTracker.curr = self.url
        self.issueTracker.validate_links(self.allowed_domains[0])

        if not self.issueTracker.end:
            self.get_response()
            self.issueTracker.validate_response(self.response)
            # converting html to some delicious soup!
            if self.issueTracker.net:
                soup = BeautifulSoup(self.response, "html.parser")

                for s in soup.select('script'):
                    s = s.extract()

                self.prevLink = soup.select("#pt_prev")
                self.prevLink = self.prevLink[0]["href"]
                self.prevLink = requests.compat.urljoin(
                    self.url, self.prevLink)

                self.nextLink = soup.select("#pt_next")
                self.nextLink = self.nextLink[0]["href"]
                self.nextLink = requests.compat.urljoin(
                    self.url, self.nextLink)

                text = soup.find_all(id="chaptercontent")[0].text
                title = soup.find_all("span", class_="title")[0].text
                text = sub(text)
                text = title + text

                self.issueTracker.prev = self.prevLink
                self.issueTracker.next = self.nextLink
                self.issueTracker.text = text
                self.issueTracker.validate_text()

        save_text(self.paths.curr, self.url)
        save_text(self.paths.text, self.issueTracker.text)
        save_text(self.paths.next, self.issueTracker.next)
        save_text(self.paths.prev, self.issueTracker.prev)
