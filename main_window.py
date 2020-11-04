from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from pynput import keyboard
import systems
import math

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()

        self.setWindowTitle("[BRGD] Undermining Tool")
        
        self.windowWidget = QtWidgets.QWidget()
        VLayout = QtWidgets.QVBoxLayout()
        self.windowWidget.setLayout(VLayout)
        self.setCentralWidget(self.windowWidget)
        self.header = Header()
        VLayout.addWidget(self.header)
        
        self.squadron = Squadron()
        self.session = Session()
        
        self.squadron.setSession(self.session)
        self.session.setSquadron(self.squadron)
        
        VLayout.addLayout(self.session)
        VLayout.addLayout(self.squadron)
        
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
        
class Session(QtWidgets.QVBoxLayout):
    """Where the user selects the system to undermine and info about total merits in system"""
    def __init__(self,):
        super(Session,self).__init__()
        
        self.systemName = ""
        self.systemTrigger = 0
        self.meritsDunked = 0
        self.meritsNeeded = 0
        self.killTracker = KillTracker(self)
        self.triggerInput = NumberField("Trigger",0)
        self.triggerInput.setCallback(self.inputTrigger)
        self.dunkedInput = NumberField("Merits Already Submitted",0)
        self.dunkedInput.setCallback(self.inputDunked)
        self.systemSelect = SystemSelect()
        self.systemSelect.setNameCallback(self.inputSystem)
        self.systemSelect.setMultiCallback(self.inputSystemAndTrigger)
        
        self.progressBar = ProgressBar()
        
        Row1 = QtWidgets.QHBoxLayout()
        Row2 = QtWidgets.QHBoxLayout()
        
        self.addLayout(Row1)
        self.addLayout(Row2)
        
        Row1.addLayout(self.systemSelect)
        Row1.addLayout(self.dunkedInput)
        
        Row2.addLayout(self.triggerInput)
        Row2.addLayout(self.killTracker)
        
        self.addLayout(self.progressBar)
    
    def setSquadron(self,squadron):
        self.squadron = squadron
        
    def calculateMerits(self):
        self.meritsNeeded = self.systemTrigger - self.meritsDunked - self.killTracker.killMerits*self.squadron.squadSize - self.squadron.totalMerits
        #TODO: add the bar class
        
        self.progressBar.updateProgressBars(self.systemTrigger,
                                            self.meritsDunked,
                                            self.squadron.totalMerits,
                                            self.killTracker.killMerits*self.squadron.squadSize,
                                            self.meritsNeeded,
                                            self.squadron.squadSize
        )
        self.squadron.changeKillTrackerMerits(self.killTracker.killMerits)
        
    def inputSystemAndTrigger(self,system_name,new_trigger):
        self.systemName = system_name
        self.inputTrigger(new_trigger)
        self.triggerInput.setValue(new_trigger)
    
    def inputSystem(self,input_string):
        """Set the current system's name"""
        self.systemName = input_string
        
    def inputTrigger(self,new_Trigger):
        """do all the things that need to be done to update the totals"""
        self.systemTrigger = new_Trigger
        self.calculateMerits()
        
    def inputDunked(self,new_dunked):
        """do all the things that need to be done to update the totals"""
        self.meritsDunked = new_dunked
        self.calculateMerits()
        
class Squadron(QtWidgets.QVBoxLayout):
    """Where the user manages the individuals undermining the system"""
    def __init__(self):
        super(Squadron,self).__init__()
        self.totalMerits = 0
        self.squadSize = 0
        self.squadMates = [SquadMate(num+1,self) for num in range(10)]
    
    def setSession(self,session):
        self.session = session
        
    def changeMerits(self):
        self.totalMerits = 0
        for mate in self.squadMates:
            self.totalMerits += mate.merits
        self.session.calculateMerits()
        
            
    def changeSquad(self):
        self.squadSize = 0
        for mate in self.squadMates:
            self.squadSize += mate.isPopulated
        self.session.calculateMerits()
        
        
    def changeKillTrackerMerits(self,merits):
        for mate in self.squadMates:
            mate.changeKillTrackerMerits(merits)
    
class SquadMate(QtWidgets.QHBoxLayout):
    def __init__(self,num,squadron):
        super(SquadMate,self).__init__()
        
        self.squadron = squadron
        self.merits = 0
        self.num = num
        self.isPopulated = False
        
        self.IDNum = QtWidgets.QLabel()
        self.IDNum.setMinimumWidth(30)
        self.addWidget(self.IDNum)
        
        self.editor = QtWidgets.QLineEdit()
        self.editor.setPlaceholderText("Commander name")
        self.editor.textChanged.connect(self.textChanged)
        self.editor.setMinimumWidth(140)
        
        self.addWidget(self.editor)
        
        self.meritEditor = QtWidgets.QSpinBox()
        self.meritEditor.valueChanged.connect(self.setMerits)
        self.meritEditor.setRange(0,100000)
        
        self.meritEditor.setMinimumWidth(90)
        self.addWidget(self.meritEditor)
        
        self.killTracker = QtWidgets.QLabel()
        self.killTracker.setMinimumWidth(90)
        self.addWidget(self.killTracker)
        
        squadron.addLayout(self)
    
    def setMerits(self,num_merits):
        self.merits = num_merits
        self.squadron.changeMerits()
        
    def changeKillTrackerMerits(self,merits):
        if merits > 0 and self.isPopulated:
            self.killTracker.setText('<font color="'+systems.PROGRESS_BAR_COLORS[2]+'">+'+str(merits)+'</font')
        else:
            self.killTracker.setText("")

    def textChanged(self,input_text):
        self.isPopulated = len(input_text) > 0
        if self.isPopulated:
            self.IDNum.setText(str(self.num))
        else:
            self.IDNum.setText("")
        self.squadron.changeSquad()

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
        
        
class KillTracker(QtWidgets.QVBoxLayout):
    def __init__(self,session):
        super(KillTracker,self).__init__()
        self.kills = 0
        self.killMerits = 0
        self.session = session
        
        TextLabel = QtWidgets.QLabel("Kill Tracker")
        self.addWidget(TextLabel)
        
        HLayout = QtWidgets.QHBoxLayout()
        self.addLayout(HLayout)
        
        self.resetButton = QtWidgets.QPushButton("Reset")
        
        self.resetButton.clicked.connect(self.resetKills)
        
        self.spinBox = QtWidgets.QSpinBox()
        self.spinBox.setRange(0,10000)
        self.spinBox.setSuffix(" kills")
        
        self.spinBox.valueChanged.connect(self.setKills)
        
        HLayout.addWidget(self.spinBox)
        HLayout.addWidget(self.resetButton)
        
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()      
    
    def on_press(self,btn):
        try:
            if btn == keyboard.Key.f4:
                self.incrementKills()
        except:
            None
    
    def on_release(self,btn):
        None
    
    def resetKills(self):
        self.setKills(0)
        
    def incrementKills(self):
        self.setKills(self.kills + 1)
        
    def decrementKills(self):
        self.setKills(max(self.kills -1, 0))
        
    def setKills(self,num_kills):
        if self.kills == num_kills:
            return
        self.kills = num_kills
        self.killMerits = num_kills * systems.MERITS_PER_KILL
        self.spinBox.setValue(self.kills)
        self.session.calculateMerits()
        
class SystemSelect(QtWidgets.QVBoxLayout):
    def __init__(self):
        super(SystemSelect,self).__init__()
        
        TextLabel = QtWidgets.QLabel("System")
        
        self.addWidget(TextLabel)
        
        self.editor = QtWidgets.QComboBox()
        self.editor.setEditable(True)
        self.editor.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.editor.addItems(systems.get_system_names())
        self.editor.activated.connect(self.activated)
        self.editor.installEventFilter(self)
        self.addWidget(self.editor)
        
    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.FocusIn:
            self.editor.clearEditText()
        return False
        
    def activated(self,new_index):
        Sys = systems.find_system_by_number(new_index)
        if Sys and self.multiCallback:
            self.multiCallback(Sys.name,Sys.systemTrigger)
        else:
            self.callback(self.editor.currentText)
        
    def setNameCallback(self,callback):
        self.callback = callback        
    def setMultiCallback(self,multiCallback):
        self.multiCallback = multiCallback
        
class ProgressBar(QtWidgets.QVBoxLayout):
    def __init__(self):
        super(ProgressBar,self).__init__()
        
        TextLabel = QtWidgets.QLabel("System Progress")
        
        self.addWidget(TextLabel)
        
        self.currentlyDunked = False
        
        self.barHolder = QtWidgets.QFrame()
        
        self.barHolder.setMinimumHeight(40)
        self.barHolder.setFrameShape(1)
        self.barHolder.setFrameShadow(0x10)
        self.barHolder.setLineWidth(1)
        self.barHolder.setMidLineWidth(1)
        
        self.addWidget(self.barHolder)
        
        BarHLayout = QtWidgets.QHBoxLayout()
        BarHLayout.setSpacing(0)
        self.barHolder.setLayout(BarHLayout)
        
        self.dunkedBar = QtWidgets.QWidget()
        self.dunkedBar.setStyleSheet("QWidget {background-color:"+systems.PROGRESS_BAR_COLORS[0]+"}")

        self.squadronBar = QtWidgets.QWidget()
        self.squadronBar.setStyleSheet("QWidget {background-color:"+systems.PROGRESS_BAR_COLORS[1]+"}")
        
        self.trackerBar = QtWidgets.QWidget()
        self.trackerBar.setStyleSheet("QWidget {background-color:"+systems.PROGRESS_BAR_COLORS[2]+"}")
        
        BarHLayout.addWidget(self.dunkedBar)
        BarHLayout.addWidget(self.squadronBar)
        BarHLayout.addWidget(self.trackerBar)
        BarHLayout.addStretch()
       
        self.progressText = QtWidgets.QLabel()
        
        self.addWidget(self.progressText)
        self.updateProgressBars(0,0,0,0,0,0)
        
    def updateProgressBars(self,trigger,dunked,squadron,tracker,remaining,mates):
        if trigger > 0:
            self.progressText.setText(str(int((dunked+squadron)/trigger*100))+"% Complete: "+str(dunked+squadron)+"/"+str(trigger)+"   "+str(max(0,remaining))+" remain w/ kill tracker   "+str(math.ceil((trigger-dunked-squadron)/max(1,mates)))+" per CMDR")
            barWidth = self.barHolder.width()-20
            dunkedBarWidth = min(int(barWidth*dunked/trigger),barWidth)
            squadronBarWidth = min(int(barWidth*squadron/trigger),barWidth-dunkedBarWidth)
            trackerBarWidth = min(int(barWidth*tracker/trigger),barWidth-dunkedBarWidth-squadronBarWidth)
        
            self.dunkedBar.setFixedWidth(dunkedBarWidth)
            self.squadronBar.setFixedWidth(squadronBarWidth)
            self.trackerBar.setFixedWidth(trackerBarWidth)
            if remaining <= 0 and not self.currentlyDunked:
                #play a beep sound
                print('\a')
                self.currentlyDunked = True
            elif remaining > 0:
                self.currentlyDunked = False
        else:
            self.currentlyDunked = False
            self.progressText.setText("0% Complete")
            self.dunkedBar.setFixedWidth(0)
            self.squadronBar.setFixedWidth(0)
            self.trackerBar.setFixedWidth(0)
        
        
        