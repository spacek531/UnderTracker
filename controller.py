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
        
        self.comboBox.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        
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
            self.session.setSystemOwner(0)

class NumberController(QtCore.QObject):
    def __init__(self,spinBox,callback):
        super(NumberController,self).__init__()
        self.spinBox = spinBox
        self.callback = callback
        
        self.spinBox.editingFinished.connect(self.editingFinished)
        self.spinBox.installEventFilter(self)     
        
    def editingFinished(self):
        self.callback(self.spinBox.value())
        
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.FocusIn:
            self.spinBox.selectAll()
        return False

class UsernameController(QtCore.QObject):
    def __init__(self,comboBox,underminer):
        super(UsernameController,self).__init__()
        self.comboBox = comboBox
        self.underminer = underminer
        self.comboBox.addItems(users.get_user_names()) 
        self.comboBox.activated.connect(self.activated) 
        self.comboBox.installEventFilter(self)
        
        self.comboBox.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.FocusIn:
            self.comboBox.clearEditText()
        return False
        
    def activated(self,new_index):
        User = users.find_user_by_number(index)
        if User:
            self.underminer.setSystemName(Sys.name)
            self.underminer.setSystemOwner(Sys.owner)
            self.underminer.setUsername(Sys.systemTrigger)
            None
        else:
            self.underminer.setUsername(self.editor.currentText)

"""
class NumberField(QtWidgets.QVBoxLayout):
    def __init__(self,description,default_value = 0):
        super(NumberField,self).__init__()
        self.value = default_value
        
        TextLabel = QtWidgets.QLabel(description)
        
        self.addWidget(TextLabel)
        
        self.editor = QtWidgets.QLineEdit()
        self.editor.setPlaceholderText(str(self.value))
        LineValidator = QtGui.QIntValidator()
        LineValidator.setBottom(0)
        self.editor.setValidator(LineValidator)
        self.editor.textChanged.connect(self.textChanged)
        self.editor.editingFinished.connect(self.editingFinished)
        
        self.addWidget(self.editor)

    def textChanged(self,input_text):
        try:
            self.value = int(str(input_text))
        except:
            self.value = 0
    def editingFinished(self):
        if self.callback:
            self.callback(self.value)
    def setCallback(self,callback):
        self.callback = callback
    
    def setValue(self,new_value):
        self.editor.setText(str(new_value))
        """