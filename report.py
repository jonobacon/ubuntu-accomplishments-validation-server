import os
import datetime
import ConfigParser
import glob
import time

cfile = "/home/jono/matrixstats.txt"
config = ConfigParser.ConfigParser()
config.read(cfile)

now = datetime.datetime.now()
sharesdir = "/home/jono/Ubuntu One/Shared With Me/"

total_users = []
total_trophycount = 0
total_usercount = 0
todaystrophies = 0
today_users = 0
today_newusers = []

users = ""


for r,d,f in os.walk(sharesdir):
    total_users.append(r.split("/")[5].split(" ")[0])
    usertime = datetime.datetime.fromtimestamp(os.path.getmtime(r))
    
    for i in f:
        if i.endswith(".trophy.asc"):
            total_trophycount = total_trophycount + 1

userdirs = [name for name in os.listdir(sharesdir)
    if os.path.isdir(os.path.join(sharesdir, name))]

for u in userdirs:
    usertime = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(sharesdir, u)))
    if usertime.date() == now.date():
        today_users = today_users + 1
        #today_newusers.append(u.split("/")[5].split(" ")[0])

for accom in glob.glob(os.path.join(sharesdir, "*", "*", "*.trophy.asc")):
    accomtime = datetime.datetime.fromtimestamp(os.path.getmtime(accom))
    if accomtime.date() == now.date():
        todaystrophies = todaystrophies + 1

final_total_users = list(set(total_users))

for user in final_total_users:
    users = users + user + " "
    total_usercount = total_usercount + 1

today = now.strftime("%Y-%m-%d")

if not config.has_section("general"):
    config.add_section("general")

config.set("general", "totalusers", len(final_total_users))
config.set("general", "totaltrophies", total_trophycount)

if not config.has_section("users"):
    config.add_section("users")
    
config.set("users", today+"-users", users.lstrip(" "))
config.set("users", today+"-total", total_usercount)
config.set("users", today+"-today", today_users)

if not config.has_section("trophies"):
    config.add_section("trophies")
    
config.set("trophies", today+"-total", total_trophycount)
config.set("trophies", today+"-today", todaystrophies)


cfile = "/home/jono/matrixstats.txt"

with open(cfile, 'wb') as configfile:
    config.write(configfile)
