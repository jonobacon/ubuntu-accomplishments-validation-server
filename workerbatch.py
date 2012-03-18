#!/usr/bin/python
import sys, os, subprocess
import ConfigParser
from optparse import OptionParser
import shutil
import subprocess

class Worker(object):
    def __init__(self, config_path):
        print "Starting the worker..."

        config = ConfigParser.ConfigParser()
        config.read(config_path + ".matrix")

        self.queue_path = None
        self.accom_path = None
        self.item_path = None

        self.queue_path = config.get("matrix", "queuepath")
        self.accom_path = config.get("matrix", "accompath")
        print "Processing items in: " + self.queue_path

        files = os.listdir(self.queue_path)

        for f in files:
            self.symlink = f

            # this grabs the real path; remember it is a symlink
            self.item_path = os.path.realpath(os.path.join(self.queue_path, f))

            print "...processing: " + self.item_path

            os.environ['ACCOMTROPHYPATH'] = self.item_path

            itemconfig = ConfigParser.ConfigParser()
            itemconfig.read(self.item_path)

            try:
                item_app = itemconfig.get("trophy", "application")
                print "found app"
            except ConfigParser.NoSectionError, err:
                self.delete_trophy()
            
            try:    
                item_accom = itemconfig.get("trophy", "accomplishment")
                print "found accom"
            except ConfigParser.NoSectionError, err:
                self.delete_trophy()
                
            script = self.accom_path + "/scripts/" + item_app + "/" + item_accom + ".py"
            print script
            if os.path.exists(script):
                print "...running: " + script
                self.run_script(script)
            else:
                self.delete_trophy()
            
        sys.exit(0)

    def delete_trophy(self):
        print "...invalid file, removing: " + self.item_path
        os.remove(self.item_path)
        self.remove_symlink()
        sys.exit(0)
        
    def run_script(self, script):
        print "...validating: " + script
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
        else:
            print "shouldn't happen"

        print "...exit code: " + str(exitcode)

        return

    def sign_trophy(self):
        print "...signing the trophy!"

	command = []
	command.append("gpg")
	command.append("--yes")
	command.append("--output")
	command.append(self.item_path + ".asc")
	command.append("--clearsign")
	command.append(self.item_path)
	print command

        #shutil.copy (self.item_path, self.item_path + ".sig")
	subprocess.Popen(command)
        print "...signed!"
        
    def remove_symlink(self):
        linkadd = os.path.join(self.queue_path, self.symlink)
        print "...removing symlink: " + linkadd
        if os.path.exists(linkadd):
            os.unlink(linkadd)
        print "COMPLETED."


if __name__ == "__main__":
    parser = OptionParser()
    parser.set_defaults(suppress_notifications=False)
    parser.add_option("--config-path", dest="config_path", default=os.getenv("HOME") + "/")
    options, args = parser.parse_args()
    foo = Worker(config_path=options.config_path)
