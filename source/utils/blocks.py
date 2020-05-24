import os
import sys
import gc
import re


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


# Some Helper Functions

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
