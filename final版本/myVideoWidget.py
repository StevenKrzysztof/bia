# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 17:13:39 2021

@author: Ziyang_Wang
"""
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import *
class myVideoWidget(QVideoWidget):
    doubleClickedItem = pyqtSignal(str)  # double click
    def __init__(self,parent=None):
        super(QVideoWidget,self).__init__(parent)
    def mouseDoubleClickEvent(self,QMouseEvent):     
        self.doubleClickedItem.emit("double clicked")