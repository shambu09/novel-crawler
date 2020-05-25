import os
import sys
import gc

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

from utils import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.h, self.w = 1000, 800
        self.setWindowIcon(QIcon(resource_path(r'temp\icon.ico')))
        self.resize(self.h, self.w)

        layout = QVBoxLayout()
        self.editor = QPlainTextEdit()
        self.editor.setReadOnly(True)

        self.text_path = resource_path(r"temp\pmet.cus")
        self.prev_path = resource_path(r"temp\verp.cus")
        self.link_path = resource_path(r"temp\knil.cus")
        self.next_path = resource_path(r"temp\txen.cus")

        self.paths = Node(self.prev_path, self.link_path, self.next_path,
                          self.text_path)
        self.crawler = NovelsCrawlSpider(self.paths)
        self.cache = NodeList()
        self.cache.threshold = 40
        self.temp_node = None
        self.clearDummy = ''
        self.crawler.issueTracker.is_next = False
        self.crawler.issueTracker.is_prev = False

        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        self.link = None
        self.prev = None
        self.next = None

        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        file_toolbar = QToolBar("Options")
        file_toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&Options")

        clear_action = QAction("Clear...", self)
        clear_action.setStatusTip("Clear Current Chapter")
        clear_action.triggered.connect(self.file_clear)
        file_menu.addAction(clear_action)
        file_toolbar.addAction(clear_action)

        print_action = QAction("Print...", self)
        print_action.setStatusTip("Print Current Page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        open_file_action = QAction("Open Link...", self)
        open_file_action.setStatusTip("Open Link")
        open_file_action.triggered.connect(self.takeinputs)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        prev_file_action = QAction("Previous...", self)
        prev_file_action.setStatusTip("Previous Chapter")
        prev_file_action.triggered.connect(self.prev_change)
        file_menu.addAction(prev_file_action)
        file_toolbar.addAction(prev_file_action)

        next_file_action = QAction("Next...", self)
        next_file_action.setStatusTip("Next Chapter")
        next_file_action.triggered.connect(self.next_change)
        file_menu.addAction(next_file_action)
        file_toolbar.addAction(next_file_action)

        self.file_open()
        self.show()

    def takeinputs(self):
        self.crawler.issueTracker.temp = self.link
        self.crawler.issueTracker.is_next = False
        self.crawler.issueTracker.is_prev = False
        link, done = QInputDialog.getText(
            self, 'Input Dialog',
            'Enter your link:                                                                '
        )

        if done:
            self.link = link
            self.crawler.parse(self.link)
            save_text(resource_path(r"temp\knil.cus"), self.link)
            self.file_open()

    def next_change(self):
        self.crawler.issueTracker.is_next = True
        self.crawler.issueTracker.is_prev = False
        self.crawler.issueTracker.nextTemp = self.link
        if self.cache.isCached(self.next):
            self.temp_node = self.cache.get_node(self.next)
            self.put_links(self.temp_node)

        else:
            if self.next != "":
                self.crawler.parse(self.next)

        self.file_open()

    def prev_change(self):
        self.crawler.issueTracker.is_next = False
        self.crawler.issueTracker.is_prev = True
        self.crawler.issueTracker.prevTemp = self.link
        if self.cache.isCached(self.prev):
            self.temp_node = self.cache.get_node(self.prev)
            self.put_links(self.temp_node)

        else:
            if self.prev != "":
                self.crawler.parse(self.prev)

        self.file_open()

    def put_links(self, node):
        save_text(self.text_path, node.text)
        save_text(self.prev_path, node.prev)
        save_text(self.link_path, node.curr)
        save_text(self.next_path, node.next)

    def get_links(self):
        self.prev = open_text(self.prev_path)
        self.link = open_text(self.link_path)
        self.next = open_text(self.next_path)

    def file_clear(self):
        save_text(self.text_path, self.clearDummy)
        save_text(self.prev_path, self.clearDummy)
        save_text(self.link_path, self.clearDummy)
        save_text(self.next_path, self.clearDummy)
        self.file_open()
        self.cache.clear_all()

    def file_open(self):
        with open(self.text_path, "r", encoding="utf-8") as f:
            text = f.read()

        self.editor.setPlainText(text)
        self.get_links()

        self.cache.garbage_collect()

        self.cache.add_node(Node(self.prev, self.link, self.next, text))

        gc.collect()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())


app = QApplication(sys.argv)
app.setApplicationName("")
window = MainWindow()
window.showMaximized()
app.exec_()
window.cache.clear_all()
