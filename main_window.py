from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

import resources
import model

#QtGui.QFontDatabase.addApplicationFont(":/resources/Audiowide_Regular.ttf")

TitleFont = QtGui.QFont("Consolas",16,100)
SubtitleFont = QtGui.QFont("Consolas",14,100)
BodyFont = QtGui.QFont("Lucida Sans",16,100)
SubBodyFont = QtGui.QFont("Lucida Sans",14,100)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("[BRGD] Undermining Tool")
        self.setStyleSheet(TOP_LEVEL_CSS)
        self.VLayout = QtWidgets.QVBoxLayout()
        self.VLayout.setContentsMargins(0,0,0,0)
        self.VLayout.setSpacing(0)
        CentralWidget = QtWidgets.QWidget()
        CentralWidget.setLayout(self.VLayout)
        CentralWidget.setObjectName("CentralWidget")
        CentralWidget.setFont(TitleFont)
        self.setCentralWidget(CentralWidget)
        
        self.createHeader()
        self.createManagementSection()
        self.createReportingSection()
        
        self.session = model.Session(self)
        
    def addWidget(self,widget):
        self.VLayout.addWidget(widget)
    
    def addLayout(self,layout):
        self.VLayout.addLayout(layout)
        
    def addSpacing(self,space):
        self.VLayout.addSpacing(space)
        
    def createHeader(self):
        ImageLabel = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(":/resources/header.png")
        ImageLabel.setPixmap(pixmap)
        ImageLabel.setMinimumSize(640,100)
        
        HorizontalBar = QtWidgets.QFrame()
        HorizontalBar.setFrameShape(QtWidgets.QFrame.HLine)
        HorizontalBar.setFrameShadow(QtWidgets.QFrame.Raised)
        HorizontalBar.setLineWidth(7)
        
        self.addWidget(ImageLabel)
        
        self.addWidget(HorizontalBar)
        
    def createManagementSection(self):
        
        Row1 = QtWidgets.QHBoxLayout()
        Row2 = QtWidgets.QHBoxLayout()
        
        Row1.setContentsMargins(15,5,25,5)
        Row2.setContentsMargins(15,5,15,10)
        
        self.systemSelector = SystemSelector()
        
        Row1.addLayout(self.createInputBoxFrame(self.systemSelector,"System"))
        Row1.addSpacing(15)
        
        self.powerLogo = QtWidgets.QLabel()
        self.powerLogo.setMinimumSize(200,100)
        
        Row1.addWidget(self.powerLogo)
        
        self.triggerInput = NumberInput()
        self.redeemedInput = NumberInput()
        
        Row2.addLayout(self.createInputBoxFrame(self.triggerInput,"Merit Trigger"))
        Row2.addSpacing(15)
        Row2.addLayout(self.createInputBoxFrame(self.redeemedInput,"Merits Redeemed","GreenText"))
        
        self.addLayout(Row1)
        self.addLayout(Row2)
        
    def createReportingSection(self):
        
        self.addSpacing(20)
        
        self.progressBar = ProgressBar()
        self.addLayout(self.progressBar)
        
        Row1 = QtWidgets.QHBoxLayout()
        Row1.setContentsMargins(15,5,15,0)
        
        self.totalUnderminedMeritsLabel = ValueLabel("Total Earned\nMerits")
        self.totalUnderminersLabel = ValueLabel("Total\nCommanders")
        #self.inactiveUnderminedMeritsLabel = ValueLabel("Inactive\nMerits")
        self.meritsNeededLabel = ValueLabel("Remaining\nMerits","OrangeText")
        
        Row1.addLayout(self.totalUnderminedMeritsLabel)
        Row1.addLayout(self.totalUnderminersLabel)
        #Row1.addLayout(self.inactiveUnderminedMeritsLabel)
        Row1.addLayout(self.meritsNeededLabel)
        
        Row2 = QtWidgets.QHBoxLayout()
        Row2.setContentsMargins(15,0,15,0)
        
        
        self.meritsPerUnderminerRemainingLabel = ValueLabel("Remaining Merits\nPer Commander","OrangeText")
        self.meritsPerUnderminerLabel = ValueLabel("Total Merits\nPer Commander","OrangeText")
        self.killsPerUnderminerLabel = ValueLabel("Remaining Kills\nPer Commander","OrangeText")
        
        Row2.addLayout(self.meritsPerUnderminerLabel)
        Row2.addLayout(self.killsPerUnderminerLabel)
        Row2.addLayout(self.meritsPerUnderminerRemainingLabel)
        
        self.addLayout(Row1)
        self.addLayout(Row2)
        
        self.updateMerits()
        self.updateUnderminers()
        
    def createInputBoxFrame(self,contentWidget,description,identifier = None):
        L1 = QtWidgets.QVBoxLayout()
        L1.setContentsMargins(0,0,0,0)
        L1.addStretch(0)
        
        TextLabel = QtWidgets.QLabel()
        TextLabel.setText(description)
        TextLabel.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        
        if identifier:
            TextLabel.setObjectName(identifier)
            
        L1.addWidget(TextLabel)
        
        Frame = QtWidgets.QFrame()
        Frame.setObjectName("InputFrame")
        
        L2 = QtWidgets.QVBoxLayout()
        L2.setContentsMargins(0,0,0,0)
        Frame.setLayout(L2)
        
        L2.addWidget(contentWidget)
        L1.addWidget(Frame)
        L1.addStretch(0)
        
        return L1
    
    ## now for the updater functions ##
    
    def updateMerits(self,
                     systemTrigger = 0000,
                     meritsTotal = 0000,
                     meritsRedeemed = 0000,
                     activeUnderminedMerits = 0000,
                     inactiveUnderminedMerits = 0000,
                     totalUnderminedMerits = 0000,
                     
                     meritsNeeded = 0000,
                     meritsPerUnderminer = 0000,
                     meritsPerUnderminerRemaining = 0000,
                     killsPerUnderminer = 0000,
                     
                     ):
        
        self.totalUnderminedMeritsLabel.setValue(totalUnderminedMerits)
        #self.activeUnderminedMeritsLabel.setValue(activeUnderminedMerits)
        #self.inactiveUnderminedMeritsLabel.setValue(inactiveUnderminedMerits)
        
        self.meritsNeededLabel.setValue(meritsNeeded)
        self.meritsPerUnderminerRemainingLabel.setValue(meritsPerUnderminerRemaining)
        self.meritsPerUnderminerLabel.setValue(meritsPerUnderminer)
        self.killsPerUnderminerLabel.setValue(killsPerUnderminer)
        
        self.progressBar.setProgress(systemTrigger,meritsTotal,meritsRedeemed,activeUnderminedMerits,inactiveUnderminedMerits)
    
    def updateUnderminers(self,
                          activeUnderminers = 0,
                          totalUnderminers = 0,
                          underminers = []
                          ):
        self.totalUnderminersLabel.setValue(totalUnderminers)

class SystemSelector(QtWidgets.QLineEdit):
    def __init__(self):
        super(SystemSelector,self).__init__()
        self.setFont(BodyFont)

class NumberInput(QtWidgets.QSpinBox):
    def __init__(self):
        super(NumberInput,self).__init__()
        self.setFont(BodyFont)
        self.setMinimum(0)
        self.setMaximum(100000)

class ValueLabel(QtWidgets.QVBoxLayout):
    def __init__(self,description,identifier = None):
        super(ValueLabel,self).__init__()
        
        self.setContentsMargins(5,0,0,5)
        
        TextLabel = QtWidgets.QLabel()
        TextLabel.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        TextLabel.setText(description)
        TextLabel.setFont(SubtitleFont)
        
        self.dataLabel = QtWidgets.QLabel()
        self.dataLabel.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.dataLabel.setFont(BodyFont)

        if identifier:
            TextLabel.setObjectName(identifier)
            self.dataLabel.setObjectName(identifier)
        
        self.addWidget(TextLabel)
        self.addWidget(self.dataLabel)
    
    def setValue(self,value):
        self.dataLabel.setText(str(value))
        
class ProgressBar(QtWidgets.QVBoxLayout):
    def __init__(self):
        super(ProgressBar,self).__init__()
        
        self.setContentsMargins(15,0,15,0)
        
        
        Row1 = QtWidgets.QHBoxLayout()
        Row1.setContentsMargins(0,0,0,0)
        
        self.completionLabel = QtWidgets.QLabel()
        self.completionLabel.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        self.progressLabel = QtWidgets.QLabel()
        self.progressLabel.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        
        Row1.addWidget(self.completionLabel)
        Row1.addWidget(self.progressLabel)
        
        
        self.frame = QtWidgets.QFrame()
        self.frame.setObjectName("ProgressBarBackground")
        
        BarLayout = QtWidgets.QHBoxLayout()
        BarLayout.setContentsMargins(0,0,0,0)
        BarLayout.setSpacing(0)
        
        self.redeemedBar = QtWidgets.QFrame()
        self.redeemedBar.setObjectName("RedeemedMeritsBar")
        
        self.underminedActiveBar = QtWidgets.QFrame()
        self.underminedActiveBar.setObjectName("UnderminedActiveMeritsBar")
        
        self.underminedInactiveBar = QtWidgets.QFrame()
        self.underminedInactiveBar.setObjectName("UnderminedInactiveMeritsBar")
        
        self.frame.setLayout(BarLayout)
        
        BarLayout.addWidget(self.redeemedBar)
        BarLayout.addWidget(self.underminedInactiveBar)
        BarLayout.addWidget(self.underminedActiveBar)
        BarLayout.addStretch(0)
        
        
        Row2 = QtWidgets.QHBoxLayout()
        Row2.setContentsMargins(15,0,15,0)
        
        Row2.addSpacing(15)
        Row2.addWidget(self.frame)
        Row2.addSpacing(15)
        
        self.addLayout(Row1)
        self.addLayout(Row2)
        
    def setProgress(self,systemTrigger,meritsTotal,meritsRedeemed,activeUnderminedMerits,inactiveUnderminedMerits):
        if systemTrigger > meritsTotal:
            self.completionLabel.setText("Completion: {0}%".format(int(meritsTotal/systemTrigger*100)))
        else:
            self.completionLabel.setText("Completion: DUNKED!")
        self.progressLabel.setText("{0}/{1} merits".format(meritsTotal,systemTrigger))
            
        if systemTrigger > 0:
            barWidth = self.frame.childrenRegion().boundingRect().width()
            redeemedBarWidth = min(int(barWidth*meritsRedeemed/systemTrigger),barWidth)
            activeBarWidth = min(int(barWidth*activeUnderminedMerits/systemTrigger),barWidth-redeemedBarWidth)
            inactiveBarWidth = min(int(barWidth*inactiveUnderminedMerits/systemTrigger),barWidth-redeemedBarWidth-activeBarWidth) 
            
            self.redeemedBar.setFixedWidth(redeemedBarWidth)
            self.underminedActiveBar.setFixedWidth(activeBarWidth)
            self.underminedInactiveBar.setFixedWidth(inactiveBarWidth)
        else:
            self.completionLabel.setText("Completion: 0%")
            self.redeemedBar.setFixedWidth(0)
            self.underminedActiveBar.setFixedWidth(0)
            self.underminedInactiveBar.setFixedWidth(0)

TOP_LEVEL_CSS ="""
QMainWindow {Background-Color:#071519; padding: 0px}
QWidget { padding: 0px; border: 0px; Background-Color: rgba(0,0,0,0) }

QLabel {Color: #58CFFA;}
QLabel#PinkText {Color: #FF56B3;}
QLabel#GreenText {Color: #4CAF0B;}
QLabel#OrangeText {Color: #F48D1C;}

.QFrame {Background-Color:#3B2049;border: 6px ridge #4D2973}

QLineEdit,QSpinBox {Color: #58CFFA; Background-Color:#3B2049}

QFrame#RedeemedMeritsBar {Background-Color: #4CAF0B; border: 4px solid #57C60D}
QFrame#UnderminedActiveMeritsBar {Background-Color: #4AB1D3; border: 4px solid #52C3E5}
QFrame#UnderminedInactiveMeritsBar {Background-Color: #4AB1D3; border: 4px solid #52C3E5}
QFrame#RedeemedMeritsBar, QFrame#UnderminedActiveMeritsBar,QFrame#UnderminedInactiveMeritsBar {border-style: outset none outset none}

QFrame#ProgressBarBackground {Background-Color:#5B5B60;min-height:30px;border: 8px ridge #6F6F77}

"""
PROGRESS_BAR_COLORS = [
    "#4CAF0B",
    "#4AB1D3",
    "#F48D1C"
]
        