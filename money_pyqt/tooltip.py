
from PyQt5 import QtWidgets, QtCore, QtGui

class Tooltip(QtWidgets.QWidget):
    def __init__(self):
        super(Tooltip, self).__init__()

        self.init()

    def init(self):
        layout = QtWidgets.QFormLayout()

        self.name = QtWidgets.QLineEdit()
        layout->addRow("名称：", self.name)
        self.price = QtWidgets.QLineEdit()
        layout->addRow("价格：", self.price)
        self.ave = QtWidgets.QLineEdit()
        layout->addRow("均价：", self.ave)
        self.ave5 = QtWidgets.QLineEdit()
        layout->addRow("今5：", self.ave5)
        self.ave4 = QtWidgets.QLineEdit()
        layout->addRow("明5：", self.ave4)

        self.setLayout(layout)

        self.setFixSize(self.sizeHint())