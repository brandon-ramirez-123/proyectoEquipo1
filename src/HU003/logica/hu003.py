import sqlite3
import sys, re, os

import SQLiteHelper as SQLiteHelper
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5 import uic
from sqlite3 import *


class Dialogo(QMainWindow):
    ruta = os.path.dirname(os.path.abspath(__file__)) + r"/../logica/estudiante.sqlite"

    def __init__(self):
        # Inicializacion
        QMainWindow.__init__(self)
        ruta = os.path.dirname(os.path.abspath(__file__)) + r"/../vista/hu003.ui"
        uic.loadUi(ruta, self)
        self.estID.setFocus()
        self.validar_nombres()
        self.validar_apellidoP()
        self.validar_apellidoM()

        # Cargar tabla "estudiante"
        self.cargarTabla()

        # Eventos
        self.estID.textChanged.connect(self.validar_ID)
        self.estNombres.textChanged.connect(self.validar_nombres)
        self.estApPat.textChanged.connect(self.validar_apellidoP)
        self.estApMat.textChanged.connect(self.validar_apellidoM)
        self.estChkBuscar.stateChanged.connect(self.buscar)
        self.tbEstudiantes.itemSelectionChanged.connect(self.seleccionFila)
        self.btnSalirEdicion.clicked.connect(self.salirEdicion)
        self.estAgregar.clicked.connect(self.anadirEstudiante)

    def validar_ID(self):
        ID = self.estID.text()
        validar = re.match(r'^[0-9]{1,8}$', ID, re.I)
        if ID == "":
            self.estID.setStyleSheet("border:1px solid yellow;")
            return False
        elif not validar:
            self.estID.setStyleSheet("border:1px solid red;")
            return False
        else:
            self.estID.setStyleSheet("border:1px solid green;")
            return True

    def validar_nombres(self):
        nombres = self.estNombres.text()
        validar = re.match(r'^[a-zA-ZÀÈÌÒÁÉÍÓÚÙÄËÏÖÜÇÑàèìòáéíóúùäëïöüçñ][a-zA-ZÀÈÌÒÁÉÍÓÚÙÄËÏÖÜÇÑàèìòáéíóúùäëïöüçñ ]+$',
                           nombres, re.I)
        if nombres == "":
            self.estNombres.setStyleSheet("border:1px solid yellow;")
            return False
        elif not validar:
            self.estNombres.setStyleSheet("border:1px solid red;")
            return False
        else:
            self.estNombres.setStyleSheet("border:1px solid green;")
            return True

    def validar_apellidoP(self):
        apPat = self.estApPat.text()
        validar = re.match(r'^[a-zA-ZÀÈÌÒÁÉÍÓÚÙÄËÏÖÜÇÑàèìòáéíóúùäëïöüçñ][a-zA-ZÀÈÌÒÁÉÍÓÚÙÄËÏÖÜÇÑàèìòáéíóúùäëïöüçñ ]+$',
                           apPat, re.I)
        if apPat == "":
            self.estApPat.setStyleSheet("border:1px solid yellow;")
            return False
        elif not validar:
            self.estApPat.setStyleSheet("border:1px solid red;")
            return False
        else:
            self.estApPat.setStyleSheet("border:1px solid green;")
            return True

    def validar_apellidoM(self):
        apMat = self.estApMat.text()
        validar = re.match(r'^[a-zA-ZÀÈÌÒÁÉÍÓÚÙÄËÏÖÜÇÑàèìòáéíóúùäëïöüçñ][a-zA-ZÀÈÌÒÁÉÍÓÚÙÄËÏÖÜÇÑàèìòáéíóúùäëïöüçñ ]+$',
                           apMat, re.I)
        if apMat == "":
            self.estApMat.setStyleSheet("border:1px solid yellow;")
            return False
        elif not validar:
            self.estApMat.setStyleSheet("border:1px solid red;")
            return False
        else:
            self.estApMat.setStyleSheet("border:1px solid green;")
            return True

    def cargarTabla(self):
        conex = sqlite3.connect(self.ruta)
        estudiantes = conex.execute("SELECT * FROM estudiante")
        for fila, estudiante in enumerate(estudiantes):
            self.tbEstudiantes.insertRow(fila)
            for columna, data in enumerate(estudiante):
                celda = QTableWidgetItem(str(data))
                self.tbEstudiantes.setItem(fila, columna, celda)
        conex.close()

    def seleccionFila(self):
        id = self.tbEstudiantes.item(self.tbEstudiantes.currentRow(), 0).text()
        conex = sqlite3.connect(self.ruta)
        eleccion = conex.execute("SELECT * FROM estudiante WHERE ID='" + id + "'")
        elementos = []
        for fila, estudiante in enumerate(eleccion):
            for columna, data in enumerate(estudiante):
                celda = QTableWidgetItem(str(data))
                elementos.append(celda.text())
        self.estID.setText(elementos[0])
        self.estID.setStyleSheet("background-color: lightgray;\nborder: 1px solid green;")
        self.estNombres.setText(elementos[1])
        self.estApPat.setText(elementos[2])
        self.estApMat.setText(elementos[3])
        self.estAgregar.setEnabled(False)
        self.estEliminar.setEnabled(False)
        self.estSorteo.setEnabled(False)
        self.estChkBuscar.setEnabled(False)
        self.estChkBuscar.setChecked(False)
        self.btnActualizar.setEnabled(True)
        self.btnSalirEdicion.setEnabled(True)
        self.estEliminar.setEnabled(True)
        conex.close()

    def salirEdicion(self):
        self.estID.setText("")
        self.estNombres.setText("")
        self.estApPat.setText("")
        self.estApMat.setText("")
        self.estAgregar.setEnabled(True)
        self.estEliminar.setEnabled(True)
        self.estSorteo.setEnabled(True)
        self.estChkBuscar.setEnabled(True)
        self.estChkBuscar.setChecked(False)
        self.btnActualizar.setEnabled(False)
        self.btnSalirEdicion.setEnabled(False)
        self.estChkBuscar.setChecked(False)
        self.estEliminar.setEnabled(False)
        self.buscar()

    def buscar(self):
        if self.estChkBuscar.isChecked():
            self.estID.textChanged.disconnect(self.validar_ID)
            self.estID.setEnabled(True)
            self.estID.setStyleSheet("background-color: white;\nborder: 1px solid black;")
            self.estID.setFocus()
            self.estNombres.setStyleSheet("border:1px solid black;")
            self.estApPat.setStyleSheet("border:1px solid black;")
            self.estApMat.setStyleSheet("border:1px solid black;")
        else:
            self.estID.textChanged.connect(self.validar_ID)
            self.estID.setEnabled(False)
            self.estID.setStyleSheet("background-color: lightgray;\nborder: 1px solid black;")
            self.estNombres.setFocus()
            self.validar_nombres()
            self.validar_apellidoP()
            self.validar_apellidoM()

    def anadirEstudiante(self):
        if self.validar_nombres() and self.validar_apellidoP() and self.validar_apellidoM():
            QMessageBox.information(self, "Datos correctos", "Datos correctos", QMessageBox.Discard)
        else:
            QMessageBox.information(self, "Datos incorrectos", "Datos incorrectos", QMessageBox.Discard)
