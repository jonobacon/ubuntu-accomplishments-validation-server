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

        # clear out links from queue

        for the_file in os.listdir(QUEUEPATH + "/"):
            file_path = os.path.join(QUEUEPATH + "/", the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e

        # create the symbol links

        i = 1

        # populating the queue

        for t in final:
            print "Adding: " + t
            os.symlink(t, QUEUEPATH + "/" + str(i))
            i = i + 1

if __name__ == "__main__":
    parser = OptionParser()
    parser.set_defaults(suppress_notifications=False)
    parser.add_option("--config-path", dest="config_path", default=os.getenv("HOME") + "/")
    options, args = parser.parse_args()
    foo = Brit(config_path=options.config_path)
