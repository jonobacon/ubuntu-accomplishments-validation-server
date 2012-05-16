import os

class Accomplishments():
    def __init__(self):
        pass

    def get_extra_information(self, app, info):
        trophypath = os.environ['ACCOMTROPHYPATH']

        a = os.path.split(trophypath)
        b = os.path.split(a[0])

        extrapath = b[0] + "/" + ".extrainformation/"

        f = open(extrapath + info)

        data = f.read()

        final = [{info : data.rstrip('\n')}]

        return final
