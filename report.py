import os
import datetime
import ConfigParser
import glob
import time

matrixconfig = ConfigParser.ConfigParser()
matrixconfig.read(os.path.join(os.getenv("HOME"), ".matrix"))

SHARESPATH = matrixconfig.get("matrix", "sharespath") + "/"
ACCOMSPATH = matrixconfig.get("matrix", "accompath")

cfile = os.path.join(os.getenv("HOME"), "matrixstats.txt")
config = ConfigParser.ConfigParser()
config.read(cfile)

now = datetime.datetime.now()

total_users = []
total_trophycount = 0
total_usercount = 0
todaystrophies = 0
today_users = 0
today_newusers = []
today_usernames = ""

users = ""

for r,d,f in os.walk(SHARESPATH):
    total_users.append(r.split("/")[5].split(" ")[0])
    usertime = datetime.datetime.fromtimestamp(os.path.getmtime(r))
    
    for i in f:
        if i.endswith(".trophy.asc"):
            total_trophycount = total_trophycount + 1

userdirs = [name for name in os.listdir(SHARESPATH)
    if os.path.isdir(os.path.join(SHARESPATH, name))]

for u in userdirs:
    usertime = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(SHARESPATH, u)))
    if usertime.date() == now.date():
        today_users = today_users + 1
        today_newusers.append(u.split()[0])

for accom in glob.glob(os.path.join(SHARESPATH, "*", "*", "*.trophy.asc")):
    accomtime = datetime.datetime.fromtimestamp(os.path.getmtime(accom))
    if accomtime.date() == now.date():
        todaystrophies = todaystrophies + 1

final_total_users = list(set(total_users))
final_today_newusers = list(set(today_newusers))

for user in final_total_users:
    users = users + user + " "
    total_usercount = total_usercount + 1

for us in final_today_newusers:
    today_usernames = today_usernames + us + " "
    
today = now.strftime("%Y-%m-%d")

# -------- generate ConfigParser output --------------

if not config.has_section("general"):
    config.add_section("general")

config.set("general", "totalusers", len(final_total_users))
config.set("general", "totaltrophies", total_trophycount)

if not config.has_section("users"):
    config.add_section("users")
    
config.set("users", today+"-usernames", today_usernames)
config.set("users", today+"-total", total_usercount)
config.set("users", today+"-today", today_users)

if not config.has_section("trophies"):
    config.add_section("trophies")
    
config.set("trophies", today+"-total", total_trophycount)
config.set("trophies", today+"-today", todaystrophies)

with open(cfile, 'wb') as configfile:
    config.write(configfile)
