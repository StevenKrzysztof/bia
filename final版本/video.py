# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 17:29:01 2021

@author: Ziyang_Wang
"""
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from GUI import Ui_MainWindow
from myVideoWidget import myVideoWidget
import sys


class myMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.sld_video_pressed=False  #Judge whether the slider is pressed by mouse
        self.videoFullScreen = False   # 
        self.videoFullScreenWidget = myVideoWidget()   # create a widget
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.wgt_video)  # play video in widget
        self.btn_open.clicked.connect(self.openVideoFile)   # open file
        self.btn_play.clicked.connect(self.playVideo)       # play
        self.btn_stop.clicked.connect(self.pauseVideo)       # pause
        
        self.player.positionChanged.connect(self.changeSlide)      # change Slide
        self.videoFullScreenWidget.doubleClickedItem.connect(self.videoDoubleClicked)  #double click
        self.wgt_video.doubleClickedItem.connect(self.videoDoubleClicked)   
        self.sld_video.setTracking(False)
        self.sld_video.sliderReleased.connect(self.releaseSlider)
        self.sld_video.sliderPressed.connect(self.pressSlider)
        self.sld_video.sliderMoved.connect(self.moveSlider)   # press the slider
        self.sld_video.ClickedValue.connect(self.clickedSlider)  
        self.sld_audio.valueChanged.connect(self.volumeChange)  # voice
        self.btn_cast.hide()

   

    def volumeChange(self, position):
        volume= round(position/self.sld_audio.maximum()*100)
        print("vlume %f" %volume)
        self.player.setVolume(volume)
        self.lab_audio.setText("volume:"+str(volume)+"%")

    def clickedSlider(self, position):
        if self.player.duration() > 0:  # only do when video starts
            video_position = int((position / 100) * self.player.duration())
            self.player.setPosition(video_position)
            self.lab_video.setText("%.2f%%" % position)
        else:
            self.sld_video.setValue(0)

    def moveSlider(self, position):
        self.sld_video_pressed = True
        if self.player.duration() > 0:  
            video_position = int((position / 100) * self.player.duration())
            self.player.setPosition(video_position)
            self.lab_video.setText("%.2f%%" % position)

    def pressSlider(self):
        self.sld_video_pressed = True
        print("pressed")

    def releaseSlider(self):
        self.sld_video_pressed = False

    def changeSlide(self, position):
        if not self.sld_video_pressed:  # mouse click, no update
            self.vidoeLength = self.player.duration()+0.1
            self.sld_video.setValue(round((position/self.vidoeLength)*100))
            self.lab_video.setText("%.2f%%" % ((position/self.vidoeLength)*100))

    def openVideoFile(self):
        self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # select file
        self.player.play()  # play file
        print(self.player.availableMetaData())

    def playVideo(self):
        self.player.play()

    def pauseVideo(self):
        self.player.pause()
        
    
    def videoDoubleClicked(self, text):

        if self.player.duration() > 0:  # allow full screen
            if self.videoFullScreen:
                self.player.setVideoOutput(self.wgt_video)
                self.videoFullScreenWidget.hide()
                self.videoFullScreen = False
            else:
                self.videoFullScreenWidget.show()
                self.player.setVideoOutput(self.videoFullScreenWidget)
                self.videoFullScreenWidget.setFullScreen(1)
                self.videoFullScreen = True

