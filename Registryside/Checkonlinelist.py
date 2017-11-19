import threading
import time
from core import constants as cn
from core.constants import _onlineList

_log = cn.getlog()


class CheckOnline(threading.Thread):

    def __init__(self,port):
        threading.Thread.__init__(self)
    def run(self):
        repeating = 0
        _log.info("Checker Thread started")
        while True:

            time.sleep(10) #5sn

            for key, value in _onlineList.items():
                if value[1]<5:
                    #del(_onlineList[key])
                    _log.info("The {} is removed Online list ".format(key))






