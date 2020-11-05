from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

import resources

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("[BRGD] Undermining Tool")
        self.setStyleSheet(TOP_LEVEL_CSS)
        
        self.VLayout = QtWidgets.QVBoxLayout()
        
        self.setLayout(self.VLayout)
        
    def addWidget(self,widget):
        self.VLayout.addWidget(widget)
    
    def addLayout(self,layout):
        self.VLayout.addLayout(layout)
        
        
        
        
PROGRESS_BAR_COLORS = [
    "#4CAF0B",
    "#4AB1D3",
    "#F48D1C"
]
        
TOP_LEVEL_CSS ="""
QMainWindow {Background-Color:#03080A; }
QLabel {Color: #1F5368; }
QGroupBox {Color: #1F5368; }
QGroupBox#submittedGroupBox {Color: #347708; }
"""