# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 18:33:00 2021

@author: Ziyang_Wang
"""
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.Qt import QPixmap, QPoint, Qt, QPainter, QIcon
from PyQt5.QtCore import QSize
from PyQt5 import QtGui
import sys
import qtawesome

from PyQt5.QtGui import *


class ImageBox(QWidget):
    def __init__(self):
        super(ImageBox, self).__init__()
        self.img = None
        self.scaled_img = None
        self.point = QPoint(0, 0)
        self.start_pos = None
        self.end_pos = None
        self.left_click = False
        self.scale = 0.5

    def init_ui(self):
        self.setWindowTitle("ImageBox")
#select the mask from the output path and show
    def set_image(self, Maskpath):
        
        Maskpath = './mask.png'
        self.img = QPixmap(Maskpath)
        
        self.scaled_img = self.img.scaled(self.size())
        
        

    
    def paintEvent(self, e):
        """
        receive paint events
        :param e: QPaintEvent
        :return:
        """
        if self.scaled_img:
            painter = QPainter()
            painter.begin(self)
            painter.scale(self.scale, self.scale)
            painter.drawPixmap(self.point, self.scaled_img)
            painter.end()
 
    #action for mouse move
    def mouseMoveEvent(self, e):
      
        if self.left_click:
            self.end_pos = e.pos() - self.start_pos
            self.point = self.point + self.end_pos
            self.start_pos = e.pos()
            self.repaint()
 #action for mouse press
    def mousePressEvent(self, e):
      
        if e.button() == Qt.LeftButton:
            self.left_click = True
            self.start_pos = e.pos()
  #action for mouse release
    def mouseReleaseEvent(self, e):
        
        if e.button() == Qt.LeftButton:
            self.left_click = False

#the app window for show picture and adjust
class MainDemo(QWidget):
    def __init__(self):
        super(MainDemo, self).__init__()

        self.setWindowTitle("Mask Show")
        self.setFixedSize(600, 600)

        
        
        # zoom in and out button
        self.zoom_in = QPushButton("+")
        self.zoom_in.clicked.connect(self.large_click)
        self.zoom_in.setFixedSize(30, 30)
        

        self.zoom_out = QPushButton("-")
        self.zoom_out.clicked.connect(self.small_click)
        self.zoom_out.setFixedSize(30, 30)
        
        

        w = QWidget(self)
        layout = QHBoxLayout()
        
        layout.addWidget(self.zoom_in)
        layout.addWidget(self.zoom_out)
        layout.setAlignment(Qt.AlignLeft)
        w.setLayout(layout)
        w.setFixedSize(550, 50)

        self.box = ImageBox()
        self.box.resize(512, 512)
        
        Maskname = ('./mask.png')
        self.box.set_image(Maskname)
        self.update()

        layout = QVBoxLayout()
        layout.addWidget(w)
        layout.addWidget(self.box)
        self.setLayout(layout)

    #open image from result path
    def open_image(self):
        
        
        Maskname = ('./mask.jpg')
        self.box.set_image(Maskname)
        self.update()
        
    
    #zoom in function
    def large_click(self):
        
        if self.box.scale < 2:
            self.box.scale += 0.1
            self.box.adjustSize()
            self.update()
    #zoom out function
    def small_click(self):
        
        if self.box.scale > 0.1:
            self.box.scale -= 0.2
            self.box.adjustSize()
            self.update()