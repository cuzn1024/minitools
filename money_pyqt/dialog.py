import os
import sys
import sip
import json
import time
import _thread
from datetime import datetime, timedelta
import subprocess
import requests
import tushare as ts

from PyQt5 import QtWidgets, QtCore, QtGui

import res

class Dialog(QtWidgets.QWidget):
    trigger = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Dialog, self).__init__()

        self.trigger.connect(self.updateData)

        self.drag = False
        self.pos = QtCore.QPoint(0, 0)
        
        self.sz = float(0)
        self.cyb = float(0)
        
        self.init()

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            return

        self.drag = True
        self.pos = event.globalPos() - self.frameGeometry().topLeft()
        event.accept()

    def mouseMoveEvent(self, event):
        if self.drag == False:
            return

        if (event.globalPos().y() == 0):
            self.move(event.globalPos().x() - self.pos.x(), 0)
        else:
            self.move(event.globalPos() - self.pos)

        event.accept()

    def mouseReleaseEvent(self, event):
        self.drag = False
        event.accept()

        self.data['config']['pos'] = str(self.x()) + "x" + str(self.y())

    def showEvent(self, event):
        self.spinButton.move(self.width() - self.spinButton.width(), 0)
        self.configButton.move(self.spinButton.pos().x() - self.configButton.width() - 5, 0)

    def mouseDoubleClickEvent(self, event):
        self.visibleSwitch()

    def init(self):
        self.setWindowTitle('nothing')
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        self.createSpinButton()
        self.createSystemTrayIcon()

        self.refreshUI()

    def refreshUI(self):
        self.loadData()
        self.createChildren()
        self.setFixedSize(self.sizeHint())
        
        self.setWindowOpacity(self.data['config']['opacity'])

        self.move(int(self.data['config']['pos'].split("x")[0]), int(self.data['config']['pos'].split("x")[1]))

        self.update()

        self.dataGotOnce = False

        _thread.start_new_thread(Dialog.getData, (self, ))

    def loadData(self):
        path = os.path.split(os.path.realpath(__file__))[0] + '/data.json'
        self.data = {}

        if os.access(path, os.R_OK):
            with open(path, 'r') as dataFile:
                self.data = json.load(dataFile)
                dataFile.close()

    def saveData(self):
        path = os.path.split(os.path.realpath(__file__))[0] + '/data.json'

        if os.access(path, os.W_OK):
            with open(path, 'w') as dataFile:
                json.dump(self.data, dataFile, indent=2)
                dataFile.close()

    def createSystemTrayIcon(self):
        self.systemTrayIcon = QtWidgets.QSystemTrayIcon()
        self.systemTrayIcon.setIcon(QtGui.QIcon(":/stock.png"))

        restoreWinAction = QtWidgets.QAction("隐藏", self)
        quitAction = QtWidgets.QAction("退出", self)

        restoreWinAction.triggered.connect(self.visibleSwitch)
        quitAction.triggered.connect(self.quitDialog)
  
        menu = QtWidgets.QMenu(QtWidgets.QApplication.desktop())
  
        menu.addAction(restoreWinAction)
        menu.addSeparator()
        menu.addAction(quitAction)

        if QtWidgets.QSystemTrayIcon.isSystemTrayAvailable() == False:
            return

        self.systemTrayIcon.setContextMenu(menu)
        self.systemTrayIcon.activated.connect(self.systemTrayIconActivated)
        self.systemTrayIcon.show()

    def createSpinButton(self):
        self.spinButton = QtWidgets.QPushButton("|", self)
        self.spinButton.setFixedSize(20, 20)
        self.spinButton.show()

        self.spinButton.clicked.connect(self.spinClicked)

        self.configButton = QtWidgets.QPushButton("dt", self)
        self.configButton.setFixedSize(20, 20)
        self.configButton.show()

        self.configButton.clicked.connect(self.configClicked)

    def createChildren(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 35, 0)

        hLayout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel()
        label.setObjectName("sz")
        label.setFixedSize(85, 20)
        hLayout.addWidget(label)
        
        self.index = {"sz":{"4days":"", "low":""}, "cyb":{"4days":"", "low":""}}

        data = ts.get_k_data(code="000001", index=True, start=(datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d"), end=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))
        if data.empty == False:
            self.index["sz"]["4days"] = round(data.tail(4)["close"].sum(), 2)
            self.index["sz"]["3days"] = round(data.tail(3)["close"].sum(), 2)
            self.index["sz"]["low"] = round(data["low"].min(), 2)

        if (self.data['config']['col'] == 1):
            layout.addLayout(hLayout)
            hLayout = QtWidgets.QHBoxLayout()
        
        label = QtWidgets.QLabel()
        label.setObjectName("cyb")
        label.setFixedSize(85, 20)
        hLayout.addWidget(label)

        data = ts.get_k_data(code="399006", index=True, start=(datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d"), end=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))
        if data.empty == False:
            self.index["cyb"]["4days"] = round(data.tail(4)["close"].sum(), 2)
            self.index["cyb"]["3days"] = round(data.tail(3)["close"].sum(), 2)
            self.index["cyb"]["low"] = round(data["low"].min(), 2)

        if (self.data['config']['col'] == 1):
            layout.addLayout(hLayout)
            hLayout = QtWidgets.QHBoxLayout()
        
        label = QtWidgets.QLabel()
        label.setObjectName("sz50")
        label.setFixedSize(85, 20)
        hLayout.addWidget(label)

        if (self.data['config']['col'] == 1):
            layout.addLayout(hLayout)
            hLayout = QtWidgets.QHBoxLayout()
        
        label = QtWidgets.QLabel()
        label.setObjectName("cyb50")
        label.setFixedSize(85, 20)
        hLayout.addWidget(label)

        hLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        layout.addLayout(hLayout)

        col = 0

        for k in self.data['stocks']:
            if col % self.data['config']['col'] == 0:
                hLayout = QtWidgets.QHBoxLayout()

            label = QtWidgets.QLabel()
            label.setObjectName("ratio_" + k)
            label.setFixedSize(80, 20)
            hLayout.addWidget(label)

            col = col + 1

            if col % self.data['config']['col'] == 0:
                layout.addLayout(hLayout)

            data = ts.get_k_data(code=k, start=(datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d"), end=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"))
            if data.empty == False:
                if '4days' in self.data['stocks'][k]:
                    self.data['stocks'][k]['4days'] = round(data.tail(4)["close"].sum(), 2)
                if '3days' in self.data['stocks'][k]:
                    self.data['stocks'][k]["3days"] = round(data.tail(3)["close"].sum(), 2)
                if 'low' in self.data['stocks'][k]:
                    self.data['stocks'][k]['low'] = round(data["low"].min(), 2)

        if col % self.data['config']['col'] != 0:
            hLayout.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
            layout.addLayout(hLayout)

        self.setLayout(layout)

    @QtCore.pyqtSlot()
    def visibleSwitch(self):
        if self.isVisible():
            self.systemTrayIcon.contextMenu().actions()[0].setText("还原")
        else:
            self.systemTrayIcon.contextMenu().actions()[0].setText("隐藏")
        self.setVisible(not self.isVisible())

    @QtCore.pyqtSlot(QtWidgets.QSystemTrayIcon.ActivationReason)
    def systemTrayIconActivated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.DoubleClick:
            self.visibleSwitch()

    def quitDialog(self):
        self.saveData()
        self.hide()
        self.systemTrayIcon.hide()
        QtCore.QCoreApplication.quit()

    @QtCore.pyqtSlot()
    def spinClicked(self):
        if self.spinButton.text() == "|":
            self.spinButton.setText("——")
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.spinButton.setText("|")
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    @QtCore.pyqtSlot()
    def configClicked(self):
        self.saveData()
        p = subprocess.Popen("notepad " + os.path.split(os.path.realpath(__file__))[0] + '/data.json')
        p.communicate('')

        self.systemTrayIcon.hide()

        python = sys.executable
        os.execl(python, python, * sys.argv)

    def getData(self):
        while True:
            time.sleep(3)

            if self.dataGotOnce == True:
                if datetime.now().hour < 9 or ((datetime.now().hour >= 11 and datetime.now().minute >= 31) and datetime.now().hour < 13) or (datetime.now().hour > 15) == True:
                    print("yes")
                    continue

            self.dataGotOnce = True

            query = "http://qt.gtimg.cn/q=sh000001,sz399006,sh000016,sz399673,"

            if self.data['stocks']:
                for stock in self.data['stocks']:
                    query = query + stock + ','

            try:
                response = requests.get(query, timeout=1)
            except:
                continue

            if response.status_code != 200:
                print("Can't access " + query)
                continue

            self.trigger.emit(response.content.decode('gb2312'))

    @QtCore.pyqtSlot(str)
    def updateData(self, s):
        strList = s.splitlines(False)

        for s in strList:
            code = s[2:10]

            if code == 'sh000001':
                s = s[12:len(s) - 2]
                values = s.split('~')

                current = float(values[3])
                label = self.findChild(QtWidgets.QLabel, 'sz')
                if current == self.sz:
                    prefix = ''
                elif current > self.sz:
                    prefix = u'\u2191'
                else:
                    prefix = u'\u2193'
                label.setText(str(values[32]) + "%|" + values[3])

                if self.index["sz"]["low"] > float(values[3]):
                    self.index["sz"]["low"] = float(values[3])
                label.setToolTip(str(round((float(self.index["sz"]["4days"]) + float(values[3])) / 5, 2)) + " " + str(self.index["sz"]["low"]))

                self.sz = current
            elif code == "sz399006":
                s = s[12:len(s) - 2]
                values = s.split('~')

                current = float(values[3])
                label = self.findChild(QtWidgets.QLabel, 'cyb')
                if current == self.cyb:
                    prefix = ''
                elif current > self.cyb:
                    prefix = u'\u2191'
                else:
                    prefix = u'\u2193'
                label.setText(str(values[32]) + "%|" + values[3])

                if self.index["cyb"]["low"] > float(values[3]):
                    self.index["cyb"]["low"] = float(values[3])
                label.setToolTip(str(round((float(self.index["cyb"]["4days"]) + float(values[3])) / 5, 2)) + " " + str(self.index["cyb"]["low"]))

                self.cyb = current

            elif code == 'sh000016':
                s = s[12:len(s) - 2]
                values = s.split('~')

                current = float(values[3])
                label = self.findChild(QtWidgets.QLabel, 'sz50')
                if current == self.sz:
                    prefix = ''
                elif current > self.sz:
                    prefix = u'\u2191'
                else:
                    prefix = u'\u2193'
                label.setText(str(values[32]) + "%|" + values[3])

            elif code == 'sz399673':
                s = s[12:len(s) - 2]
                values = s.split('~')

                current = float(values[3])
                label = self.findChild(QtWidgets.QLabel, 'cyb50')
                if current == self.sz:
                    prefix = ''
                elif current > self.sz:
                    prefix = u'\u2191'
                else:
                    prefix = u'\u2193'
                label.setText(str(values[32]) + "%|" + values[3])
            else:
                s = s[12:len(s) - 2]

                values = s.split('~')
                name = values[1]
                current = float(values[3])
                
                label = self.findChild(QtWidgets.QLabel, 'ratio_' + code)

                price = 0
                if '4days' in self.data['stocks'][code]:
                    fiveDaysAver = (float(self.data['stocks'][code]['4days']) + float(values[3])) / 5
                    price = fiveDaysAver
                
                if self.data['stocks'][code]['price'] != "":
                    price = float(self.data['stocks'][code]['price'])

                text = str(values[32]) + "%|" + str(float(int(((float(values[3]) - price) / price * 10000))  / float(100)
                               )) + "%"
                label.setText(text)

                if (float(values[36]) < 1):
                    tooltip = values[1] + "|" + values[3]
                    label.setToolTip(tooltip)
                else:
                    #当日均线 5日均线 支撑线
                    tooltip = values[1] + "|" + values[3]

                    todayAver = float(values[37]) / float(values[36]) * 100
                    todayAver = round((float(values[3]) - todayAver) / todayAver * 100, 2)
                    tooltip = tooltip + ' ' + str(todayAver) + "%"

                    if '4days' in self.data['stocks'][code]:
                        tooltip = tooltip + " " + str(round((float(values[3]) - fiveDaysAver) * 100 / fiveDaysAver, 2)) + "%"

                    if '3days' in self.data['stocks'][code]:
                        fiveDaysAver = (float(self.data['stocks'][code]['3days']) + float(values[3]) * 2) / 5
                        tooltip = tooltip + " " + str(round((float(values[3]) - fiveDaysAver) * 100 / fiveDaysAver, 2)) + "%"

                    if 'low' in self.data['stocks'][code]:
                        low = float(self.data['stocks'][code]['low'])
                        if low > float(values[3]):
                            low = float(values[3])
                        low = round((float(values[3]) - low) * 100 / low, 2)
                        tooltip = tooltip + " " + str(low) + "%"

                    label.setToolTip(tooltip)