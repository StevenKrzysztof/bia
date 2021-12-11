# coding:utf-8

from PyQt5 import QtCore,QtGui,QtWidgets
import sys
import qtawesome
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QAction, QMenu ,QMenuBar
import os
import time
from PyQt5.QtCore import QCoreApplication, Qt, pyqtSignal, QTimer
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
#from GUI import Ui_MainWindow
from PyQt5.QtWidgets import QSlider
from myVideoWidget import myVideoWidget
from PyQt5.QtWidgets import QMenu
from myvideoslider import myVideoSlider
import video 
import Maskshow
import segmentation
import Distributionshow



#video的window



# 原本的右边窗口
class right_widget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格


        self.right_recommend_label = QtWidgets.QLabel("welcome to our programme")
        self.right_recommend_label.setObjectName('right_lable')

        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)
        

        
        
        
        
        #self.recommend_logo_1.setIcon(QtGui.QIcon('./logo.jpg')) # 设置按钮图标
        #self.recommend_logo_1.setIconSize(QtCore.QSize(800,800)) # 设置图标大小
        

        

        self.right_layout.addWidget(self.right_recommend_label, 2, 0, 1, 8, Qt.AlignTop)
        self.right_layout.addWidget(self.right_recommend_widget, 2, 0, 2, 9)

        
       


       

       


        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                border-image:url(./background.png);
                background:white;
                border-top:10px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:20px;
                border-bottom-right-radius:20px;
            }
            QLabel#right_lable{
                border:none;
                font-size:30px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')

        self.right_recommend_widget.setStyleSheet(
            '''
            QToolButton{
                border:none;
                background:yellow;
                width:100px;
                height:100px;
                border-top:1px solid darkRed;
                border-bottom:1px solid darkRed;
                border-top-right-radius:20px;
                border-bottom-right-radius:20px;
                border-top-left-radius:20px;
                border-bottom-left-radius:20px;
            }
            QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')

       


       

##main window
class FakeWindow(QWidget):
    def __init__(self, name, Layout):
        super().__init__()
        self.name = name
        self.Layout = Layout
        self.init_ui()

    def init_ui(self):
        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        self.Layout.addWidget(self.right_widget,0,2,12,10) # 右侧部件在第0行第3列，占8行9列

        self.right_recommend_label1 = QtWidgets.QLabel("Welcome to our Programme")
        self.right_recommend_label1.setObjectName('right_lable')

        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)
        
        

        
       

       
        self.right_layout.addWidget(self.right_recommend_label1, 2, 0, 1, 8, Qt.AlignTop)

        self.right_layout.addWidget(self.right_recommend_widget, 7, 0, 2, 9, Qt.AlignTop)
  
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                border-image:url(./background.png);
                background:white;
                border-top:10px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:20px;
                border-bottom-right-radius:20px;
            }
            QLabel#right_lable{
                border:none;
                font-size:40px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')

        self.right_recommend_widget.setStyleSheet(
            '''
            QToolButton{
                border:none;
                background:yellow;
                width:100px;
                height:100px;
                border-top:1px solid darkRed;
                border-bottom:1px solid darkRed;
                border-top-right-radius:20px;
                border-bottom-right-radius:20px;
                border-top-left-radius:20px;
                border-bottom-left-radius:20px;
            }
            QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')


#fake window 2, which is help readme

class FakeWindow2(QWidget):
    def __init__(self, name, Layout):
        super().__init__()
        self.name = name
        self.Layout = Layout
        self.init_ui()

    def init_ui(self):
        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        self.Layout.addWidget(self.right_widget,0,2,12,10) # 右侧部件在第0行第3列，占8行9列


        self.right_recommend_label1 = QtWidgets.QLabel("Here may help you understand our software")
        self.right_recommend_label1.setObjectName('right_lable')
        
        

        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)

        
        


        self.right_layout.addWidget(self.right_recommend_label1, 1, 0, 1, 9, Qt.AlignTop)
        
        

        self.right_layout.addWidget(self.right_recommend_widget, 4, 0, 2, 9, Qt.AlignTop)

        
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                border-image:url(./readme.png);
                background:white;
                border-top:10px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:20px;
                border-bottom-right-radius:20px;
            }
            QLabel#right_lable{
                border:none;
                font-size:30px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')

        self.right_recommend_widget.setStyleSheet(
            '''
            QToolButton{
                border:none;
                background:yellow;
                width:100px;
                height:100px;
                border-top:1px solid darkRed;
                border-bottom:1px solid darkRed;
                border-top-right-radius:20px;
                border-bottom-right-radius:20px;
                border-top-left-radius:20px;
                border-bottom-left-radius:20px;
            }
            QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')


 


#这里改成上传文件功能
class SegmentationWindow(QWidget):
    def __init__(self, name, Layout):
        super().__init__()
        self.name = name
        self.Layout = Layout
        self.init_ui()
        
        
    def echo(self, value):
      '''显示对话框返回值'''
      QMessageBox.information(self, "返回值",  "得到：{}\n\ntype: {}".format(value, type(value)), QMessageBox.Yes | QMessageBox.No)
    #pass
    
    def do_btn31(self, event): # 文件：文件夹
      dir = QFileDialog.getExistingDirectory(self, 
                  "choose file", 
                  "C:/")         # 起始路径
      segmentation.seg(dir)
      
      
    
    

    def init_ui(self):
        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        self.Layout.addWidget(self.right_widget,0,2,12,10) # 右侧部件在第0行第3列，占8行9列

        self.right_recommend_label1 = QtWidgets.QLabel("Segmentation Processing")
        self.right_recommend_label1.setObjectName('right_lable')

        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)
        
        

        
        self.recommend_button_11 = QtWidgets.QToolButton()
        self.recommend_button_11.setText("start") # 设置按钮文本
        self.recommend_button_11.clicked.connect(self.do_btn31)
        self.recommend_button_11.setIcon(QtGui.QIcon('./start.jpg')) # 设置按钮图标
        self.recommend_button_11.setIconSize(QtCore.QSize(100,80)) # 设置图标大小
        self.recommend_button_11.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文

        


        self.right_recommend_layout.addWidget(self.recommend_button_11,0,0)
        
        

       
        self.right_layout.addWidget(self.right_recommend_label1, 2, 0, 1, 8, Qt.AlignTop)

        self.right_layout.addWidget(self.right_recommend_widget, 7, 0, 2, 9, Qt.AlignTop)
  
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                border-image:url(./segbackground.png);
                background:white;
                border-top:10px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:20px;
                border-bottom-right-radius:20px;
            }
            QLabel#right_lable{
                border:none;
                font-size:40px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')

        self.right_recommend_widget.setStyleSheet(
            '''
            QToolButton{
                border:none;
                background:yellow;
                width:100px;
                height:100px;
                border-top:1px solid darkRed;
                border-bottom:1px solid darkRed;
                border-top-right-radius:20px;
                border-bottom-right-radius:20px;
                border-top-left-radius:20px;
                border-bottom-left-radius:20px;
            }
            QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')



#cell filter window
class FilterWindow(QWidget):
    def __init__(self, name, Layout):
        super().__init__()
        self.name = name
        self.Layout = Layout
        self.init_ui()
        
        
    def echo(self, value):
      '''显示对话框返回值'''
      QMessageBox.information(self, "返回值",  "得到：{}\n\ntype: {}".format(value, type(value)), QMessageBox.Yes | QMessageBox.No)
    #pass
    
    def do_btn32(self, event): # 文件：文件夹
      dir = QFileDialog.getExistingDirectory(self, 
                  "choose file", 
                  "C:/")         # 起始路径
      segmentation.seg(dir)
      
      
    
    

    def init_ui(self):
        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        self.Layout.addWidget(self.right_widget,0,2,12,10) # 右侧部件在第0行第3列，占8行9列

        self.right_recommend_label1 = QtWidgets.QLabel("Detect Active Cells")
        self.right_recommend_label1.setObjectName('right_lable')

        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)
        
        

        
        self.recommend_button_11 = QtWidgets.QToolButton()
        self.recommend_button_11.setText("Process") # 设置按钮文本
        self.recommend_button_11.clicked.connect(self.do_btn32)
        self.recommend_button_11.setIcon(QtGui.QIcon('./start.jpg')) # 设置按钮图标
        self.recommend_button_11.setIconSize(QtCore.QSize(100,80)) # 设置图标大小
        self.recommend_button_11.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文

        


        self.right_recommend_layout.addWidget(self.recommend_button_11,0,0)
        
        

       
        self.right_layout.addWidget(self.right_recommend_label1, 2, 0, 1, 8, Qt.AlignTop)

        self.right_layout.addWidget(self.right_recommend_widget, 7, 0, 2, 9, Qt.AlignTop)
  
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                border-image:url(./filterbackground.png);
                background:white;
                border-top:10px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:20px;
                border-bottom-right-radius:20px;
            }
            QLabel#right_lable{
                border:none;
                font-size:40px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')

        self.right_recommend_widget.setStyleSheet(
            '''
            QToolButton{
                border:none;
                background:yellow;
                width:100px;
                height:100px;
                border-top:1px solid darkRed;
                border-bottom:1px solid darkRed;
                border-top-right-radius:20px;
                border-bottom-right-radius:20px;
                border-top-left-radius:20px;
                border-bottom-left-radius:20px;
            }
            QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')






"这里是一个test"
class scan_us(QWidget):
    
    def __init__(self, name, Layout):
        super().__init__()
        self.name = name
        self.Layout = Layout
        self.init_ui()

    def init_ui(self):
        
        
        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        self.Layout.addWidget(self.right_widget,0,2,12,10) # 右侧部件在第0行第3列，占8行9列


        self.right_recommend_label1 = QtWidgets.QLabel("Our group Member Information")
        self.right_recommend_label1.setObjectName('right_lable')
        self.right_recommend_label2 = QtWidgets.QLabel("If you have any problem when using our program")
        self.right_recommend_label2.setObjectName('right_lable')
        self.right_recommend_label3 = QtWidgets.QLabel("Do not hesitiate to contact us through E-mail")
        self.right_recommend_label3.setObjectName('right_lable')
       
        
        

        self.right_recommend_widget = QtWidgets.QWidget() # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)


        
        
        self.recommend_button_1 = QtWidgets.QToolButton()
        self.recommend_button_1.setText("Weifan.18@intl.zju.edu.cn") # 设置按钮文本
        #self.recommend_button_1.setText("Wait")
        self.recommend_button_1.setIcon(QtGui.QIcon('./q11.png')) # 设置按钮图标
        self.recommend_button_1.setIconSize(QtCore.QSize(200,200)) # 设置图标大小
        self.recommend_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon) # 设置按钮形式为上图下文
        



        self.recommend_button_2 = QtWidgets.QToolButton()
        self.recommend_button_2.setText("Siyu.18@intl.zju.edu.cn")
        
        
        self.recommend_button_2.setIcon(QtGui.QIcon('./q22.png'))
        self.recommend_button_2.setIconSize(QtCore.QSize(200, 200))
        self.recommend_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_3 = QtWidgets.QToolButton()
        self.recommend_button_3.setText("Chenxi.18@intl.zju.edu.cn")
        
        self.recommend_button_3.setIcon(QtGui.QIcon('./q33.png'))
        self.recommend_button_3.setIconSize(QtCore.QSize(200, 200))
        self.recommend_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.recommend_button_4 = QtWidgets.QToolButton()
        self.recommend_button_4.setText("Zhiwen.18@intl.zju.edu.cn")
        self.recommend_button_4.setIcon(QtGui.QIcon('./q44.png'))
        self.recommend_button_4.setIconSize(QtCore.QSize(200, 200))
        self.recommend_button_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        
        self.recommend_button_5 = QtWidgets.QToolButton()
        self.recommend_button_5.setText("Feiyu.18@intl.zju.edu.cn")
        self.recommend_button_5.setIcon(QtGui.QIcon('./q55.png'))
        self.recommend_button_5.setIconSize(QtCore.QSize(200, 200))
        self.recommend_button_5.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)


        self.recommend_button_6 = QtWidgets.QToolButton()
        self.recommend_button_6.setText("Ziyang.18@intl.zju.edu.cn")
        self.recommend_button_6.setIcon(QtGui.QIcon('./q66.png'))
        self.recommend_button_6.setIconSize(QtCore.QSize(200, 200))
        self.recommend_button_6.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)



        self.right_recommend_layout.addWidget(self.recommend_button_1,0,0)
        
        self.right_recommend_layout.addWidget(self.recommend_button_2,0,1)
        self.right_recommend_layout.addWidget(self.recommend_button_3, 1, 0)
        self.right_recommend_layout.addWidget(self.recommend_button_4, 1, 1)
        self.right_recommend_layout.addWidget(self.recommend_button_5, 1, 2)
        self.right_recommend_layout.addWidget(self.recommend_button_6, 0, 2)


        self.right_layout.addWidget(self.right_recommend_label1, 1, 0, 1, 9, Qt.AlignTop)
        self.right_layout.addWidget(self.right_recommend_label2, 10, 0, 1, 9, Qt.AlignTop)
        self.right_layout.addWidget(self.right_recommend_label3, 12, 0, 1, 9, Qt.AlignTop)
        

        self.right_layout.addWidget(self.right_recommend_widget, 2, 0, 1, 9, Qt.AlignTop)

        
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')


        self.right_recommend_widget.setStyleSheet(
            '''
                QToolButton{border:none;}
                QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')






class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(960,700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.windowList = []

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格

        self.right_widget = right_widget()

        self.main_layout.addWidget(self.left_widget,0,0,12,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget.right_widget,0,2,12,10) # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件
        self.left_close = QtWidgets.QPushButton("") # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("") # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮
        
        
        self.left_label_4 = QtWidgets.QPushButton("Home Page")
        self.left_label_4.setObjectName('left_label')
        self.left_label_1 = QtWidgets.QPushButton("Cell Detection")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("Cell Activity")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("Ask for Help")
        self.left_label_3.setObjectName('left_label')

        
        self.left_label_4.clicked.connect(self.Main)
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.heart',color='white'),"About Us")
        self.left_button_2.setObjectName('left_button')
        self.left_button_2.clicked.connect(self.Us)
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.star',color='white'),"play Video ")
        self.left_button_4.clicked.connect(self.video)
        self.left_button_4.setObjectName('left_button')
        
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.star',color='white'),"Heat Map")
        self.left_button_6.clicked.connect(self.distribution)
        self.left_button_6.setObjectName('left_button')
        
        
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.question',color='white'),"read   me")
        self.left_button_9.setObjectName('left_button')
        self.left_button_9.clicked.connect(self.Help)
        
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star',color='white'),"Segmentation")
        self.left_button_8.setObjectName('left_button')
        self.left_button_8.clicked.connect(self.Segmentation)
        
        
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.star',color='white'),"Show Mask")
        self.left_button_7.setObjectName('left_button')
        self.left_button_7.clicked.connect(self.MaskShow)
        
        self.left_button_10 = QtWidgets.QPushButton(qtawesome.icon('fa.star',color='white'),"Find active cells")
        self.left_button_10.setObjectName('left_button')
        self.left_button_10.clicked.connect(self.Filterwind)

        self.left_layout.addWidget(self.left_mini, 0, 0,1,1)
        self.left_layout.addWidget(self.left_close, 0, 2,1,1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_label_1,2,0,1,3)
        self.left_layout.addWidget(self.left_button_8, 3, 0,1,3)
        self.left_layout.addWidget(self.left_button_2, 10, 0,1,3)
        self.left_layout.addWidget(self.left_label_2, 5, 0,1,3)
        self.left_layout.addWidget(self.left_button_4, 7, 0,1,3)
        self.left_layout.addWidget(self.left_label_4, 1, 0,1,3)
        self.left_layout.addWidget(self.left_button_6, 8, 0,1,3)
        self.left_layout.addWidget(self.left_label_3, 9, 0,1,3)
        self.left_layout.addWidget(self.left_button_7, 4, 0,1,3)
        self.left_layout.addWidget(self.left_button_10, 6, 0,1,3)
        self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)

        
        self.left_close.setFixedSize(15,15) # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15) # 设置最小化按钮大小


        self.left_close.setStyleSheet('''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet('''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        self.left_close.clicked.connect(QCoreApplication.instance().quit)
        self.left_close.clicked.connect(self.close)
        self.left_mini.clicked.connect(self.showMinimized)
        self.left_visit.clicked.connect(self.showMaximized)

        self.left_widget.setStyleSheet("\
            QPushButton{border:none;color:white;}\
            QPushButton#left_label{\
                border:none;\
                border-bottom:1px solid white;\
                font-size:18px;\
                font-weight:700;\
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;\
            }\
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}\
            QWidget#left_widget{\
                background:gray;\
                border-top:1px solid white;\
                border-bottom:1px solid white;\
                border-left:1px solid white;\
                border-top-left-radius:10px;\
                border-bottom-left-radius:10px;\
            }"
        )


        self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明


        #self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # 隐藏边框

        self.main_layout.setSpacing(0)
        
    

    
    def video(self):
        #app1 = QApplication(sys.argv)
        video1=video.myMainWindow()
        video1.show()
        sys.exit(app2.exec_())  
        
        
    def MaskShow(self):
        
        #app = QApplication(sys.argv)
        box = Maskshow.MainDemo()
        box.show()
        app.exec_()
         
        
    '''    
    def Filter(self, regions):
        ACF = Active_cell_finder('neurofinder.00.00/images/*.tiff', regions)
        _ = ACF()
        
    '''
    
    def distribution(self):
        
        #app = QApplication(sys.argv)
        box = Distributionshow.MainDemo()
        box.show()
        app.exec_()
         
        
        
    
        
        
        
    

    def Launch_Nav(self):
        turn_around_window = SecondWindow("Navigation",self.main_layout)
        self.windowList.append(turn_around_window)
        # 先关闭第一个窗口,视觉上好看
        self.right_widget.right_widget.close()
        #turn_around_window.show()
        # 开启导航
        # source 是为了将当前工作空间的所有环境变量置于最上层

        '''
        os.system(
        "gnome-terminal -x bash -c 'source ~/New_catkin_ws/devel/setup.bash; roslaunch rbx1_bringup fake_turtlebot.launch'"
        )
        time.sleep(3)
        os.system(
        "gnome-terminal -x bash -c 'roslaunch rbx1_nav fake_amcl.launch map:=test_map.yaml'"
        )
        time.sleep(3)
        os.system(
        "gnome-terminal -x bash -c 'rosrun rviz rviz -d `rospack find rbx1_nav`/nav.rviz'"
        )
        '''

    '''
    def CheckOut(self):
        CheckOut_window = scan_pay("Check_Out",self.main_layout)
        self.windowList.append(CheckOut_window)
        # 先关闭第一个窗口,视觉上好看
        self.right_widget.right_widget.close()
    '''
        
    def Segmentation(self,img_path):
        Segment_window = SegmentationWindow("Segment",self.main_layout)
        self.windowList.append(Segment_window)
        # 先关闭第一个窗口,视觉上好看
        self.right_widget.right_widget.close()


    def Filterwind(self,img_path):
        Filter_window = FilterWindow("Filter",self.main_layout)
        self.windowList.append(Filter_window)
        # 先关闭第一个窗口,视觉上好看
        self.right_widget.right_widget.close()


    def Us(self):
        Us_window = scan_us("Us", self.main_layout)
        self.right_widget.right_widget.close()
        
        self.windowList.append(Us_window)
        
        
        
    def Main(self):
        Main_window = FakeWindow("Main",self.main_layout)
        self.right_widget.right_widget.close()
        self.windowList.append(Main_window)
        # 先关闭第一个窗口,视觉上好看
       
    def Help(self):
        Main_window2 = FakeWindow2("Main2",self.main_layout)
        self.right_widget.right_widget.close()
        self.windowList.append(Main_window2)
        # 先关闭第一个窗口,视觉上好看
         

        

#补充的内容






def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
