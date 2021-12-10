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

    def set_image(self, img_path):
        """
        open image file
        :param img_path: image file path
        :return:
        """
        img_path = './distribution.jpg'
        self.img = QPixmap(img_path)
        
        self.scaled_img = self.img.scaled(self.size())
        
        #QPixmap('./mask.jpg')
        #QPixmap.scaled(self.size())

    
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
    
    def mouseMoveEvent(self, e):
        """
        mouse move events for the widget
        :param e: QMouseEvent
        :return:
        """
        if self.left_click:
            self.end_pos = e.pos() - self.start_pos
            self.point = self.point + self.end_pos
            self.start_pos = e.pos()
            self.repaint()

    def mousePressEvent(self, e):
        """
        mouse press events for the widget
        :param e: QMouseEvent
        :return:
        """
        if e.button() == Qt.LeftButton:
            self.left_click = True
            self.start_pos = e.pos()

    def mouseReleaseEvent(self, e):
        """
        mouse release events for the widget
        :param e: QMouseEvent
        :return:
        """
        if e.button() == Qt.LeftButton:
            self.left_click = False


class MainDemo(QWidget):
    def __init__(self):
        super(MainDemo, self).__init__()

        self.setWindowTitle("Mask Show")
        self.setFixedSize(600, 600)

        #self.open_file = QPushButton("show")
        #self.open_file.setToolTip("Open the image to view.")
        #self.open_file.clicked.connect(self.open_image)
        #self.open_file.setFixedSize(50, 30)
        

        self.zoom_in = QPushButton("+")
        self.zoom_in.clicked.connect(self.large_click)
        self.zoom_in.setFixedSize(30, 30)
        

        self.zoom_out = QPushButton("-")
        self.zoom_out.clicked.connect(self.small_click)
        self.zoom_out.setFixedSize(30, 30)
        
        

        w = QWidget(self)
        layout = QHBoxLayout()
        #layout.addWidget(self.open_file)
        layout.addWidget(self.zoom_in)
        layout.addWidget(self.zoom_out)
        layout.setAlignment(Qt.AlignLeft)
        w.setLayout(layout)
        w.setFixedSize(550, 50)

        self.box = ImageBox()
        self.box.resize(512, 512)
        
        img_name = ('./distribution.jpg')
        self.box.set_image(img_name)
        self.update()

        layout = QVBoxLayout()
        layout.addWidget(w)
        layout.addWidget(self.box)
        self.setLayout(layout)

    
    def open_image(self):
        """
        select image file and open it
        :return:
        """
        #img_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "*.jpg;;*.png;;*.jpeg")
        img_name = ('./mask.jpg')
        self.box.set_image(img_name)
        self.update()
        
    

    def large_click(self):
        """
        used to enlarge image
        :return:
        """
        if self.box.scale < 2:
            self.box.scale += 0.1
            self.box.adjustSize()
            self.update()

    def small_click(self):
        """
        used to reduce image
        :return:
        """
        if self.box.scale > 0.1:
            self.box.scale -= 0.2
            self.box.adjustSize()
            self.update()