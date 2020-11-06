
MERITS_PER_KILL = 30

OWNERSHIP_CODES = [
"NB", # nobody
"ZH",#: 'Zachary Hudson',
"EM",#: 'Edmund Mahon',
"AD",#: 'Aisling Duval',
"ALD",#: 'Arissa Lavingy-Duval',
"DP",#: 'Denton Patreus',
"YG",#: 'Yuri Grom',
"PA",#: 'Pranav Antal',
'FC',#: 'Felicia Winters',
'LYR',#: 'Li Yong-Rui',
'ACD',#: 'Archon Delaine',
'ZT'#: 'Zemina Torval'
]

systems = []

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
        
class Sys():
    def __init__(self,name,systemTrigger, owner = None):
        self.name = name
        self.systemTrigger = systemTrigger
        self.owner = owner
        add_system(self)

    def set_owner(self,owner):
        self.owner = owner


_hudson = [
    Sys("lhs 2088",67606),
    Sys("groombridge 1618",75359),
    Sys("caspatsuria",9366),
    Sys("col 258 sector cy-n b21-0",9718),
    Sys("lhs 3447",13180),
    Sys("ltt 9795",11812),
    Sys("burr",13692),
    Sys("lushertha",55021),
    Sys("lhs 1541",22722),
    Sys("sol",33998),
    Sys("anlave",47295),
    Sys("rana",20679),
    Sys("lhs 3749",17419),
    Sys("lp 291-34",18283),
    Sys("rati irtii",10436),
    Sys("phanes",23075),
    Sys("atropos",13751),
    Sys("mulungu",13282),
    Sys("onduwatya",10837),
    Sys("nltt 46403",11134),
    Sys("gcrv 2743",11924),
    Sys("hyades sector gh-v d2-135",12007),
    Sys("phra mool", 12098),
    Sys("aornum",13810),
    Sys("othime", 12889),
    Sys("clayahu",9826),
    Sys("adeo",13260),
    Sys("gliese 868",14768),
    Sys("wat yu",17662),
    Sys("wolf 906",15554),
    Sys("arnemil",15968),
    Sys("abi",16695),
    Sys("37 xi bootis",36573),
    Sys("tun",28974),
    Sys("shoujeman",24937),
    Sys("dongkum",13102),
    Sys("kaushpoos",13274),
    Sys("rho capricorni",10762),
    Sys("jiuyou",14522),
    Sys("lung",30172),
    Sys("vega",35671),
    Sys("39 serpentis", 17430),
    Sys("alpha fornacis",14977),
    Sys("lenty", 9606),
    Sys("lhs 1197", 15150),
    Sys("mariyacoch",12336), 
    Sys("g 250-34", 29849),
    Sys("brhitzameno", 25758),
    Sys("mislika",12389),
    Sys("bd+42 3917",14630),
    Sys("ptah",13988),
    Sys("ross 33", 27471),
    Sys("epsilon scorpii", 12959),
    Sys("kanus", 11494),
    Sys("ltt 15574", 12276),
    Sys("hr 2776", 12047),
    Sys("lhs 3885", 18914), 
    Sys("16 cygni", 17159),
    Sys("wolf 25", 23151),
    Sys("wolf 867", 17605),
    Sys("14 geminorum", 18484),
    Sys("venetic", 14018),
    Sys("gilgamesh", 14194),
    Sys("lhs 3577", 25544),
    Sys("neits", 12215), 
    Sys("parutis", 18589),
    Sys("gd 219", 14686),
    Sys("lalande 39866", 14261),
    Sys("nltt 46621", 27172),
    Sys("mombaluma", 16052),
    Sys("lhs 1681", 19144),
    Sys("mantxe", 13269), 
    Sys("mulachi", 16178),
    Sys("ltt 15449", 14504),
    Sys("allowini", 10798),
    Sys("lhs 6427", 21671)
]
_winters = [
    Sys("kanati", 21793),
    Sys("binjamingi",19704),
    Sys("erivit", 19490),
    Sys("skardee", 13171),
    Sys("uteran",16765),
    Sys("fousang",20813),
    Sys("kali",149040),
    Sys("sosong",12456),
    Sys("carnoeck",15441),
    Sys("lp 906-9",16632),
    Sys("sanos",16354),
    Sys("sawali",13733),
    Sys("odondage",13169),
    Sys("neali",11274),
    Sys("169 g. canis majoris",11037),
    Sys("albicevci",8873),
    Sys("velians",9146),
    Sys("hip 39908",8385),
    Sys("hip 38747",8483),
    Sys("malgariji",7184),
    Sys("hip 50489", 7699),
    Sys("nltt 19808", 36272),
    Sys("54 g. antlia",21600),
    Sys("18 puppis", 51219),
    Sys("neche",37929),
    Sys("skeggiko o",13659),
    Sys("marahli",15802),
    Sys("lhs 1887",18366),
    Sys("momoirent",21041),
    Sys("lhs 235", 15010),
    Sys("morixa",15230),
    Sys("fan yin",22411),
    Sys("elli", 19684),
    Sys("taexalk",9121),
    Sys("ragapajo",16443),
    Sys("mexicatese",32258),
    Sys("oscabi",8192),
    Sys("lft 601", 20091),
    Sys("kaura",16546),
    Sys("mendindui",15229),
    Sys("namte",24364),
    Sys("lhs 1928", 18696),
    Sys("ahemakino",7825)
]
_mahon = [
    Sys("san tu", 17576),
    Sys("akheilos", 32625),
    Sys("ao kond", 9613),
    Sys("chukchan",9528)
]


for system in _hudson:
    system.set_owner("ZH")
for system in _winters:
    system.set_owner("FC")
for system in _mahon:
    system.set_owner("EM")