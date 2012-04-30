import os
import datetime
import ConfigParser

config = ConfigParser.ConfigParser()

now = datetime.datetime.now()

sharesdir = "/home/jono/Ubuntu One/Shared With Me/"

userlist = []
trophycount = 0
usercount = 0

users = ""

for r,d,f in os.walk(sharesdir):
    userlist.append(r.split("/")[5].split(" ")[0])
    for i in f:
        if i.endswith(".trophy.asc"):
            trophycount = trophycount + 1

finaluserlist = list(set(userlist))

for user in finaluserlist:
    users = users + user + " "
    usercount = usercount + 1

today = now.strftime("%Y-%m-%d")

config.add_section("general")
config.set("general", "totalusers", len(finaluserlist))
config.set("general", "totaltrophies", trophycount)

config.add_section("users")
config.set("users", today+"-users", users.lstrip(" "))
config.set("users", today+"-total", usercount)

config.add_section("trophies")
config.set("trophies", today, trophycount)

cfile = "/home/jono/matrixstats.txt"

with open(cfile, 'wb') as configfile:
    config.write(configfile)
