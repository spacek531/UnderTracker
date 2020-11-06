from PyQt5 import QtWidgets, QtCore, QtGui
import systems, users

class SystemController(QtCore.QObject):
    def __init__(self,comboBox,session):
        super(SystemController,self).__init__()
        self.comboBox = comboBox
        self.session = session
        self.comboBox.addItems(systems.get_system_names()) 
        self.comboBox.activated.connect(self.activated)       
        
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

class NumberController(QtCore.QObject):
    def __init__(self,spinBox,callback):
        super(NumberController,self).__init__()
        self.spinBox = spinBox
        self.callback = callback
        
        #self.spinBox.textChanged.connect(self.textChanged)
        self.spinBox.editingFinished.connect(self.editingFinished)
        
    def textChanged(self,input_text):
        try:
            self.value = int(str(input_text))
        except:
            self.value = 0
    def editingFinished(self):
        self.callback(self.value)