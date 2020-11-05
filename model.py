"""The model for UnderTracker. Controls all the data relevant to undermining"""

import math, pyperclip

MERITS_PER_KILL = 30

class Session():
    def __init__():
        self.systemName = ""
        self.systemTrigger = 0
        self.meritsRedeemed = 0
        self.meritsTotal = 0
        self.meritsNeeded = 0
        
        self.totalUnderminedMerits = 0
        self.activeUnderminedMerits = 0
        self.inactiveUnderminedMerits = 0

        self.meritsPerUnderminer = 0
        self.meritsPerUnderminerRemaining = 0
        self.killsPerUnderminer = 0
        
        self.activeUnderminers = 0
        
        self.underminers = []
        
    def recalculateMerits(self):
        """calculates all merit values and updates target merits of each underminer"""
        self.meritsTotal = self.meritsRedeemed + self.totalUnderminedMerits
        self.meritsNeeded = self.systemTrigger - meritsTotal
        if self.meritsNeeded > 0:
            self.meritsPerUnderminer = math.ceil((self.systemTrigger - self.meritsRedeemed)/max(1,self.activeUnderminers))
            self.meritsPerUnderminerRemaining = math.ceil((self.systemTrigger - self.meritsRedeemed - self.totalUnderminedMerits)/max(1,self.activeUnderminers))
            self.killsPerUnderminer = math.ceil(self.meritsPerUnderminerRemaining / MERITS_PER_KILL)
        else:
            self.meritsPerUnderminer = 0
            self.meritsPerUnderminerRemaining = 0
            self.killsPerUnderminer = 0
        
        for miner in self.underminers:
            miner.setTargetMerits(miner.underminedMerits + self.meritsPerUnderminerRemaining)
            
    def setSystemTrigger(self,newTrigger):
        """sets the system trigger"""
        self.systemTrigger = newTrigger
        self.recalculateMerits()
        
    def setSystemName(self,newName):
        """sets the system name"""
        self.systemName = newName
        
    def setMeritsRedeemed(self,newRedeemed):
        """sets the redeemed merits"""
        self.meritsRedeemed = newRedeemed
        self.recalculateMerits()
            
    def updateUnderminerMerits(self):
        """Recalculates merits when an underminer's merits changes"""
        self.activeUnderminedMerits = 0
        self.inactiveUnderminedMerits = 0
        for miner in self.underminers:
            if miner.isActive:
                self.activeUnderminedMerits += miner.underminedMerits
            else:
                self.inactiveUnderminedMerits += miner.underminedMerits
        self.recalculateMerits()
    
    def updateActiveUnderminers(self):
        """Recalculates things based on how many active underminers"""
        self.activeUnderminers = 0
        self.activeUnderminedMerits = 0
        self.inactiveUnderminedMerits = 0
        for miner in self.underminers:
            self.activeUnderminers += miner.isActive
            if miner.isActive:
                self.activeUnderminedMerits += miner.underminedMerits
            else:
                self.inactiveUnderminedMerits += miner.underminedMerits
        self.recalculateMerits()
        
    def createDiscordPaste(self):
        """creates a string for pasting into discord to show system completion"""
        if self.systemTrigger == 0:
            # play a sound (hopefully) so the user knows something is wrong
            print("\a")
            return
        Components = ["""__**{0}:**__""".format(self.systemName.upper())]
        Components.extend([(miner.associatedUser and "@"+miner.associatedUser.discordHandle or miner.underminerName)+": +"+miner.underminedMerits for miner in self.underminers])
        Components.append("""**Total: +{0}** {1}/{2}""".format(self.totalUnderminedMerits, self.meritsTotal, self.systemTrigger))
        if self.meritsNeeded > 0:
            Components.append("""{0}% complete""".format(int(self.meritsTotal/systemTrigger)))
        else:
            Components.append("""**Dunked!**""")
        
        pasteString = "\n".join(Components)
        
        pyperclip.copy(pasteString)
        
    def createUnderminer(self):
        self.underminers.append(Underminer(self))
        
    def removeUnderminer(self,underminer):
        try:
            self.underminers.remove(self.underminers.index(underminer))
            self.updateActiveUnderminers()
        except:
            #cry about it I guess
            None
            
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
        self.underminerName = ""
        self.isActive = False
        self.underminedMerits = 0
        self.targetMerits = 0
        self.associatedUser = None
        
        self.setActive()
        
    def setMerits(self,merits):
        """sets the merits of the underminer"""
        self.underminedMerits = merits
        self.session.updateUnderminerMerits()
        
    def dumpMerits(self):
        """transfers the merits to redeemed and removes them from the underminer"""
        self.session.dumpUnderminerMerits(self.underminedMerits,self.isActive)
        self.underminedMerits = 0
        
    def setUsername(self,username):
        """sets the username of the underminer"""
        self.underminerName = username
        
    def setAssociatedUser(self,associatedUser):
        """sets the UserProxy of the underminer for discord integration"""
        self.associatedUser = associatedUser
        
    def setTargetMerits(self,target):
        """sets the underminer's target merits"""
        self.targetMerits = target
        
    def setInactive(self):
        """sets the underminer to inactive, so they are not considered for needed merits"""
        self.isActive = False
        self.session.updateActiveUnderminers()
        
    def setActive(self):
        """sets the underminer to active to include them for needed merits"""
        self.isActive = True
        self.session.updateActiveUnderminers()
        
    def toggleActive(self):
        if self.isActive:
            self.setInactive()
        else:
            self.setActive()
            
    def remove(self):
        """deletes the underminer and gets rid of their merits"""
        self.session.removeUnderminer(self)