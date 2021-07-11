import urllib.request

import requests
from PyQt5.QtWidgets import *
from design import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QScrollArea
import sys, os, cv2
import numpy as np
import pymongo
from pymongo import MongoClient
import re
import urllib.request as urllib2
from urllib.request import Request, urlopen
import webbrowser
import wget
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
class interface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.text=None
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.setupUi(self)
        self.grid = QGridLayout()
        self.ui.label.setLayout(self.grid)
        self.list_img=[]
        self.url_liste=[]
        self.thumbnails_list=[]
        self.ui.pushButton.clicked.connect(self.search)
        #self.create_labels(self.list_img)

    def search(self):
        self.text=self.ui.textEdit.toPlainText()
        self.url_liste=self.get_img_database(self.text)
        #print("sayı:"+str(len(self.url_liste)))
        for link in self.url_liste:
            print(link)
        chrome_path="C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
        #webbrowser.get(chrome_path).open(self.url_liste[0])
        self.thumbnails_list=self.get_thumbnails(self.url_liste)
        for i in self.thumbnails_list:
            print(i)
        if (len(self.text)!=0):
            self.list_img = self.get_img_database(self.text)
            if (len(self.list_img)==0):
                QMessageBox.warning(self, 'Error', 'There is no image about search key')
            else:
                self.create_labels(self.thumbnails_list)
        else:
            QMessageBox.warning(self, 'Error', 'There is no search key')
    def location(self,i):
        y=int(i/4)
        x=int(i%4)
        return x,y
    def get_thumbnails(self,link_liste):
        thumbnail_liste=[]
        for link in link_liste:
            url = link
            id = url.split("=", 1)[1]
            thumbnailurl = 'https://img.youtube.com/vi/' + id + '/maxresdefault.jpg'
            thumbnail_liste.append(thumbnailurl)
        return thumbnail_liste
    def link(self,linkStr):
        QDesktopServices.openUrl(QUrl(linkStr))
    def create_labels(self,list):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)
        for i in range(0, len(list)):
            self.url=list[i]
            self.lbl = QLabel(self)
            self.lbl.setAlignment(Qt.AlignCenter)
            #qp = QtGui.QPainter()
            self.mymap = QPixmap()
            self.data = urllib.request.urlopen(self.url).read()
            #self.data = urllib.request.urlopen(self.url).read()
            self.mymap.loadFromData(self.data)
            self.mymap = self.mymap.scaled(200, 200, QtCore.Qt.KeepAspectRatio, Qt.FastTransformation)
            x, y = self.location(i)
            #qp.drawPixmap(x, y, 200, 200,self.mymap.scaled(200, 200, transformMode=QtCore.Qt.SmoothTransformation))
            self.lbl.setParent(None)
            self.lbl.setPixmap(self.mymap)
            self.cw = QWidget(self)
            self.setCentralWidget(self.cw)
            self.mainlay = QGridLayout(self.cw)
            #self.ui.label.setLayout(self.mainlay)
            self.setLayout(self.mainlay)
            #x, y = self.location(i)
            self.mainlay.addWidget(self.lbl)
            self.lbl.repaint()

            """label1 = QLabel()
            label1.setAlignment(Qt.AlignCenter)
            req = Request(list[i], headers={'User-Agent': 'Mozilla/5.0'})
            url_data = urllib2.urlopen(req).read()
            self.pm = QPixmap()  # .scaled(250, 250, Qt.KeepAspectRatio,Qt.SmoothTransformation)
            self.pm.loadFromData(url_data)
            label1.setPixmap(self.pm)
            x, y = self.location(i)
            self.grid.addWidget(label1, y, x)"""
    def get_img_database(self,key):
        cluster = MongoClient("mongodb+srv://melin:1234@cluster0.9j4nx.mongodb.net/myFirstDatabase?ssl=true&ssl_cert_reqs=CERT_NONE")
        db = cluster["videos"]
        collection = db["videos"]
        regx = re.compile("{}".format(key), re.IGNORECASE)
        collections = collection.find({"captions": regx})
        url_list=[]
        for x in collections:
            #if "https" in x["url"]:
                #if (len(url_list)<20):
            url_list.append(x['video_url'])
        return url_list

app = QtWidgets.QApplication(sys.argv)
window = interface()
window.show()
#sys.exit(app.exec())
app.exec_()
