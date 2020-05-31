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
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'
        }
        self.url = url
        self.prevLink = None
        self.paths = node
        self.manager = Manager(None, self.url, None, None)
        self.text = None

    def get_response(self):
        try:
            self.response = requests.get(self.url,
                                         headers=self.headers).content
            self.manager.error502 = False

        except requests.exceptions.ConnectionError:
            self.manager.error502 = True
            print("hey")

    def parse(self, link=None):
        if link is not None:
            self.url = link
        self.get_response()

        if not self.manager.error502:

            # converting html to some delicious soup!
            soup = BeautifulSoup(self.response, "html.parser")

            for s in soup.select('script'):
                s = s.extract()

            self.text = soup.find_all(id="chaptercontent")[0].text

            title = soup.find_all("span", class_="title")[0].text

            self.prevLink = soup.select("#pt_prev")
            self.prevLink = self.prevLink[0]["href"]
            self.prevLink = requests.compat.urljoin(self.url, self.prevLink)

            self.nextLink = soup.select("#pt_next")
            self.nextLink = self.nextLink[0]["href"]
            self.nextLink = requests.compat.urljoin(self.url, self.nextLink)

            self.text = sub(self.text)
            self.text = title + self.text

            self.saveFiles(self.prevLink, self.url, self.nextLink, self.text)

        else:
            self.manager.badGateway()
            self.manager.curr = self.url
            save_text(self.paths.text, self.manager.text)

    def saveFiles(self, prev, curr, Next, text):
        save_text(self.paths.prev, prev)
        save_text(self.paths.curr, curr)
        save_text(self.paths.next, Next)
        save_text(self.paths.text, text)
