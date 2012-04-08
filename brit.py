import os
import ConfigParser
from optparse import OptionParser

SHARESPATH = None
QUEUEPATH = None

all = []
signed = []
matches = []
final = []

class Brit(object):
    def __init__(self, config_path):
        config = ConfigParser.ConfigParser()
        config.read(config_path + ".matrix")

        SHARESPATH = config.get("matrix", "sharespath")
        QUEUEPATH = config.get("matrix", "queuepath")

        self.remove_broken_symlinks()
        for r,d,f in os.walk(SHARESPATH):
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
                matches.append(i)

        final = list(set(matches) - set(signed))

        #print final
        # clear out links from queue

        #for the_file in os.listdir(QUEUEPATH + "/"):
        #    file_path = os.path.join(QUEUEPATH + "/", the_file)
        #    try:
        #        if os.path.isfile(file_path):
        #            os.unlink(file_path)
        #    except Exception, e:
        #        print e
        
        # create the symbol links

        #i = 1

        # populating the queue

        for t in final:
            symname = None
            stripslash = str(t.replace("/", ""))
            stripspace = str(stripslash.replace(" ", ""))
            striplb = str(stripspace.replace("(", ""))
            striprb = str(striplb.replace(")", ""))
            finalsym = str(striprb.replace(".", ""))
            symname = os.path.join(QUEUEPATH, finalsym)
            #print symname
            if not os.path.exists(symname):
                print "Adding: " + t
                os.symlink(t, symname)
            #i = i + 1

    def remove_broken_symlinks(self):
        links = []
        broken = []
        for root, dirs, files in os.walk('/home/jono/queue'):
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
            break
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
