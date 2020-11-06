from PyQt5 import QtWidgets, QtCore, QtGui
import systems, users

class SystemController(QtCore.QObject):
    def __init__(self,comboBox,session):
        super(SystemController,self).__init__()
        self.comboBox = comboBox
        self.session = session
        self.comboBox.addItems(systems.get_system_names())        
        
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.FocusIn:
            self.comboBox.clearEditText()
        return False
        
    def activated(self,new_index):
        Sys = systems.find_system_by_number(new_index)
        if Sys:
            self.session.setSystemName(Sys.name)
            self.session.setSystemOwner(Sys.owner)
            self.session.setSystemTrigger(Sys.systemTrigger)
            None
        else:
            self.session.setSystemName(self.editor.currentText)

class NumberInputController(QtCore.QObject):
    def __init__(self,spinbox,callback):
        super(NumberInputController,self).__init__()
        self.spinbox = spinbox
        self.callback = callback
        
    