from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()

        self.setWindowTitle("[BRGD] Undermining Tool")
        
        self.windowWidget = QtWidgets.QWidget()
        vLayout = QtWidgets.QVBoxLayout()
        self.windowWidget.setLayout(vLayout)
        self.setCentralWidget(self.windowWidget)
        self.header = Header()
        vLayout.addWidget(self.header)
        
    def create_menu(self):
        None

class Header(QtWidgets.QWidget):
    """The fancy shmancy logo on the top of the application"""
    def __init__(self):
        super(Header,self).__init__()
        
        HLayout = QtWidgets.QVBoxLayout()
        self.setLayout(HLayout)
        self.setMinimumHeight(50)
        
        c = QtWidgets.QLabel("Starlight Brigade Undermining Tool")
        
        HLayout.addWidget(c)
        
class Session(QtWidgets.QWidget):
    """Where the user selects the system to undermine and info about total merits in system"""
    def __init__(self):
        super(Session,self).__init__()
        
        self.systemName = ""
        self.systemTrigger = 0
        self.meritsDunked = 0
        
        
        
class Squadron(QtWidgets.QWidget):
    """Where the user manages the individuals undermining the system"""
    def __init__(self):
        super(Squadron,self).__init__()
        
        