import logging
import os
import sys



DBPATH   ='mongodb://localhost:27017/'

ONLINEUSERS={}
CONECTIONS= []
TCP=3131
UDP=5151
ROOTPATH = ''
COLLECTIONS="authentication"
DBNAME="P2PApp"
TIMEOUT=60



for i in os.path.dirname(os.path.abspath(__file__)).split('/')[1:]:
        ROOTPATH = ROOTPATH+'/'+i
if ROOTPATH not in sys.path:
        sys.path.append(ROOTPATH)

def getlog():
    logFormatter = logging.Formatter(
        "%(asctime)s [%(filename)s  %(funcName)s  %(threadName)s ] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()

    if (len(rootLogger.handlers) > 0):
        return rootLogger
    rootLogger.setLevel(logging.INFO)
    fileHandler = logging.FileHandler('logfile.log')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    return rootLogger