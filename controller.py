from PyQt5 import QtWidgets, QtCore, QtGui

class SystemController(QtCore.QObject):
    def __init__(self,comboBox,session):
        super(SystemController,self).__init__()
        self.comboBox = comboBox
        self.session = session
        
        
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.FocusIn:
            self.comboBox.clearEditText()
        return False
        
    def activated(self,new_index):
        Sys = systems.find_system_by_number(new_index)
        if Sys:
            session.setSystemTrigger(Sys.systemTrigger)
            session.setSystemName(Sys.name)
            session.setSystemOwner(Sys.owner)
        else:
            self.session.setSystemName(self.editor.currentText)   