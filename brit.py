import os
import ConfigParser
from optparse import OptionParser

all = []
signed = []
matches = []
final = []

class Brit(object):
    def __init__(self, config_path):
        config = ConfigParser.ConfigParser()
        config.read(config_path + ".matrix")

        self.SHARESPATH = config.get("matrix", "sharespath")
        self.QUEUEPATH = config.get("matrix", "queuepath")

        for r,d,f in os.walk(self.SHARESPATH):
            for i in f:
                if i.endswith(".trophy.asc"):
                    res = os.path.join(r,i)
                    signed.append(res[:-4])
            for i in f:
                if i.endswith(".trophy"):
                    res = os.path.join(r,i)
                    all.append(res)

        for i in all:
            if i.endswith(".asc"):
                pass
            else:
                p = "'" + i.replace("'", "'\\''") + "'"
                itemconfig = ConfigParser.ConfigParser()
                itemconfig.read(i)
                
                if itemconfig.has_option("trophy", "needs-signing"):
                    if itemconfig.get("trophy", "needs-signing").lower().strip() == "true":
                        matches.append(i)
                    else:
                        pass
                else:
                    pass

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
            

if __name__ == "__main__":
    parser = OptionParser()
    parser.set_defaults(suppress_notifications=False)
    parser.add_option("--config-path", dest="config_path", default=os.getenv("HOME") + "/")
    options, args = parser.parse_args()
    foo = Brit(config_path=options.config_path)
