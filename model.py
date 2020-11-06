"""The model for UnderTracker. Controls all the data relevant to undermining"""

import math, pyperclip

MERITS_PER_KILL = 30

class Session():
    def __init__(self,mainWindow):
        self.mainWindow = mainWindow
        
        self.systemName = ""
        self.systemObject = None
        
        self.systemOwner = 0
        self.systemTrigger = 0
        self.meritsTotal = 0
        self.meritsRedeemed = 0
        
        self.activeUnderminedMerits = 0
        self.inactiveUnderminedMerits = 0

        self.totalUnderminedMerits = 0        
        self.meritsNeeded = 0

        self.meritsPerUnderminer = 0
        self.meritsPerUnderminerRemaining = 0
        self.killsPerUnderminer = 0
        
        self.activeUnderminers = 0
        self.totalUnderminers = 0
        
        self.underminers = []
        
    def recalculateMerits(self):
        """calculates all merit values and updates target merits of each underminer"""
        self.meritsTotal = self.meritsRedeemed + self.totalUnderminedMerits
        self.meritsNeeded = max(0,self.systemTrigger - self.meritsTotal)
        if self.meritsNeeded > 0:
            self.meritsPerUnderminer = math.ceil((self.systemTrigger - self.meritsRedeemed)/max(1,self.activeUnderminers))
            self.meritsPerUnderminerRemaining = math.ceil((self.systemTrigger - self.meritsRedeemed - self.totalUnderminedMerits)/max(1,self.activeUnderminers))
            self.killsPerUnderminer = math.ceil(self.meritsPerUnderminerRemaining / MERITS_PER_KILL)
        else:
            self.meritsPerUnderminer = 0
            self.meritsPerUnderminerRemaining = 0
            self.killsPerUnderminer = 0
        
        for miner in self.underminers:
            if self.meritsNeeded > 0:
                miner.setTargetMerits(self.meritsPerUnderminerRemaining)
            else:
                miner.setTargetBlank()
            
        self.mainWindow.updateMerits(self.systemTrigger,self.meritsTotal,self.meritsRedeemed,self.activeUnderminedMerits,self.inactiveUnderminedMerits,self.totalUnderminedMerits,self.meritsNeeded,self.meritsPerUnderminer,self.meritsPerUnderminerRemaining,self.killsPerUnderminer)
        
    def setSystemObject(self,systemObject):
        self.systemObject = None
        if systemObject:
            self.setSystemName(systemObject.name)
            self.setSystemOwner(systemObject.owner)
            self.setSystemTrigger(systemObject.systemTrigger)
            self.systemObject = systemObject
            
    def setSystemTrigger(self,newTrigger):
        """sets the system trigger"""
        self.systemTrigger = newTrigger
        self.recalculateMerits()
        if self.systemObject:
            self.systemObject.changeSystemTrigger(newTrigger)
        # send this to MainWindow?
        
    def setSystemName(self,newName):
        """sets the system name"""
        self.systemName = newName
        # send this to MainWindow?
        
    def setSystemOwner(self,newOwnerId):
        self.systemOwner = newOwnerId
        self.mainWindow.setSystemOwner(newOwnerId)
        # send this to MainWindow
        
    def setMeritsRedeemed(self,newRedeemed):
        """sets the redeemed merits"""
        self.meritsRedeemed = newRedeemed
        self.recalculateMerits()
        # send this to MainWindow?
            
    def updateUnderminerMerits(self):
        """Recalculates merits when an underminer's merits changes"""
        self.totalUnderminedMerits = 0
        self.activeUnderminedMerits = 0
        self.inactiveUnderminedMerits = 0
        for miner in self.underminers:
            self.totalUnderminedMerits += miner.underminedMerits
            if miner.isActive:
                self.activeUnderminedMerits += miner.underminedMerits
            else:
                self.inactiveUnderminedMerits += miner.underminedMerits
        self.recalculateMerits()
    
    def updateActiveUnderminers(self):
        """Recalculates things based on how many active underminers"""
        self.totalUnderminers = 0
        self.activeUnderminers = 0
        self.activeUnderminedMerits = 0
        self.inactiveUnderminedMerits = 0
        for miner in self.underminers:
            self.activeUnderminers += miner.isActive
            self.totalUnderminers += miner.exists
            if miner.isActive:
                self.activeUnderminedMerits += miner.underminedMerits
            else:
                self.inactiveUnderminedMerits += miner.underminedMerits
        self.recalculateMerits()
        self.mainWindow.updateUnderminers(self.activeUnderminers,self.totalUnderminers,self.underminers)
        
    def createDiscordPaste(self):
        """creates a string for pasting into discord to show system completion"""
        if self.systemTrigger == 0:
            # play a sound (hopefully) so the user knows something is wrong
            print("\a")
            return
        Components = ["""__**{0}:**__""".format(self.systemName.upper())]
        for i in range(len(self.underminers)):
            miner = self.underminers[i]
            if miner.exists:
                Components.append("@{0}: +{1}".format(miner.associatedUser and miner.associatedUser.discordHandle or miner.underminerName, miner.underminedMerits))
        
        Components.append("""**Total: +{0}** {1}/{2}""".format(self.totalUnderminedMerits, self.meritsTotal, self.systemTrigger))
        if self.meritsNeeded > 0:
            Components.append("""{0}% complete""".format(int(100*self.meritsTotal/self.systemTrigger)))
        else:
            Components.append("""**Dunked!**""")
        
        pasteString = "\n".join(Components)
        
        pyperclip.copy(pasteString)
        
    def createUnderminer(self):
        Miner = Underminer(self)
        Card = self.mainWindow.createUnderminer(Miner)
        Miner.setCard(Card)
        self.underminers.append(Miner)
        
    def dumpUnderminerMerits(self,merits,active):
        """transfers the specified merits from undermined merits to redeemed merits"""
        self.meritsRedeemed += merits
        self.totalUnderminedMerits -= merits
        if active:
            self.activeUnderminedMerits -= merits
        else:
            self.inactiveUnderminedMerits -= merits
        self.recalculateMerits()
    
class Underminer():
    def __init__(self,session):
        self.session = session
        self.username = ""
        self.isActive = False
        self.exists = False
        self.firstTimeActivation = False
        self.underminedMerits = 0
        self.targetMerits = 0
        self.associatedUser = None
        
    def setCard(self,card):
        self.card = card
        self.setInactive()
        
    def determineIfExists(self):
        self.exists = len(self.username) > 0 or self.isActive or self.underminedMerits
        self.session.updateActiveUnderminers()   
        
    def setMerits(self,merits):
        """sets the merits of the underminer"""
        self.underminedMerits = merits
        self.session.updateUnderminerMerits()
        self.card.setMerits(self.underminedMerits)
        
    def dumpMerits(self):
        """transfers the merits to redeemed and removes them from the underminer"""
        self.session.dumpUnderminerMerits(self.underminedMerits,self.isActive)
        self.underminedMerits = 0
        self.card.setMerits(self.underminedMerits)
        self.determineIfExists()
        
    def setUsername(self,username):
        """sets the username of the underminer"""
        self.username = username
        if not self.firstTimeActivation:
            self.firstTimeActivation = True
            self.setActive()
        #self.card.setUsername(self.username)
        
    def setAssociatedUser(self,associatedUser):
        """sets the UserProxy of the underminer for discord integration"""
        self.associatedUser = associatedUser
        
    def setTargetBlank(self):
        self.card.setTargetMerits(-1)
        
    def setTargetMerits(self,target):
        """sets the underminer's target merits"""
        self.targetMerits = self.underminedMerits + target
        if self.isActive:
            self.card.setTargetMerits(self.targetMerits)
        
    def setInactive(self):
        """sets the underminer to inactive, so they are not considered for needed merits"""
        self.isActive = False
        self.determineIfExists()
        self.card.setInactive()
        self.setTargetBlank()
        
    def setActive(self):
        """sets the underminer to active to include them for needed merits"""
        self.isActive = True
        self.determineIfExists()
        self.card.setActive()
        # the target merits will get set when the session recalculates everything
        
    def toggleActive(self):
        self.firstTimeActivation = True
        if self.isActive:
            self.setInactive()
        else:
            self.setActive()