import threading
import time
from core import constants as cn
from core.constants import _onlineList

_log = cn.getlog()


class CheckOnline(threading.Thread):

    def __init__(self,port):
        threading.Thread.__init__(self)
    def run(self):
        _log.info("Checker Thread started")
        while True:

            time.sleep(1) #1sn
            ctime=round(time.time())
            for key, value in _onlineList.items():
                if (ctime-value[1]) >  10:
                    #del(_onlineList[key])
                    _log.info("The {} is removed Online list ".format(key))






