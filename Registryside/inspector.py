import threading
import time
from core import constants as cn
from core.constants import ONLINEUSERS
from core.constants import CONECTIONS

LOG = cn.getlog()


class Checker(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        LOG.info("Checker Thread started")
        while True:

            time.sleep(1) #1sn
            ctime=round(time.time())

            for key in list(ONLINEUSERS):
                if (ctime-ONLINEUSERS[key][1]) >  cn.TIMEOUT:
                    del(ONLINEUSERS[key])
                    LOG.info("The {} is removed online list becuse of timeout ".format(key))


            self.controlConnections()


    def controlConnections(self):
        for index,item in enumerate(CONECTIONS):
            if item.isAlive is False:
                print("Removed connections",item.getName(), ' ', item.isAlive())
                CONECTIONS.remove(index)






