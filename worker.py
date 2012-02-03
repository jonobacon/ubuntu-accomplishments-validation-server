#!/usr/bin/python
import sys, os, subprocess
import ConfigParser
from optparse import OptionParser
import shutil

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

        self.symlink = files[0]
        print "sym:"
        print self.symlink

        # this grabs the real path; remember it is a symlink
        self.item_path = os.path.realpath(self.queue_path + "/" + files[0])

        print "...processing: " + self.item_path

        os.environ['ACCOMTROPHYPATH'] = self.item_path

        itemconfig = ConfigParser.ConfigParser()
        itemconfig.read(self.item_path)

        item_app = itemconfig.get("trophy", "application")
        item_accom = itemconfig.get("trophy", "accomplishment")

        script = self.accom_path + "/scripts/" + item_app + "/" + item_accom + ".py"
        print "...running: " + script

        self.run_script(script)

        sys.exit(0)
        
    def run_script(self, script):
        print "...validating: " + script
        exitcode = subprocess.call(script)
        if exitcode == 0:
            print "...SUCCESS"
            self.sign_trophy()
            self.remove_symlink()
        elif exitcode == 1:
            print "failed"
            self.remove_symlink()
        elif exitcode == 2:
            print "error"
            self.remove_symlink()
        else:
            print "shouldn't happen"

        print "...exit code: " + str(exitcode)

        return

    def sign_trophy(self):
        print "...signing the trophy!"
        shutil.copy (self.item_path, self.item_path + ".sig")
        print "...done!"
        
    def remove_symlink(self):
        print "...removing symlink: " + self.symlink
        if self.symlink:
            os.unlink(os.path.join(self.queue_path, self.symlink))
        print "COMPLETED."


if __name__ == "__main__":
    parser = OptionParser()
    parser.set_defaults(suppress_notifications=False)
    parser.add_option("--config-path", dest="config_path", default=os.getenv("HOME") + "/")
    options, args = parser.parse_args()
    foo = Worker(config_path=options.config_path)
