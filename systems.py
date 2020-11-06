"""Reads from the systems file and writes any changes to the trigger"""

SYSTEMS_FILE = "systems.txt"
syslines = []

systems = []

class Sys():
    
    OwnershipCodes = [
    "NB", # nobody
    'ZT',#: 'Zemina Torval'
    "AD",#: 'Aisling Duval',
    "ALD",#: 'Arissa Lavingy-Duval',
    "DP",#: 'Denton Patreus',
    "ZH",#: 'Zachary Hudson',
    'FW',#: 'Felicia Winters',
    'LYR',#: 'Li Yong-Rui',
    'ACD',#: 'Archon Delaine',
    "PA",#: 'Pranav Antal',
    "YG",#: 'Yuri Grom',
    "EM"#: 'Edmund Mahon',
    ]
    
    def __init__(self,name,owner,systemTrigger,index):
        self.index = index
        self.name = name
        self.systemTrigger = int(systemTrigger)
        self.owner = owner.upper() in self.OwnershipCodes and self.OwnershipCodes.index(owner.upper()) or 0
        add_system(self)
        
    def changeSystemTrigger(self,newTrigger):
        if self.systemTrigger == newTrigger:
            return
        
        self.systemTrigger = newTrigger
        try:
            syslines[self.index][2] = str(self.systemTrigger)
            with open(SYSTEMS_FILE,"w") as sysfile:
                sysfile.writelines(['\n'.join([', '.join(line) for line in syslines])])
                sysfile.close()
        except:
            None

def find_system_by_number(number):
    if number >= len(systems) or number < 0:
        return None
    return systems[number]

def add_system(system):
    # add systems in alphabetical order
    if len(systems) == 0:
        systems.append(system)
    else:
        for i in range(len(systems)):
            if systems[i].name > system.name:
                systems.insert(i,system)
                return
        systems.append(system)
            
def get_system_names():
    return [system.name for system in systems]


# add the systems to the systems list
with open(SYSTEMS_FILE,"r") as sysfile:
    syslines = [[data.strip() for data in line.split(",")] for line in sysfile.readlines()]
    sysfile.close()

for i in range(len(syslines)):
    props = syslines[i]
    if "##" in props[0]:
        continue
    if len(props) == 3:
        try:
            int(props[2])
            Sys(*props,i)
        except:
            None
        