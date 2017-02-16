#coding: utf8
import sys
import datetime, time
from datetime import timedelta

from PyQt5.QtCore import pyqtSlot, QRunnable, QThread, QTimer
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUiType
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import win32event, win32api, os


# Load UI
form_class, base_class = loadUiType('T1.ui')

#timerVal = 100000000000

# Form initialization
class MainWindow(QDialog, form_class):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.setupUi(self)
        ringList = []
        for item in os.listdir('mp3'):
            if item.endswith(".mp3"):
                ringList.append(item)
        for item in ringList:
            self.comboBox.addItem(item)

    # Alarm setting
    def buttonClick(self):
        alarmTimer.start()
        progressTimer.start()


class ClockThread(QThread):
    def run(self):
        while True != False:
            hr = str(datetime.datetime.now().time().hour)
            minu = makeTwo(str(datetime.datetime.now().time().minute))
            secd = makeTwo(str(datetime.datetime.now().time().second))
            form.label.setText('%s:%s:%s' % (hr, minu, secd))
            time.sleep(1)

class AlarmThread(QThread):
    def run(self):
        ringTrack = form.comboBox.currentText()
        ringHour = int(form.timeEdit.dateTime().time().hour())
        ringMin = int(form.timeEdit.dateTime().time().minute())
        timerVal = (ringHour * 60 * 60 * 10000000 + ringMin * 60 * 10000000)

        h = win32event.CreateWaitableTimer(None, 1, None)
        form.pushButton.setEnabled(False)
        win32event.SetWaitableTimer(h, -timerVal, 0, None, None, 1)
        win32event.WaitForSingleObject(h, win32event.INFINITE)  # backup: (1 * 60 * 10000000)
        os.startfile("mp3\\" + ringTrack)
        form.label_3.setText('')
        form.pushButton.setEnabled(True)


class ProgressThread(QThread):
    def run(self):
        ringHour = int(form.timeEdit.dateTime().time().hour())                          # DRY
        ringMin = int(form.timeEdit.dateTime().time().minute())                         # THAT
        timerVal = (ringHour * 60 * 60 * 10000000 + ringMin * 60 * 10000000)            # UP!!!! FFS!

        sec = int(timerVal/10000000)
        print(sec)
        i = sec
        while i > 0:
            form.label_3.setText('Timer is set on: %s seconds' % (i))
            i -= 1
            time.sleep(1)


# Add '0' to one-digit minute/second value
def makeTwo(i):
    if len(i) == 1:
        i = '0'+i
    return i

# System tray icon initialization
class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)

#-----------------------------------------------------#


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName('Puma Alarm')
    # Create primary window
    form = MainWindow()
    form.setWindowTitle('Puma Alarm')
    form.show()

    # Create tray icon
    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("img/clock.png"), w)
    trayIcon.show()


    clockTimer = ClockThread()
    alarmTimer = AlarmThread()
    progressTimer = ProgressThread()

    clockTimer.start()


    # Exit
    sys.exit(app.exec_())


