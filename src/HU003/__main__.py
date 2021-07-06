import sys
from logica.hu003 import uiEstudiantes
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialogo = uiEstudiantes()
    dialogo.show()
    app.exec_()
