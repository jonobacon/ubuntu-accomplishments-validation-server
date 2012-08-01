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
        self.dir_config = os.path.join(xdg.BaseDirectory.xdg_config_home, "accomplishments")

        if not os.path.exists(self.dir_cache):
            os.makedirs(self.dir_cache)

        if not os.path.exists(os.path.join(self.dir_cache, "logs")):
            os.makedirs(os.path.join(self.dir_cache, "logs"))

        self.output_csv = os.path.join(self.dir_cache, "logs", "worker_failures.csv")

        now = datetime.datetime.now()
        self.date = now.strftime("%Y-%m-%d")
        self.time = now.strftime("%H:%M:%S")

        config = ConfigParser.ConfigParser()
        config.read(os.path.join(self.dir_config, ".matrix"))

        self.queue_path = None
        self.accom_path = None
        self.item_path = None
        self.adminweb_path = None
                
        self.current_user = ""
        self.current_collection = ""
        self.current_accom = ""
        self.current_reason = ""

        self.queue_path = config.get("matrix", "queuepath")
        self.accom_path = config.get("matrix", "accompath")
        self.adminweb_path = config.get("matrix", "adminwebpath")

        files = os.listdir(self.queue_path)

        for f in files:
            self.symlink = f
            self.failurecodes = []

            # this grabs the real path; remember it is a symlink
            self.item_path = os.path.realpath(os.path.join(self.queue_path, f))

            print "Processing: " + self.item_path
            self.current_date = self.date + " " + self.time            
            self.current_user = self.item_path.split("/")[7].split(" ")[0]
            self.current_collection = self.item_path.split("/")[-2]
            self.current_accom = self.item_path.split("/")[-1].split(".")[0]
            self.current_accom_id = self.current_collection + "/" + self.current_accom
            self.current_share_id = self.item_path.split(")")[-2].split("(")[-1].split(" ")[-1]

            os.environ['ACCOMTROPHYPATH'] = self.item_path

            itemconfig = ConfigParser.ConfigParser()
            itemconfig.read(self.item_path)

            try:
                item_app = itemconfig.get("trophy", "id").split("/")[0].replace(os.path.sep,'')
                item_accom = itemconfig.get("trophy", "id").split("/")[1].replace(os.path.sep,'')
            except ConfigParser.NoOptionError, err:
                self.current_reason = "Missing Trophy Option: id"
                self.failurecodes.append(200)

            script = ""
            
            try:
                script = self.get_script(itemconfig.get("trophy", "id"))
            except ConfigParser.NoOptionError, err:
                pass

            print "Script: " + script
            if os.path.exists(script):
                self.run_script(script)
            else:
                self.current_reason = "Script does not exist (" + str(script) + " )"
                self.failurecodes.append(201)

            if len(self.failurecodes) > 0:
                failurestring = ""
                
                for f in self.failurecodes:
                    failurestring = failurestring + str(f) + ","
                
                failurestring = failurestring.rstrip(",")
                addfailurepath = os.path.join(self.adminweb_path, "manage.py")
                
                try:
                    failurecommand = "python " + addfailurepath + " addfailure" + " '" + self.current_date + "' " + self.current_share_id + " " + self.current_user + " " + self.current_accom_id + " " + failurestring
                    active_proc = subprocess.Popen(["python", addfailurepath, "addfailure", self.current_date, self.current_share_id, self.current_user, self.current_accom_id, failurestring], 0, None, subprocess.PIPE, subprocess.PIPE, None)
                except:
                    print "Problem running failure logging."
                
                self.delete_trophy()            
        sys.exit(0)

    def get_script(self, accomid):
        collection = accomid.split("/")[0]
        accomfile = accomid.split("/")[1]        
        scriptsdir = os.path.join(self.accom_path, "scripts", collection)

        scriptfile = ""
        testfile = ""
        scriptname = (accomfile + ".py")

        for root, dirs, names in os.walk(scriptsdir):
            if scriptname in names:
                scriptfile = os.path.join(root, scriptname)
        
        return scriptfile

    def delete_trophy(self):
        print "...INVALID. Removing: " + self.item_path
        os.remove(self.item_path)
        self.remove_symlink()
        sys.exit(0)
        
    def run_script(self, script):
        exitcode = subprocess.call(script)
        if exitcode == 0:
            print "...SUCCESS (0)"
            self.sign_trophy()
            self.remove_symlink()
        elif exitcode == 1:
            print "...FAILED (1)"
            self.remove_symlink()
        elif exitcode == 2:
            print "...ERROR (2)"
            self.remove_symlink()
            self.delete_trophy()
        else:
            print "...BIZARRO"
        
        return

    def sign_trophy(self):
        print "signing trophy"
        print self.item_path
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

if __name__ == "__main__":
    parser = OptionParser()
    parser.set_defaults(suppress_notifications=False)
    parser.add_option("--config-path", dest="config_path", default=os.getenv("HOME") + "/")
    options, args = parser.parse_args()
    foo = Worker(config_path=options.config_path)
