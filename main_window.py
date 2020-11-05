from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

import resources

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("[BRGD] Undermining Tool")
        self.setStyleSheet(TOP_LEVEL_CSS)
        
        self.windowWidget = QtWidgets.QWidget()
        self.VLayout = QtWidgets.QVBoxLayout()
        self.windowWidget.setLayout(self.VLayout)
        
        self.createHeader()
        
        imageLabel = QtWidgets.QLabel()
        imageLabel.setText("Hello WOrld")
        imageLabel.setObjectName("HeaderImage")
        imageLabel.setMinimumSize(400,400)
        
        self.VLayout.addWidget(imageLabel)
        
    def addWidget(self,widget):
        self.VLayout.addWidget(widget)
    
    def addLayout(self,layout):
        self.VLayout.addLayout(layout)
        
    def createHeader(self):
        None
        
PROGRESS_BAR_COLORS = [
    "#4CAF0B",
    "#4AB1D3",
    "#F48D1C"
]
        
TOP_LEVEL_CSS ="""
QMainWindow {Background-Color:#03080A; }
QLabel {Color: #1F5368; Background-Color:#FFFFFA; }
QGroupBox {Color: #1F5368; }
QGroupBox#submittedGroupBox {Color: #347708; }
"""