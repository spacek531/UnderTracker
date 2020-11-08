from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

import resources
import model, controller

NUMBER_OF_UNDERMINERS = 16

TitleFont = QtGui.QFont("Consolas",16,100)
SubtitleFont = QtGui.QFont("Consolas",14,100)
BodyFont = QtGui.QFont("Lucida Sans",16,100)
SubBodyFont = QtGui.QFont("Lucida Sans",12,100)
SmallFont = QtGui.QFont("Lucida Sans",10,100)

class SystemSelector(QtWidgets.QComboBox):
    def __init__(self,session):
        super(SystemSelector,self).__init__()
        self.setFont(BodyFont)
        self.setEditable(True)
        self.controller = controller.SystemController(self,session)
        

class UsernameSelector(QtWidgets.QComboBox):
    def __init__(self,miner):
        super(UsernameSelector,self).__init__()
        self.setFont(SubBodyFont)
        self.setEditable(True)
        self.controller = controller.UsernameController(self,miner)        

class NumberInput(QtWidgets.QSpinBox):
    def __init__(self,callback):
        super(NumberInput,self).__init__()
        self.setFont(BodyFont)
        self.setMinimum(0)
        self.setMaximum(999999)
        self.setSingleStep(30)
        self.controller = controller.NumberController(self,callback)

class PushButton(QtWidgets.QPushButton):
    def __init__(self,callback):
        super(PushButton,self).__init__()
        self.controller = controller.PushButtonController(self,callback)

class ValueLabel(QtWidgets.QVBoxLayout):
    def __init__(self,description,identifier = None):
        super(ValueLabel,self).__init__()
        
        self.setContentsMargins(5,0,0,5)
        
        self.textLabel = QtWidgets.QLabel()
        self.textLabel.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.textLabel.setText(description)
        self.textLabel.setFont(SubtitleFont)
        
        self.dataLabel = QtWidgets.QLabel()
        self.dataLabel.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.dataLabel.setFont(BodyFont)

        if identifier:
            self.textLabel.setObjectName(identifier)
            self.dataLabel.setObjectName(identifier)
        
        self.addWidget(self.textLabel)
        self.addWidget(self.dataLabel)
    
    def setValue(self,value):
        self.dataLabel.setText(str(value))
        
    def setColor(self,colorString = None):
        if colorString:
            self.dataLabel.setStyleSheet("QLabel {{ color: \#{0}}}".format(colorString))
            self.textLabel.setStyleSheet("QLabel {{ color: \#{0}}}".format(colorString))
        else:
            self.dataLabel.setStyleSheet("")
            self.textLabel.setStyleSheet("")

class MainWindow(QtWidgets.QMainWindow):

    def getOwnerSprite(self,ownerId):
        if ownerId == 0:
            return QtGui.QPixmap()
        else:
            return QtGui.QPixmap(self.OwnerSheet.copy(QtCore.QRect(0,100*(ownerId-1),200,100)))
        
    def createInputBoxFrame(self,contentWidget,description,identifier = None):
        L1 = QtWidgets.QVBoxLayout()
        L1.setContentsMargins(0,0,0,0)
        L1.addStretch(0)
        
        TextLabel = QtWidgets.QLabel()
        TextLabel.setFont(SubtitleFont)
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
    
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("[BRGD] Undermining Tracker")
        self.setStyleSheet(TOP_LEVEL_CSS)
        self.VLayout = QtWidgets.QVBoxLayout()
        self.VLayout.setContentsMargins(0,0,0,0)
        self.VLayout.setSpacing(0)
        CentralWidget = QtWidgets.QWidget()
        CentralWidget.setLayout(self.VLayout)
        CentralWidget.setObjectName("CentralWidget")
        CentralWidget.setFont(TitleFont)
        self.setCentralWidget(CentralWidget)

        self.session = model.Session(self)  
        
    
        self.OwnerSheet = QtGui.QPixmap(":/resources/SPRITE_BLACK.png")        
        
        self.createHeader()
        self.createManagementSection()
        self.createReportingSection()
        self.createUnderminerGrid()
        self.createCopyButton()
        
        for _ in range(NUMBER_OF_UNDERMINERS):
            self.session.createUnderminer()
        
    def addWidget(self,widget):
        self.VLayout.addWidget(widget)
    
    def addLayout(self,layout):
        self.VLayout.addLayout(layout)
        
    def addSpacing(self,space):
        self.VLayout.addSpacing(space)
        
    def createHeader(self):
        ImageLabel = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(":/resources/STARLIGHT_BRIGADE_UM.png")
        ImageLabel.setPixmap(pixmap)
        ImageLabel.setMinimumSize(650,100)
        ImageLabel.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        
        HorizontalBar = QtWidgets.QFrame()
        HorizontalBar.setFrameShape(QtWidgets.QFrame.HLine)
        HorizontalBar.setFrameShadow(QtWidgets.QFrame.Raised)
        HorizontalBar.setLineWidth(7)
        
        self.addWidget(ImageLabel)
        
        self.addWidget(HorizontalBar)
        
    def createManagementSection(self):
        
        Row1 = QtWidgets.QHBoxLayout()
        Row2 = QtWidgets.QHBoxLayout()
        
        Row1.setContentsMargins(15,5,15,0)
        Row2.setContentsMargins(15,0,15,10)
        
        self.systemSelector = SystemSelector(self.session)
        
        Row1.addLayout(self.createInputBoxFrame(self.systemSelector,"System"))
        Row1.addSpacing(15)
        
        self.powerLogo = QtWidgets.QLabel()
        self.powerLogo.setMinimumSize(200,100)
        
        self.bonusWidget = NumberInput(self.session.setPowerBonus)
        self.bonusWidget.setMaximum(50)
        self.bonusWidget.setSuffix("%")
        self.bonusWidget.setSingleStep(1)
        self.bonusWidget.setFont(BodyFont)
        
        L1 = QtWidgets.QVBoxLayout()
        L1.setContentsMargins(0,0,0,0)
        L1.addStretch(0)
        
        TextLabel = QtWidgets.QLabel()
        TextLabel.setText("Defense Bonus")
        TextLabel.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        TextLabel.setFont(SubtitleFont)
            
        L1.addWidget(TextLabel)
        
        Frame = QtWidgets.QFrame()
        Frame.setObjectName("InputFrame")
        
        L2 = QtWidgets.QVBoxLayout()
        L2.setContentsMargins(0,0,0,0)
        Frame.setLayout(L2)
        
        L2.addWidget(self.bonusWidget)
        L1.addWidget(Frame)
        L1.addStretch(0)
        
        
        Row1.addLayout(L1)
        Row1.addSpacing(0)
        Row1.addWidget(self.powerLogo)
        Row1.addSpacing(0)
        
        self.triggerInput = NumberInput(self.session.setSystemTrigger)
        self.redeemedInput = NumberInput(self.session.setMeritsRedeemed)
        #Row2.addLayout(L1)
        #Row2.addSpacing(15)
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
        self.meritsPerUnderminerRemainingLabel = ValueLabel("Remaining Merits\nPer Commander","OrangeText")
        self.meritsPerUnderminerLabel = ValueLabel("Total Merits\nPer Commander")
        self.killsPerUnderminerLabel = ValueLabel("Remaining Kills\nPer Commander","OrangeText")
        
        Row1.addLayout(self.totalUnderminedMeritsLabel)
        Row1.addLayout(self.totalUnderminersLabel)
        #Row1.addLayout(self.inactiveUnderminedMeritsLabel)
        Row1.addLayout(self.meritsPerUnderminerLabel)
        
        Row2 = QtWidgets.QHBoxLayout()
        Row2.setContentsMargins(15,0,15,0)
        

        Row2.addLayout(self.meritsNeededLabel)        
        Row2.addLayout(self.killsPerUnderminerLabel)
        Row2.addLayout(self.meritsPerUnderminerRemainingLabel)
        
        self.addLayout(Row1)
        self.addLayout(Row2)
        
        self.updateMerits()
        self.updateUnderminers()
        
    def createUnderminerGrid(self):
        self.underminerGrid = UnderminerGrid()
        self.addLayout(self.underminerGrid)
    
    def createCopyButton(self):
        
        HLayout = QtWidgets.QHBoxLayout()
        HLayout.setContentsMargins(5,5,5,10)
        self.copyButton = PushButton(self.session.createDiscordPaste)
        
        self.copyButton.setText("Copy to clipboard")
        
        HLayout.addStretch()
        HLayout.addWidget(self.copyButton)
        HLayout.addStretch()
        self.addLayout(HLayout)
        
    
    def createUnderminer(self,miner):
        card = UnderminerCard(miner)
        self.underminerGrid.addUnderminer(card)
        return card
    
    ## now for the updater functions #
    
    def setSystemOwner(self,ownerId,bonus):
        self.powerLogo.setPixmap(self.getOwnerSprite(ownerId))
        self.bonusWidget.setValue(bonus)
    
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
        
        WinnerColor = "4CAF0B"
        
        if meritsNeeded <= 0 and systemTrigger > 0:
            self.totalUnderminedMeritsLabel.setColor(WinnerColor)
            self.meritsNeededLabel.setColor(WinnerColor)
            self.meritsPerUnderminerRemainingLabel.setColor(WinnerColor)
            self.meritsPerUnderminerLabel.setColor(WinnerColor)
            self.killsPerUnderminerLabel.setColor(WinnerColor)
            self.totalUnderminersLabel.setColor(WinnerColor)
        else:
            self.totalUnderminedMeritsLabel.setColor()
            self.meritsNeededLabel.setColor()
            self.meritsPerUnderminerRemainingLabel.setColor()
            self.meritsPerUnderminerLabel.setColor()
            self.killsPerUnderminerLabel.setColor()
            self.totalUnderminersLabel.setColor()
          
        self.triggerInput.setValue(systemTrigger)
        self.redeemedInput.setValue(meritsRedeemed)
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
        
class ProgressBar(QtWidgets.QVBoxLayout):
    WinnerColor = "4CAF0B"
    
    def __init__(self):
        super(ProgressBar,self).__init__()
        
        self.setContentsMargins(15,0,15,0)
        
        Row1 = QtWidgets.QHBoxLayout()
        Row1.setContentsMargins(0,0,0,0)
        
        self.completionLabel = QtWidgets.QLabel()
        self.completionLabel.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.completionLabel.setFont(TitleFont)

        self.progressLabel = QtWidgets.QLabel()
        self.progressLabel.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.progressLabel.setFont(TitleFont)
        
        Row1.addWidget(self.completionLabel)
        Row1.addWidget(self.progressLabel)
        
        
        self.frame = QtWidgets.QFrame()
        self.frame.setObjectName("ProgressBarBackground")
        
        BarFrameLayout = QtWidgets.QHBoxLayout()
        BarFrameLayout.setContentsMargins(0,0,0,0)
        
        BarLayout = QtWidgets.QHBoxLayout()
        BarLayout.setContentsMargins(0,0,0,0)
        BarLayout.setSpacing(0)
        
        self.redeemedBar = QtWidgets.QFrame()
        self.redeemedBar.setObjectName("RedeemedMeritsBar")
        
        self.underminedActiveBar = QtWidgets.QFrame()
        self.underminedActiveBar.setObjectName("UnderminedActiveMeritsBar")
        
        self.underminedInactiveBar = QtWidgets.QFrame()
        self.underminedInactiveBar.setObjectName("UnderminedInactiveMeritsBar")
        
        
        BarHolder = QtWidgets.QWidget()
        BarFrameLayout.addWidget(BarHolder)
        
        BarHolder.setLayout(BarLayout)
        
        self.frame.setLayout(BarFrameLayout)
        
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
        
        if meritsTotal >= systemTrigger:
            self.completionLabel.setText("Completion: DUNKED!")
            self.completionLabel.setStyleSheet("QLabel {{ color: #{0}}}".format(ProgressBar.WinnerColor))
            self.progressLabel.setStyleSheet("QLabel {{ color: #{0}}}".format(ProgressBar.WinnerColor))
        else:
            self.completionLabel.setText("Completion: {0}%".format(int(meritsTotal/systemTrigger*100)))
            self.completionLabel.setStyleSheet("")
            self.progressLabel.setStyleSheet("")
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
            self.completionLabel.setStyleSheet("")
            self.progressLabel.setStyleSheet("")
            
class UnderminerGrid(QtWidgets.QHBoxLayout):
    maxRows = 8
    spacerColumnWidth = 10
    def __init__(self):
        super(UnderminerGrid,self).__init__()
        self.setContentsMargins(5,0,0,5)
        self.setSpacing(2)
        
        self.columns = []
        
        self.currentRow = 0
        self.createColumn()
        
    def createColumn(self):
        Column = QtWidgets.QVBoxLayout()
        Column.setContentsMargins(0,0,0,0)
        self.addLayout(Column)
        self.columns.append(Column)
        
    def addUnderminer(self,card):
        self.columns[len(self.columns)-1].addLayout(card)
        
        self.currentRow += 1
        if self.currentRow == self.maxRows:
            self.currentRow = 0
            self.createColumn()
            
class UnderminerCard(QtWidgets.QHBoxLayout):
    
    ActiveStyle = """QPushButton {Color: #FFFFFF; Background-Color: #4CAF0B; border: 3px outset #57C60D}"""
    InactiveStyle = """QPushButton {Color: #FFFFFF; Background-Color: #E50091; border: 3px outset #FF9BC9}"""
    
    ButtonSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Preferred)
    UsernameSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,QtWidgets.QSizePolicy.Preferred)
    MeritsSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Preferred)
        
    def createInputOutline(self,contentWidget= None):

        Frame = QtWidgets.QFrame()
        Frame.setObjectName("InputFrame")
        L2 = QtWidgets.QHBoxLayout()
        L2.setContentsMargins(0,0,0,0)
        Frame.setLayout(L2)
        if contentWidget:
            L2.addWidget(contentWidget)
        
        return Frame
    
    def __init__(self,miner):
        super(UnderminerCard,self).__init__()
        self.miner = miner
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(0)
        
        ButtonLayout = QtWidgets.QHBoxLayout()
        ButtonLayout.setContentsMargins(0,4,4,4)
        
        self.activeButton = PushButton(miner.toggleActive)
        
        self.activeButton.setFont(SmallFont)
        self.activeButton.setText("I")
        self.activeButton.setStyleSheet(self.ActiveStyle)
        self.activeButton.setMinimumWidth(18)
        self.activeButton.setSizePolicy(self.ButtonSizePolicy)
        """
        self.dumpButton = PushButton(miner.dumpMerits)        
        self.dumpButton.setFont(SmallFont)
        self.dumpButton.setText("D")
        self.dumpButton.setMinimumWidth(18)
        self.dumpButton.setSizePolicy(self.ButtonSizePolicy)
        """
        ButtonLayout.addWidget(self.activeButton)
        #ButtonLayout.addWidget(self.dumpButton)
        
        self.usernameInput = UsernameSelector(miner)
        
        self.meritInput = NumberInput(miner.setMerits)
        self.meritInput.setFont(SubBodyFont)
        self.meritInput.setMaximum(99999)
        
        InputFrame = self.createInputOutline(self.usernameInput)
        InputFrame.setSizePolicy(self.UsernameSizePolicy)
        
        InputFrame.layout().addWidget(self.usernameInput)
        InputFrame.layout().addWidget(self.meritInput)
        
        self.target = QtWidgets.QLabel()
        self.target.setObjectName("OrangeText")
        self.target.setFont(SmallFont)
        self.target.setMinimumWidth(60)

        self.addLayout(ButtonLayout)
        self.addWidget(InputFrame)
        self.addWidget(self.target)
    
    def setTargetMerits(self,target):
        if target < 0:
            self.target.setText("")
        else:
            self.target.setText("of {0}".format(target))
            
    def setUsername(self,username):
        self.usernameInput.setText(username)
    
    def setMerits(self,merits):
        self.meritInput.setValue(merits)
    
    def setActive(self):
        self.activeButton.setText("I")
        self.activeButton.setStyleSheet(UnderminerCard.ActiveStyle)
    
    def setInactive(self):
        self.activeButton.setText("O")
        self.activeButton.setStyleSheet(UnderminerCard.InactiveStyle)
            
    
#QMainWindow {Background-Color:#071519; padding: 0px}
TOP_LEVEL_CSS ="""
QMainWindow {Background-Color:#FFFFFF; padding: 0px}
QWidget { padding: 0px; border: 0px; Background-Color: rgba(0,0,0,0) }

QLabel {Color: #58CFFA;}
QLabel#PinkText {Color: #E50091;}
QLabel#GreenText {Color: #4CAF0B;}
QLabel#OrangeText {Color: #F48D1C;}

.QFrame {Background-Color:#001E4C;border: 6px ridge #002A6B}

QLineEdit,QSpinBox,QComboBox {Color: #FF7CB7; Background-Color:#001E4C; border-color: #002A6B}
QComboBox::drop-Down {Background-Color:#FF7CB7;border: 2px outset #FF9BC9}
QComboBox::down-arrow {
    Color: #001E4C;
}
QComboBox QAbstractItemView {
Color: #FF7CB7;
}

QPushButton {Color: #FFFFFF; Background-Color: #4CAF0B; border: 4px outset #57C60D}

QFrame#RedeemedMeritsBar {Background-Color: #4CAF0B; border: 4px solid #57C60D}
QFrame#UnderminedActiveMeritsBar {Background-Color: #4AB1D3; border: 4px solid #52C3E5}
QFrame#UnderminedInactiveMeritsBar {Background-Color: #4AB1D3; border: 4px solid #52C3E5}
QFrame#RedeemedMeritsBar, QFrame#UnderminedActiveMeritsBar,QFrame#UnderminedInactiveMeritsBar {border-style: outset none outset none}

QFrame#ProgressBarBackground {Background-Color:#5B5B60;min-height:30px;border: 8px ridge #6F6F77}

"""