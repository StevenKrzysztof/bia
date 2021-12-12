# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 17:25:11 2021

@author: Ziyang_Wang
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QSlider

class myVideoSlider(QSlider):
    ClickedValue = pyqtSignal(int)

    def __init__(self, father):
        super().__init__(Qt.Horizontal, father)

    def mousePressEvent(self, QMouseEvent):     
        super().mousePressEvent(QMouseEvent)
        value = QMouseEvent.localPos().x()
        
        value = round(value/self.width()*self.maximum())  # calculate the percentage of volume
        self.ClickedValue.emit(value)
