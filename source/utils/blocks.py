import os
import sys
import gc
import re
import requests


class Node:
    def __init__(self, prev, curr, Next, text):
        self.prev = prev
        self.curr = curr
        self.next = Next
        self.text = text


class NodeList:
    def __init__(self):
        self.list = []
        self.tracker = []
        self.threshold = 50

    def add_node(self, node):
        if node.curr not in self.tracker and node.curr is not None:
            self.list.append(node)
            self.tracker.append(node.curr)

    def get_node(self, link):
        return self.list[self.tracker.index(link)]

    def isCached(self, link):
        return link in self.tracker

    def garbage_collect(self):
        if len(self.tracker) > self.threshold + 1:
            self.tracker.pop(0)
            self.list.pop(0)
            gc.collect()

    def clear_all(self):
        self.tracker = []
        self.list = []
        gc.collect()


class Issues(Node):
    def __init__(self, prev, curr, Next, text):
        Node.__init__(self, prev, curr, Next, text)
        self.end = False

    def get_base(self, url):
        _ = requests.compat.urljoin(url, '.')
        if _ == url: return "end"
        return requests.compat.urljoin(_, '/.')

    def validate_response(self, base):
        if self.get_base(self.curr) != base:
            self.text = "Invalid link, Try again with a valid link."
            self.end = True

        elif self.get_base(self.prev) == "end":
            self.text = self.text + "\n\n\nSorry there is no previous chapter or the previous chapter is broken :(\nPress Next to continue reading."
            self.end = True

        elif self.get_base(self.next) == "end":
            self.text = self.text + "\n\n\nSorry there is no next chapter(yet?) or the next chapter is broken!\nTry going back :("
            self.end = True

        elif self.text == '' or self.text is None or len(self.text) <= 100:
            self.text = "The Link is broken :(\nTry again with a valid link."
            self.end = True

        else:
            self.end = False


#Some Helper Functions
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def sub(text):
    en = str(text)
    s = re.sub("\n([ ]|[\n])*\n", "\n\n", en)
    return s


def save_text(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def save_bin(path, content):
    with open(path, 'wb') as f:
        f.write(content)


def open_text(path):
    with open(path, 'r') as f:
        temp = f.read()

    return temp
