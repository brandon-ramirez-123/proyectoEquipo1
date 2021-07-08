import sys

from PyQt5 import QtCore, QtWidgets

from logica.hu003 import uiEstudiantes
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    dialogo = uiEstudiantes()
    dialogo.show()
    app.exec_()
