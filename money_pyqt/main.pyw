import sys
from PyQt5 import QtWidgets
from dialog import Dialog

app = QtWidgets.QApplication(sys.argv)
dialog = Dialog()
dialog.show()
sys.exit(app.exec_())
