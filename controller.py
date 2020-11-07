from PyQt5 import QtWidgets, QtCore, QtGui
import systems, users

class SystemController(QtCore.QObject):
    def __init__(self,comboBox,session):
        super(SystemController,self).__init__()
        self.comboBox = comboBox
        self.session = session
        self.comboBox.addItems(systems.get_system_names()) 
        self.comboBox.activated.connect(self.activated) 
        self.comboBox.installEventFilter(self)
        
        self.comboBox.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.FocusIn:
            self.comboBox.clearEditText()
        return False
        
    def activated(self,new_index):
        Sys = systems.find_system_by_number(new_index)
        if Sys:
            self.session.setSystemObject(Sys)
        else:
            self.session.setSystemObject(None)
            self.session.setSystemName(self.comboBox.currentText())
            
class UsernameController(QtCore.QObject):
    def __init__(self,comboBox,miner):
        super(UsernameController,self).__init__()
        self.comboBox = comboBox
        self.miner = miner
        self.comboBox.addItems(users.get_user_names()) 
        self.comboBox.activated.connect(self.activated) 
        #self.comboBox.installEventFilter(self)
        
        self.comboBox.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.comboBox.clearEditText()
        
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.FocusIn:
            self.comboBox.clearEditText()
        return False
        
    def activated(self,new_index):
        User = users.find_user_by_number(new_index)
        if User:
            self.miner.setAssociatedUser(User)
            self.miner.setUsername(User.truename)
            None
        else:
            self.miner.setUsername(self.comboBox.currentText())

class NumberController(QtCore.QObject):
    def __init__(self,spinBox,callback):
        super(NumberController,self).__init__()
        self.spinBox = spinBox
        self.callback = callback
        
        self.spinBox.editingFinished.connect(self.editingFinished)
        self.spinBox.valueChanged.connect(self.editingFinished)
        self.spinBox.installEventFilter(self)
        
    def editingFinished(self):
        self.callback(self.spinBox.value())
        
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.FocusIn:
            self.spinBox.selectAll()
        return False

class PushButtonController(QtCore.QObject):
    def __init__(self,button,callback):
        super(PushButtonController,self).__init__()
        self.button = button
        self.callback = callback
        
        self.button.clicked.connect(self.clicked)
        
    def eventFilter(self,object,event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.clicked()
                
        return False
    
    def clicked(self):
        self.callback()