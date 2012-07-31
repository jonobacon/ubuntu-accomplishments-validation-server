import os, subprocess
import ConfigParser
from optparse import OptionParser
import xdg.BaseDirectory, datetime
from time import gmtime, strftime

all = []
signed = []
matches = []
final = []

class Brit(object):
    def __init__(self):
        self.dir_cache = os.path.join(xdg.BaseDirectory.xdg_cache_home, "accomplishments")
        self.dir_config = os.path.join(xdg.BaseDirectory.xdg_config_home, "accomplishments")

        if not os.path.exists(self.dir_cache):
            os.makedirs(self.dir_cache)

        if not os.path.exists(os.path.join(self.dir_cache, "logs")):
            os.makedirs(os.path.join(self.dir_cache, "logs"))

        self.output_csv = os.path.join(self.dir_cache, "logs", "brit_failures.csv")

        now = datetime.datetime.now()
        self.date = now.strftime("%Y-%m-%d")
        self.time = now.strftime("%H:%M:%S")

        self.current_user = ""
        self.current_collection = ""
        self.current_accom = ""
        self.current_reason = ""

        config = ConfigParser.ConfigParser()
        config.read(os.path.join(self.dir_config, ".matrix"))

        self.SHARESPATH = config.get("matrix", "sharespath")
        self.QUEUEPATH = config.get("matrix", "queuepath")

        for r,d,f in os.walk(self.SHARESPATH):
            if not r.endswith(".extrainformation"):
                for i in f:
                    if i.endswith(".trophy.asc"):
                        res = os.path.join(r,i)
                        signed.append(res[:-4])
                    elif i.endswith(".trophy"):
                        res = os.path.join(r,i)
                        all.append(res)

        for i in all:
            self.failurecodes = []
            if i.endswith(".asc"):
                pass
            else:
                self.current_date = self.date + " " + self.time
                self.current_user = i.split("/")[5].split(" ")[0]
                self.current_collection = i.split("/")[-2]
                self.current_accom = i.split("/")[-1].split(".")[0]
                self.current_accom_id = self.current_collection + "/" + self.current_accom
                self.current_share_id = i.split(")")[-2].split("(")[-1].split(" ")[-1]
                                
                p = "'" + i.replace("'", "'\\''") + "'"
                itemconfig = ConfigParser.ConfigParser()

                try:
                    # check if this is a ConfigParser file
                    itemconfig.read(i)
                    
                    # check if there is a [trophyy] section header
                    if itemconfig.has_section("trophy"):
                        if len(itemconfig.items("trophy")) == 0:
                            self.current_reason = "No Options"
                            self.failurecodes.append(102)
                            self.update_log()
                        else:
                            # check if the trophy has any options
                            if itemconfig.has_option("trophy", "needs-signing"):
                                if itemconfig.get("trophy", "needs-signing").lower().strip() == "true":
                                    matches.append(i)
                                else:
                                    pass
                            else:
                                pass
                    else:
                        self.current_reason = "Missing Section: trophy"                        
                        self.failurecodes.append(101)
                        self.update_log()
                except ConfigParser.MissingSectionHeaderError, err:
                    self.current_reason = "No section header."
                    self.failurecodes.append(100)
                    self.update_log()                    
        
            if len(self.failurecodes) > 0:
                failurestring = ""
                
                for f in self.failurecodes:
                    failurestring = failurestring + str(f) + ","
                
                failurestring = failurestring.rstrip(",")
                
                failurecommand = "python /var/www/accomplishmentsadmin/manage.py addfailure" + " '" + self.current_date + "' " + self.current_share_id + " " + self.current_user + " " + self.current_accom_id + " " + failurestring
                print failurecommand
                active_proc = subprocess.Popen(["python", "/var/www/accomplishmentsadmin/manage.py", "addfailure", self.current_date, self.current_share_id, self.current_user, self.current_accom_id, failurestring], 0, None, subprocess.PIPE, subprocess.PIPE, None)
                os.remove(i)

        final = list(set(matches) - set(signed))

        # populating the queue

        for t in final:
            symname = None
            stripslash = str(t.replace("/", ""))
            stripspace = str(stripslash.replace(" ", ""))
            striplb = str(stripspace.replace("(", ""))
            striprb = str(striplb.replace(")", ""))
            finalsym = str(striprb.replace(".", ""))
            symname = os.path.join(self.QUEUEPATH, finalsym)
            #print symname
            if not os.path.exists(symname):
                print "Adding: " + t
                os.symlink(t, symname)
            #i = i + 1

        self.remove_broken_symlinks()
    
    def remove_broken_symlinks(self):
        links = []
        broken = []
        for root, dirs, files in os.walk(self.QUEUEPATH):
            for filename in files:
                path = os.path.join(root,filename)
                if os.path.islink(path):
                    target_path = os.readlink(path)
                    # Resolve relative symlinks
                    if not os.path.isabs(target_path):
                        target_path = os.path.join(os.path.dirname(path),target_path)
                    if not os.path.exists(target_path):
                        links.append(path)
                        broken.append(path)
                    else:
                        links.append(path)
                else:
                    # If it's not a symlink we're not interested.
                    continue
        if broken == []:
            pass
        else:
            for link in broken:
                # delete broken symlinks
                os.unlink(link)

    def update_log(self):        
        text_header = "Date,Time,User,Collection,Accomplishment,Reason\n"
        text_today = str(self.date) + "," + str(self.time) + "," + str(self.current_user) + "," + str(self.current_collection) + "," + str(self.current_accom) + "," + str(self.current_reason) + "\n"

        lines = []

        if not os.path.exists(self.output_csv):
            with open(self.output_csv, "a") as myfile:
                myfile.write(text_header)
                myfile.write(text_today)
                myfile.close()
        else:
            with file(self.output_csv, "r") as myfile:
                lines = myfile.readlines()
                lines.append(text_today)
                myfile.close()

                os.remove(self.output_csv)

                with open(self.output_csv, "w") as myfile:
                    for l in lines:
                        myfile.write(l)
                    myfile.close()            

if __name__ == "__main__":
    foo = Brit()
