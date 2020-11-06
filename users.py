

class UserProxy():
    def __init__(self,discordHandle,nicknames,truename = None):
        self.discordHandle = discordHandle
        self.truename = truename
        self.nicknames = nicknames
    def addNicknames(self,nicknames):
        if type(nicknames) == list:
            self.nicknames.extend(nicknames)
        else:
            self.nicknames.append(nicknames)

KNOWN_USERS = [
    # [BRGD] members
    UserProxy("Spacek",["nwspacek","spacek531"],"NWSpacek"),
    UserProxy("jordanindenmark",["deftbridge","deutsche bahn","dadbridge"],"Deftbridge"),
    UserProxy("Ner0",["nero","nero prizak","prizak"], "Nero Prizak"),
    UserProxy("Xenophon117",["xenophon117"],"Xenophon117"),
    UserProxy("djp5",["erkad posner","erkat posner"],"Erkat Posner"),
    UserProxy("donkipunx",["donki","donkipunx","donkipunch"],"Donkipunx"),
    UserProxy("Rasperry",["rasperry","party perry"],"Rasperry"),
    UserProxy("HyrooHimolil",["kate balthazar","chaos agent","fearless leader"],"Kate Balthazar"),
    UserProxy("Avalyn",["avalyndis"],"Avalyndis"),
    UserProxy("UnspeakablePat",["unspeakablepat","speakablepat"],"UnspeakablePat"),
    UserProxy("Terra Sheer",["terra sheer"],"Terra Sheer"),
    UserProxy("SPNKR",["spnkr","spencer"],"SPNKR"),
    UserProxy("otolock",["otolock"],"Otolock"),
    UserProxy("hubcap",["hubcap","hub cap","hub-cap"],"HUB-CAP"),
    UserProxy("Buster",["buster335"],"Buster335"),
    UserProxy("BTEC GLOBAL ELITE",["bertioli"],"Bertioli"),
    UserProxy("Asagi Asagiri",["xenocrunch"],"Xenocrunch"),
    
    
    # other ADC members
    UserProxy("z64555",["z","z64555"],"z64555"),
    UserProxy("schielman",["schielman"],"Schielman"),
    UserProxy("AERO",["aeroassault"],"AEROassault"),
    UserProxy("Cyanidex",["cyanidex"],"Cyanidex"),
    UserProxy("Mo Mo",["mo mo","momo"],"Mo Mo"),
    UserProxy("|3lue|2aven",["|3lue|2aven","blueraven"],"|3lue|2aven"),
    UserProxy("Octavius",["octavius"],"Octavius"),
    UserProxy("Kraig",["kraig lane"],"Kraig Lane"),
    UserProxy("Flebens",["mace cartier","space dad"],"Mace Cartier")
]

def find_user_by_number(number):
    if number >= len(KNOWN_USERS) or number < 0:
        return None
    return KNOWN_USERS[number]

def get_user_names():
    return [user.trueName for user in KNOWN_USERS]

