
import sys

def getparam(id):
    teste=0
    for param in sys.argv:
        if (teste == 1):
            return param
        if(param==id):
            teste=1
