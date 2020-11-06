"""Reads from the users file"""

USERS_FILE = "users.txt"
usrlines = []

users = []

def find_user_by_number(number):
    if number >= len(users) or number < 0:
        return None
    return users[number]

def get_user_names():
    return [user.truename for user in users]

class UserProxy():
    def __init__(self,discordHandle,truename = None):
        self.discordHandle = discordHandle
        self.truename = truename or discordHandle
        users.append(self)

with open(USERS_FILE,"r") as usrfile:
    usrlines = [[data.rstrip() for data in line.split(",")] for line in usrfile.readlines()]
    usrfile.close()


for props in usrlines:
    if "##" in props[0]:
        continue
    if len(props) == 2:
        try:
            UserProxy(*props)
        except:
            None
