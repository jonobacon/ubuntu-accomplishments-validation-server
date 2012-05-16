#!/usr/bin/python
import sys, os, subprocess, datetime
from time import gmtime, strftime
import ConfigParser
from optparse import OptionParser
import shutil
import subprocess
import xdg.BaseDirectory

class Worker(object):
    def __init__(self, config_path):               
        self.dir_cache = os.path.join(xdg.BaseDirectory.xdg_cache_home, "accomplishments")

        if not os.path.exists(self.dir_cache):
            os.makedirs(self.dir_cache)

        if not os.path.exists(os.path.join(self.dir_cache, "logs")):
            os.makedirs(os.path.join(self.dir_cache, "logs"))

        self.output_csv = os.path.join(self.dir_cache, "logs", "worker_csv.csv")

        now = datetime.datetime.now()
        self.date = now.strftime("%Y-%m-%d")
        self.time = now.strftime("%H:%M:%S")

        config = ConfigParser.ConfigParser()
        config.read(config_path + ".matrix")

        self.queue_path = None
        self.accom_path = None
        self.item_path = None
                
        self.current_user = ""
        self.current_collection = ""
        self.current_accom = ""
        self.current_status = ""

        self.queue_path = config.get("matrix", "queuepath")
        self.accom_path = config.get("matrix", "accompath")

        files = os.listdir(self.queue_path)

        for f in files:
            self.symlink = f

            # this grabs the real path; remember it is a symlink
            self.item_path = os.path.realpath(os.path.join(self.queue_path, f))

            print "Processing: " + self.item_path
            
            self.current_user = self.item_path.split("/")[7].split(" ")[0]
            self.current_collection = self.item_path.split("/")[-2]
            self.current_accom = self.item_path.split("/")[-1].split(".")[0]
            

            os.environ['ACCOMTROPHYPATH'] = self.item_path

            itemconfig = ConfigParser.ConfigParser()
            itemconfig.read(self.item_path)

            try:
                item_app = itemconfig.get("trophy", "application").replace(os.path.sep,'')
            except ConfigParser.NoOptionError, err:
                self.delete_trophy()
            
            try:    
                item_accom = itemconfig.get("trophy", "accomplishment").replace(os.path.sep,'')
            except ConfigParser.NoOptionError, err:
                self.delete_trophy()
                
            script = os.path.join(self.accom_path, "scripts", item_app, item_accom + ".py")
            if os.path.exists(script):
                self.run_script(script)
            else:
                self.delete_trophy()
            
        sys.exit(0)

    def delete_trophy(self):
        print "...INVALID. Removing: " + self.item_path
        self.current_status = "INVALID (" + self.item_path + ")"
        os.remove(self.item_path)
        self.remove_symlink()
        self.update_log()
        sys.exit(0)
        
    def run_script(self, script):
        exitcode = subprocess.call(script)
        if exitcode == 0:
            print "...SUCCESS (0)"
            self.current_status = "SUCCESS"
            self.sign_trophy()
            self.remove_symlink()
        elif exitcode == 1:
            print "...FAILED (1)"
            self.current_status = "FAILURE"
            self.remove_symlink()
        elif exitcode == 2:
            print "...ERROR (2)"
            self.current_status = "ERROR"
            self.remove_symlink()
        else:
            self.current_status = "BIZARRO"
            print "...BIZARRO"

        self.update_log()
        
        return

    def sign_trophy(self):
        command = []
        command.append("gpg")
        command.append("--yes")
        command.append("--output")
        command.append(self.item_path + ".asc")
        command.append("--clearsign")
        command.append(self.item_path)

        subprocess.Popen(command)
            
    def remove_symlink(self):
        linkadd = os.path.join(self.queue_path, self.symlink)
        if os.path.exists(linkadd):
            os.unlink(linkadd)

    def update_log(self):        
        text_header = "Date,Time,User,Collection,Accomplishment,Status\n"
        text_today = str(self.date) + "," + str(self.time) + "," + str(self.current_user) + "," + str(self.current_collection) + "," + str(self.current_accom) + "," + str(self.current_status) + "\n"

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
    parser = OptionParser()
    parser.set_defaults(suppress_notifications=False)
    parser.add_option("--config-path", dest="config_path", default=os.getenv("HOME") + "/")
    options, args = parser.parse_args()
    foo = Worker(config_path=options.config_path)
