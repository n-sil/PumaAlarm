import sys
import datetime, time

from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, QTimer, pyqtSignal)


def makeTwo(i):
    if len(i) == 1:
        i = '0'+i
    return i


class clockThread(QThread):
    def run(self):
        while True != False:
            hr = str(datetime.datetime.now().time().hour)
            minu = makeTwo(str(datetime.datetime.now().time().minute))
            secd = makeTwo(str(datetime.datetime.now().time().second))
            print('Time is: %s:%s:%s' % (hr, minu, secd))
            time.sleep(1)

class timerThread(QThread):
    def run(self):
        for i in range(20):
            print('aasdf ' + str(i))
            time.sleep(1)

def runClock():
    print('sadf')

if __name__ == "__main__":
    app = QCoreApplication([])
    thread1 = clockThread()
    thread1.start()
    thread2 = timerThread()
    thread2.start()
    sys.exit(app.exec_())

'''


#import win32api
#win32api.SetSystemPowerState(1,0)

'''

'''
- Handle clock and timer via different threads
- Add countdown 'til alarm activation
-

'''