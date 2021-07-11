import os
import re
import sqlite3
import traceback

from datetime import datetime
from PyQt5 import QtGui, uic
from PyQt5.QtCore import QCoreApplication, QRect, QSize, Qt
from PyQt5.QtWidgets import QAbstractItemView, QDialog, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, \
    QTableWidgetItem, QWidget


class estudiantesMain(QMainWindow):
    rutadb = os.path.dirname(os.path.abspath(__file__)) + r"/../logica/estudiante.sqlite"
    ident = 0
    nombre = ""
    apPat = ""
    apMat = ""

    def __init__(self):
        # Inicializacion
        super().__init__()
        rutaui = os.path.dirname(os.path.abspath(__file__)) + r"/../vista/hu003_estudiantes.ui"
        uic.loadUi(rutaui, self)
        self.setWindowTitle("Estudiantes")
        self.estID.setFocus()
        self.validar_nombres()
        self.validar_apellidoP()
        self.validar_apellidoM()

        # Cargar tabla "estudiante"
        self.cargarTabla()

        # Eventos
        self.estNombres.textChanged.connect(self.validar_nombres)
        self.estApPat.textChanged.connect(self.validar_apellidoP)
        self.estApMat.textChanged.connect(self.validar_apellidoM)
        self.estChkBuscar.stateChanged.connect(self.buscar)
        self.tbEstudiantes.itemSelectionChanged.connect(self.seleccionFila)
        self.tbEstudiantes.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbEstudiantes.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.estSalirEdicion.clicked.connect(self.salirEdicion)
        self.estAgregar.clicked.connect(self.anadirEstudiante)
        self.estEliminar.clicked.connect(self.eliminarEstudiante)
        self.estActualizar.clicked.connect(self.actualizarEstudiante)
        self.estSorteo.clicked.connect(self.sorteoEstudiante)

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
        self.tbEstudiantes.setRowCount(0)
        conex = sqlite3.connect(self.rutadb)
        estudiantes = conex.execute("SELECT * FROM estudiante ORDER BY ID ASC")
        for fila, estudiante in enumerate(estudiantes):
            self.tbEstudiantes.insertRow(fila)
            for columna, data in enumerate(estudiante):
                celda = QTableWidgetItem(str(data))
                self.tbEstudiantes.setItem(fila, columna, celda)
        conex.close()

    def seleccionFila(self):
        try:
            print(self.tbEstudiantes.item(self.tbEstudiantes.currentRow(), 0).text())
            id = self.tbEstudiantes.item(self.tbEstudiantes.currentRow(), 0).text()
            elementos = []
            conex = sqlite3.connect(self.rutadb)
            eleccion = conex.execute("SELECT * FROM estudiante WHERE ID='" + id + "'")
            for fila, estudiante in enumerate(eleccion):
                for columna, data in enumerate(estudiante):
                    celda = QTableWidgetItem(str(data))
                    elementos.append(celda.text())
            conex.close()
            self.datosSelecc(elementos[0], elementos[1], elementos[2], elementos[3])
        except:
            pass
        try:
            self.estNombres.disconnect()
            self.estApPat.disconnect()
            self.estApMat.disconnect()
        except:
            traceback.print_exc()
            pass
        try:
            self.estNombres.textChanged.connect(self.validar_nombres)
            self.estApPat.textChanged.connect(self.validar_apellidoP)
            self.estApMat.textChanged.connect(self.validar_apellidoM)
        except:
            traceback.print_exc()
            pass
        self.estID.setReadOnly(True)
        self.estID.setStyleSheet("background-color: white;\nborder: 1px solid black;")
        self.estID.setText(self.ident)
        self.estID.setFocus()
        self.estNombres.setText(self.nombre)
        self.estApPat.setText(self.apPat)
        self.estApMat.setText(self.apMat)
        self.estAgregar.setEnabled(False)
        self.estEliminar.setEnabled(False)
        self.estSorteo.setEnabled(False)
        self.estChkBuscar.setEnabled(False)
        self.estChkBuscar.setChecked(False)
        self.estActualizar.setEnabled(True)
        self.estSalirEdicion.setEnabled(True)
        self.estEliminar.setEnabled(True)

    def datosSelecc(self, stid, nom, pat, mat):
        self.ident = stid
        self.nombre = nom
        self.apPat = pat
        self.apMat = mat

    def salirEdicion(self):
        self.tbEstudiantes.disconnect()
        self.cargarTabla()
        self.tbEstudiantes.itemSelectionChanged.connect(self.seleccionFila)
        self.estID.setStyleSheet("background-color: lightgray;\nborder: 1px solid black;")
        self.estID.setText("")
        self.estID.setReadOnly(True)
        self.estNombres.setText("")
        self.estApPat.setText("")
        self.estApMat.setText("")
        self.estAgregar.setEnabled(True)
        self.estEliminar.setEnabled(True)
        self.estSorteo.setEnabled(True)
        self.estChkBuscar.setEnabled(True)
        self.estChkBuscar.setChecked(False)
        self.estActualizar.setEnabled(False)
        self.estSalirEdicion.setEnabled(False)
        self.estChkBuscar.setChecked(False)
        self.estEliminar.setEnabled(False)
        try:
            self.estNombres.textChanged.connect(self.validar_nombres)
            self.estApPat.textChanged.connect(self.validar_apellidoP)
            self.estApMat.textChanged.connect(self.validar_apellidoM)
        except:
            traceback.print_exc()
            pass

    def limpiar(self):
        self.estID.setText("")
        self.estNombres.setText("")
        self.estApPat.setText("")
        self.estApMat.setText("")

    def busquedaTotal(self):
        ides = self.estID.text()
        nomb = self.estNombres.text()
        apat = self.estApPat.text()
        amat = self.estApMat.text()
        self.tbEstudiantes.setRowCount(0)
        conex = sqlite3.connect(self.rutadb)
        eleccion = conex.execute(
            "SELECT * FROM estudiante WHERE ID LIKE '%" + ides + "%' AND nombres LIKE '%" + nomb + "%' AND apellidoPaterno LIKE '%" + apat + "%' AND apellidoMaterno LIKE '%" + amat + "%' ORDER BY ID ASC")
        for fila, estudiante in enumerate(eleccion):
            self.tbEstudiantes.insertRow(fila)
            for columna, data in enumerate(estudiante):
                celda = QTableWidgetItem(str(data))
                self.tbEstudiantes.setItem(fila, columna, celda)
        conex.close()

    def buscar(self):
        if self.estChkBuscar.isChecked():
            self.estID.setStyleSheet("background-color: white;\nborder: 1px solid black;")
            self.estID.setReadOnly(False)
            self.estID.setFocus()
            self.estNombres.disconnect()
            self.estNombres.setStyleSheet("border:1px solid black;")
            self.estApPat.disconnect()
            self.estApPat.setStyleSheet("border:1px solid black;")
            self.estApMat.disconnect()
            self.estApMat.setStyleSheet("border:1px solid black;")
            self.limpiar()
            self.tbEstudiantes.setRowCount(0)
            self.tbEstudiantes.disconnect()
            self.tbEstudiantes.itemSelectionChanged.connect(self.seleccionFila)
            self.busquedaTotal()
            self.estID.textChanged.connect(self.busquedaTotal)
            self.estNombres.textChanged.connect(self.busquedaTotal)
            self.estApPat.textChanged.connect(self.busquedaTotal)
            self.estApMat.textChanged.connect(self.busquedaTotal)
            self.estAgregar.setEnabled(False)
            self.estSorteo.setEnabled(False)
            self.estEliminar.setEnabled(True)
            self.estActualizar.setEnabled(True)
        else:
            self.estID.setStyleSheet("background-color: lightgray;\nborder: 1px solid black;")
            self.estID.setReadOnly(True)
            self.estID.disconnect()
            self.tbEstudiantes.disconnect()
            self.tbEstudiantes.itemSelectionChanged.connect(self.seleccionFila)
            try:
                self.estNombres.disconnect()
                self.estApPat.disconnect()
                self.estApMat.disconnect()
            except:
                traceback.print_exc()
                pass
            try:
                self.estNombres.textChanged.connect(self.validar_nombres)
                self.estApPat.textChanged.connect(self.validar_apellidoP)
                self.estApMat.textChanged.connect(self.validar_apellidoM)
            except:
                traceback.print_exc()
                pass

    def verRepetido(self, nomb, apat, amat):
        conex = sqlite3.connect(self.rutadb)
        eleccion = conex.execute(
            "select * from estudiante where nombres='" + nomb + "' and apellidoPaterno='" + apat + "' and apellidoMaterno='" + amat + "'")
        res = eleccion.fetchone()
        conex.close()
        if res is None:
            return False
        else:
            return True

    def anadirEstudiante(self):
        if self.validar_nombres() and self.validar_apellidoP() and self.validar_apellidoM():
            nomb = self.estNombres.text()
            apat = self.estApPat.text()
            amat = self.estApMat.text()
            if (self.verRepetido(nomb, apat, amat)):
                QMessageBox.information(self, "Datos repetidos", "Datos duplicados, reviselos.", QMessageBox.Ok)
            else:
                paso = False
                try:
                    conex = sqlite3.connect(self.rutadb)
                    eleccion = conex.cursor()
                    eleccion.execute(
                        "insert into estudiante (ID, nombres, apellidoPaterno, apellidoMaterno, agregado) values ((select id+1 from estudiante order by agregado desc limit 1),'" + nomb + "','" + apat + "','" + amat + "',strftime('%Y-%m-%d %H:%M:%f', 'now'))")
                    conex.commit()
                    conex.close()
                    paso = True
                except:
                    QMessageBox.information(self, "Error!", traceback.print_exc(), QMessageBox.Ok)
                if paso:
                    self.cargarTabla()
                    try:
                        conex = sqlite3.connect(self.rutadb)
                        eleccion = conex.execute(
                            "select * from estudiante where id=(select id from estudiante order by agregado desc limit 1)")
                        elementos = []
                        for fila, estudiante in enumerate(eleccion):
                            for columna, data in enumerate(estudiante):
                                celda = QTableWidgetItem(str(data))
                                elementos.append(celda.text())
                        conex.close()
                        self.popup = anadirEstudiante()
                        self.popup.setDatos(elementos[0], elementos[1], elementos[2], elementos[3])
                        self.popup.insDatos()
                        self.popup.show()
                        self.popup.exec_()
                    except:
                        QMessageBox.information(self, "Error!", traceback.print_exc(), QMessageBox.Ok)
        else:
            QMessageBox.information(self, "Datos incorrectos", "Revise los datos ingresados.", QMessageBox.Ok)

    def actualizarEstudiante(self):
        nombN = self.estNombres.text()
        apatN = self.estApPat.text()
        amatN = self.estApMat.text()
        if self.nombre == nombN and self.apPat == apatN and self.apMat == amatN:
            QMessageBox.information(self, "Sin cambios", "No se detectaron cambios, no se actualizará.", QMessageBox.Ok)
        else:
            if self.estID.text() != "" and self.ident != 0 and self.validar_nombres() and self.validar_apellidoP() and self.validar_apellidoM():
                paso = False
                try:
                    conex = sqlite3.connect(self.rutadb)
                    eleccion = conex.cursor()
                    eleccion.execute(
                        "update estudiante set nombres='" + nombN + "', apellidoPaterno='" + apatN + "', apellidoMaterno='" + amatN + "', agregado='" + str(
                            datetime.now()) + "') where ID='" + self.ident + "'")
                    conex.commit()
                    conex.close()
                    paso = True
                except:
                    QMessageBox.information(self, "Error!", traceback.print_exc(), QMessageBox.Ok)
                if paso:
                    self.cargarTabla()
                    self.limpiar()
                    self.salirEdicion()
                    self.estID.setStyleSheet("background-color: lightgray;\nborder: 1px solid black;")
                    self.estID.setReadOnly(True)
                    try:
                        self.popup = actualizarEstudiante()
                        self.popup.setDatos(self.ident, self.nombre, self.apPat, self.apMat, nombN, apatN, amatN)
                        self.popup.insDatos()
                        self.popup.revisarDiferencias()
                        self.popup.show()
                        self.popup.exec_()
                    except:
                        QMessageBox.information(self, "Error!", traceback.print_exc(), QMessageBox.Ok)
            else:
                QMessageBox.information(self, "Datos incorrectos", "Revise los datos ingresados.", QMessageBox.Ok)

    def eliminarEstudiante(self):
        paso = False
        try:
            conex = sqlite3.connect(self.rutadb)
            eleccion = conex.cursor()
            eleccion.execute(
                "delete from estudiante where ID='" + str(self.ident) + "'")
            conex.commit()
            conex.close()
            paso = True
        except:
            QMessageBox.information(self, "Error!", traceback.print_exc(), QMessageBox.Ok)
        if paso:
            try:
                self.popup = eliminarEstudiante()
                self.popup.setDatos(self.ident, self.nombre, self.apPat, self.apMat)
                self.popup.insDatos()
                self.popup.show()
                self.popup.exec_()
                if self.popup.close:
                    self.cargarTabla()
            except:
                QMessageBox.information(self, "Error!", traceback.print_exc(), QMessageBox.Ok)

    def sorteoEstudiante(self):
        try:
            conex = sqlite3.connect(self.rutadb)
            eleccion = conex.execute(
                "select * from estudiante order by random() limit 1")
            elementos = []
            for fila, estudiante in enumerate(eleccion):
                for columna, data in enumerate(estudiante):
                    celda = QTableWidgetItem(str(data))
                    elementos.append(celda.text())
            conex.close()
            self.popup = electoEstudiante()
            self.popup.setDatos(elementos[0], elementos[1], elementos[2], elementos[3])
            self.popup.insDatos()
            self.popup.show()
            self.popup.exec_()
        except:
            QMessageBox.information(self, "Error!", traceback.print_exc(), QMessageBox.Ok)


class anadirEstudiante(QDialog):
    ident = 0
    nombre = ""
    apPat = ""
    apMat = ""

    def __init__(self):
        # Inicializacion
        super().__init__()
        self.est_anadir()

        # Eventos
        self.nestCerrar.clicked.connect(self.close)

    def est_anadir(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('¡Éxito!')
        self.resize(340, 200)
        self.setMinimumSize(QSize(340, 200))
        self.setMaximumSize(QSize(340, 200))
        self.wid = QWidget(self)
        self.wid.setObjectName("wid")
        self.nestNombres = QLineEdit(self.wid)
        self.nestNombres.setGeometry(QRect(140, 70, 181, 21))
        self.nestNombres.setStyleSheet("border: 1px solid lightgray;")
        self.nestNombres.setMaxLength(255)
        self.nestNombres.setReadOnly(True)
        self.nestNombres.setObjectName("nestNombres")
        self.nestApPat = QLineEdit(self.wid)
        self.nestApPat.setGeometry(QRect(140, 100, 181, 21))
        self.nestApPat.setStyleSheet("border: 1px solid lightgray;")
        self.nestApPat.setMaxLength(255)
        self.nestApPat.setReadOnly(True)
        self.nestApPat.setObjectName("nestApPat")
        self.nest_lblApMat = QLabel(self.wid)
        self.nest_lblApMat.setGeometry(QRect(20, 130, 111, 16))
        self.nest_lblApMat.setObjectName("nest_lblApMat")
        self.nestApMat = QLineEdit(self.wid)
        self.nestApMat.setGeometry(QRect(140, 130, 181, 21))
        self.nestApMat.setStyleSheet("border: 1px solid lightgray;")
        self.nestApMat.setMaxLength(255)
        self.nestApMat.setReadOnly(True)
        self.nestApMat.setObjectName("nestApMat")
        self.nest_lblApPat = QLabel(self.wid)
        self.nest_lblApPat.setGeometry(QRect(20, 100, 111, 16))
        self.nest_lblApPat.setObjectName("nest_lblApPat")
        self.nest_lblNombres = QLabel(self.wid)
        self.nest_lblNombres.setGeometry(QRect(20, 70, 71, 16))
        self.nest_lblNombres.setObjectName("nest_lblNombres")
        self.nest_lblID = QLabel(self.wid)
        self.nest_lblID.setGeometry(QRect(20, 10, 291, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.nest_lblID.setFont(font)
        self.nest_lblID.setObjectName("nest_lblID")
        self.nestCerrar = QPushButton(self.wid)
        self.nestCerrar.setGeometry(QRect(230, 160, 91, 32))
        self.nestCerrar.setObjectName("nestCerrar")
        self.lblID = QLabel(self.wid)
        self.lblID.setGeometry(QRect(20, 40, 91, 16))
        self.lblID.setObjectName("lblID")
        self.nestID = QLineEdit(self.wid)
        self.nestID.setEnabled(True)
        self.nestID.setGeometry(QRect(140, 40, 181, 21))
        self.nestID.setAutoFillBackground(False)
        self.nestID.setStyleSheet("border: 1px solid lightgray;")
        self.nestID.setMaxLength(8)
        self.nestID.setReadOnly(True)
        self.nestID.setObjectName("nestID")
        _translate = QCoreApplication.translate
        self.nest_lblApMat.setText(_translate("MainWindow", "Apellido materno:"))
        self.nest_lblApPat.setText(_translate("MainWindow", "Apellido paterno:"))
        self.nest_lblNombres.setText(_translate("MainWindow", "Nombres:"))
        self.nest_lblID.setText(_translate("MainWindow", "Agregó un nuevo estudiante:"))
        self.nestCerrar.setText(_translate("MainWindow", "Cerrar"))
        self.lblID.setText(_translate("MainWindow", "ID estudiante:"))

    def setDatos(self, stid, nom, pat, mat):
        self.ident = stid
        self.nombre = nom
        self.apPat = pat
        self.apMat = mat

    def insDatos(self):
        self.nestID.setText(str(self.ident))
        self.nestNombres.setText(self.nombre)
        self.nestApPat.setText(self.apPat)
        self.nestApMat.setText(self.apMat)


class actualizarEstudiante(QDialog):
    ident = 0
    nombreA = ""
    apPatA = ""
    apMatA = ""
    nombreN = ""
    apPatN = ""
    apMatN = ""

    def __init__(self):
        # Inicializacion
        super().__init__()
        self.est_actualizar()

        # Eventos
        self.nestCerrar.clicked.connect(self.close)

    def est_actualizar(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('¡Éxito!')
        self.resize(340, 380)
        self.setMinimumSize(QSize(340, 380))
        self.setMaximumSize(QSize(340, 380))
        self.centralwidget = QWidget(self)
        self.aestApMatA = QLineEdit(self.centralwidget)
        self.aestApMatA.setGeometry(QRect(100, 280, 221, 21))
        self.aestApMatA.setStyleSheet("border: 1px solid lightgray;")
        self.aestApMatA.setMaxLength(255)
        self.aestApMatA.setReadOnly(True)
        self.aestApMatA.setObjectName("aestApMatA")
        self.nest_lblApMat = QLabel(self.centralwidget)
        self.nest_lblApMat.setGeometry(QRect(20, 250, 111, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.nest_lblApMat.setFont(font)
        self.nest_lblApMat.setObjectName("nest_lblApMat")
        self.aest_lblAct = QLabel(self.centralwidget)
        self.aest_lblAct.setGeometry(QRect(20, 10, 231, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.aest_lblAct.setFont(font)
        self.aest_lblAct.setObjectName("aest_lblAct")
        self.aestApPatN = QLineEdit(self.centralwidget)
        self.aestApPatN.setGeometry(QRect(100, 210, 221, 21))
        self.aestApPatN.setStyleSheet("border: 1px solid lightgray;")
        self.aestApPatN.setMaxLength(255)
        self.aestApPatN.setReadOnly(True)
        self.aestApPatN.setObjectName("aestApPatN")
        self.nest_lblApPat = QLabel(self.centralwidget)
        self.nest_lblApPat.setGeometry(QRect(20, 150, 111, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.nest_lblApPat.setFont(font)
        self.nest_lblApPat.setObjectName("nest_lblApPat")
        self.nestCerrar = QPushButton(self.centralwidget)
        self.nestCerrar.setGeometry(QRect(230, 340, 91, 32))
        self.nestCerrar.setObjectName("nestCerrar")
        self.aestID = QLineEdit(self.centralwidget)
        self.aestID.setEnabled(True)
        self.aestID.setGeometry(QRect(260, 10, 61, 21))
        self.aestID.setAutoFillBackground(False)
        self.aestID.setStyleSheet("border: 1px solid lightgray;")
        self.aestID.setMaxLength(8)
        self.aestID.setReadOnly(True)
        self.aestID.setObjectName("aestID")
        self.aestNombresA = QLineEdit(self.centralwidget)
        self.aestNombresA.setGeometry(QRect(100, 80, 221, 21))
        self.aestNombresA.setStyleSheet("border: 1px solid lightgray;")
        self.aestNombresA.setMaxLength(255)
        self.aestNombresA.setReadOnly(True)
        self.aestNombresA.setObjectName("aestNombresA")
        self.nest_lblNombres = QLabel(self.centralwidget)
        self.nest_lblNombres.setGeometry(QRect(20, 50, 71, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.nest_lblNombres.setFont(font)
        self.nest_lblNombres.setObjectName("nest_lblNombres")
        self.nest_lblNombresA = QLabel(self.centralwidget)
        self.nest_lblNombresA.setGeometry(QRect(20, 80, 61, 16))
        self.nest_lblNombresA.setObjectName("nest_lblNombresA")
        self.nest_lblNombresD = QLabel(self.centralwidget)
        self.nest_lblNombresD.setGeometry(QRect(20, 110, 71, 16))
        self.nest_lblNombresD.setObjectName("nest_lblNombresD")
        self.aestNombresN = QLineEdit(self.centralwidget)
        self.aestNombresN.setGeometry(QRect(100, 110, 221, 21))
        self.aestNombresN.setStyleSheet("border: 1px solid lightgray;")
        self.aestNombresN.setMaxLength(255)
        self.aestNombresN.setReadOnly(True)
        self.aestNombresN.setObjectName("aestNombresN")
        self.nest_lblApPatA = QLabel(self.centralwidget)
        self.nest_lblApPatA.setGeometry(QRect(20, 180, 51, 16))
        self.nest_lblApPatA.setObjectName("nest_lblApPatA")
        self.nest_lblApPatD = QLabel(self.centralwidget)
        self.nest_lblApPatD.setGeometry(QRect(20, 210, 71, 16))
        self.nest_lblApPatD.setObjectName("nest_lblApPatD")
        self.aestApPatA = QLineEdit(self.centralwidget)
        self.aestApPatA.setGeometry(QRect(100, 180, 221, 21))
        self.aestApPatA.setStyleSheet("border: 1px solid lightgray;")
        self.aestApPatA.setMaxLength(255)
        self.aestApPatA.setReadOnly(True)
        self.aestApPatA.setObjectName("aestApPatA")
        self.nest_lblApMatD = QLabel(self.centralwidget)
        self.nest_lblApMatD.setGeometry(QRect(20, 310, 71, 16))
        self.nest_lblApMatD.setObjectName("nest_lblApMatD")
        self.nest_lblApMatA = QLabel(self.centralwidget)
        self.nest_lblApMatA.setGeometry(QRect(20, 280, 51, 16))
        self.nest_lblApMatA.setObjectName("nest_lblApMatA")
        self.aestApMatN = QLineEdit(self.centralwidget)
        self.aestApMatN.setGeometry(QRect(100, 310, 221, 21))
        self.aestApMatN.setStyleSheet("border: 1px solid lightgray;")
        self.aestApMatN.setMaxLength(255)
        self.aestApMatN.setReadOnly(True)
        self.aestApMatN.setObjectName("aestApMatN")
        _translate = QCoreApplication.translate
        self.nest_lblApMat.setText(_translate("MainWindow", "Apellido materno:"))
        self.aest_lblAct.setText(_translate("MainWindow", "Actualizó los datos del estudiante:"))
        self.nest_lblApPat.setText(_translate("MainWindow", "Apellido paterno:"))
        self.nestCerrar.setText(_translate("MainWindow", "Cerrar"))
        self.nest_lblNombres.setText(_translate("MainWindow", "Nombres:"))
        self.nest_lblNombresA.setText(_translate("MainWindow", "- Antes:"))
        self.nest_lblNombresD.setText(_translate("MainWindow", "- Después:"))
        self.nest_lblApPatA.setText(_translate("MainWindow", "- Antes:"))
        self.nest_lblApPatD.setText(_translate("MainWindow", "- Después:"))
        self.nest_lblApMatD.setText(_translate("MainWindow", "- Después:"))
        self.nest_lblApMatA.setText(_translate("MainWindow", "- Antes:"))

    def setDatos(self, stid, nom, pat, mat, nomN, patN, matN):
        self.ident = stid
        self.nombre = nom
        self.apPat = pat
        self.apMat = mat
        self.nombreN = nomN
        self.apPatN = patN
        self.apMatN = matN

    def insDatos(self):
        self.aestID.setText(str(self.ident))
        self.aestNombresA.setText(self.nombre)
        self.aestApPatA.setText(self.apPat)
        self.aestApMatA.setText(self.apMat)
        self.aestNombresN.setText(self.nombreN)
        self.aestApPatN.setText(self.apPatN)
        self.aestApMatN.setText(self.apMatN)

    def revisarDiferencias(self):
        if self.aestNombresA.text() != self.aestNombresN.text():
            self.aestNombresA.setStyleSheet("border:1px solid yellow;")
            self.aestNombresN.setStyleSheet("border:1px solid red;")
        else:
            self.aestNombresA.setStyleSheet("border:1px solid green;")
            self.aestNombresN.setStyleSheet("border:1px solid green;")
        if self.aestApPatA.text() != self.aestApPatN.text():
            self.aestApPatA.setStyleSheet("border:1px solid yellow;")
            self.aestApPatN.setStyleSheet("border:1px solid red;")
        else:
            self.aestApPatA.setStyleSheet("border:1px solid green;")
            self.aestApPatN.setStyleSheet("border:1px solid green;")
        if self.aestApMatA.text() != self.aestApMatN.text():
            self.aestApMatA.setStyleSheet("border:1px solid yellow;")
            self.aestApMatN.setStyleSheet("border:1px solid red;")
        else:
            self.aestApMatA.setStyleSheet("border:1px solid green;")
            self.aestApMatN.setStyleSheet("border:1px solid green;")


class eliminarEstudiante(QDialog):
    ident = 0
    nombre = ""
    apPat = ""
    apMat = ""

    def __init__(self):
        # Inicializacion
        super().__init__()
        self.est_actualizar()

        # Eventos
        self.nestCerrar.clicked.connect(self.close)
        self.nestCancelar.clicked.connect(self.cancelarEliminacion)

    def est_actualizar(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('¡Éxito!')
        self.resize(340, 200)
        self.setMinimumSize(QSize(340, 200))
        self.setMaximumSize(QSize(340, 200))
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.nestApMat = QLineEdit(self.centralwidget)
        self.nestApMat.setGeometry(QRect(140, 130, 181, 21))
        self.nestApMat.setStyleSheet("border: 1px solid lightgray;")
        self.nestApMat.setMaxLength(255)
        self.nestApMat.setReadOnly(True)
        self.nestApMat.setObjectName("nestApMat")
        self.nest_lblApMat = QLabel(self.centralwidget)
        self.nest_lblApMat.setGeometry(QRect(20, 130, 111, 16))
        self.nest_lblApMat.setObjectName("nest_lblApMat")
        self.nest_lblID = QLabel(self.centralwidget)
        self.nest_lblID.setGeometry(QRect(20, 10, 291, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.nest_lblID.setFont(font)
        self.nest_lblID.setObjectName("nest_lblID")
        self.nestApPat = QLineEdit(self.centralwidget)
        self.nestApPat.setGeometry(QRect(140, 100, 181, 21))
        self.nestApPat.setStyleSheet("border: 1px solid lightgray;")
        self.nestApPat.setMaxLength(255)
        self.nestApPat.setReadOnly(True)
        self.nestApPat.setObjectName("nestApPat")
        self.nest_lblApPat = QLabel(self.centralwidget)
        self.nest_lblApPat.setGeometry(QRect(20, 100, 111, 16))
        self.nest_lblApPat.setObjectName("nest_lblApPat")
        self.nestCerrar = QPushButton(self.centralwidget)
        self.nestCerrar.setGeometry(QRect(230, 160, 91, 32))
        self.nestCerrar.setObjectName("nestCerrar")
        self.lblID = QLabel(self.centralwidget)
        self.lblID.setGeometry(QRect(20, 40, 91, 16))
        self.lblID.setObjectName("lblID")
        self.nestID = QLineEdit(self.centralwidget)
        self.nestID.setEnabled(True)
        self.nestID.setGeometry(QRect(140, 40, 181, 21))
        self.nestID.setAutoFillBackground(False)
        self.nestID.setStyleSheet("border: 1px solid lightgray;")
        self.nestID.setMaxLength(8)
        self.nestID.setReadOnly(True)
        self.nestID.setObjectName("nestID")
        self.nestNombres = QLineEdit(self.centralwidget)
        self.nestNombres.setGeometry(QRect(140, 70, 181, 21))
        self.nestNombres.setStyleSheet("border: 1px solid lightgray;")
        self.nestNombres.setMaxLength(255)
        self.nestNombres.setReadOnly(True)
        self.nestNombres.setObjectName("nestNombres")
        self.nest_lblNombres = QLabel(self.centralwidget)
        self.nest_lblNombres.setGeometry(QRect(20, 70, 71, 16))
        self.nest_lblNombres.setObjectName("nest_lblNombres")
        self.nestCancelar = QPushButton(self.centralwidget)
        self.nestCancelar.setGeometry(QRect(20, 160, 91, 32))
        self.nestCancelar.setObjectName("nestCancelar")
        _translate = QCoreApplication.translate
        self.nest_lblApMat.setText(_translate("MainWindow", "Apellido materno:"))
        self.nest_lblID.setText(_translate("MainWindow", "Eliminó un estudiante:"))
        self.nest_lblApPat.setText(_translate("MainWindow", "Apellido paterno:"))
        self.nestCerrar.setText(_translate("MainWindow", "Cerrar"))
        self.lblID.setText(_translate("MainWindow", "ID estudiante:"))
        self.nest_lblNombres.setText(_translate("MainWindow", "Nombres:"))
        self.nestCancelar.setText(_translate("MainWindow", "Cancelar"))

    def setDatos(self, stid, nom, pat, mat):
        self.ident = stid
        self.nombre = nom
        self.apPat = pat
        self.apMat = mat

    def insDatos(self):
        self.nestID.setText(str(self.ident))
        self.nestNombres.setText(self.nombre)
        self.nestApPat.setText(self.apPat)
        self.nestApMat.setText(self.apMat)
        self.nestApMat.setText(self.apMat)
        self.nestApMat.setText(self.apMat)

    def cancelarEliminacion(self):
        try:
            rutadb = os.path.dirname(os.path.abspath(__file__)) + r"/../logica/estudiante.sqlite"
            conex = sqlite3.connect(rutadb)
            revertir = conex.cursor()
            revertir.execute(
                "insert into estudiante (ID, nombres, apellidoPaterno, apellidoMaterno, agregado) values ('" + str(
                    self.ident) + "','" + self.nombre + "','" + self.apPat + "','" + self.apMat + "',strftime('%Y-%m-%d %H:%M:%f', 'now'))")
            conex.commit()
            conex.close()
            self.close()
        except:
            QMessageBox.information(self, "Error!", traceback.print_exc(), QMessageBox.Ok)


class electoEstudiante(QDialog):
    ident = 0
    nombre = ""
    apPat = ""
    apMat = ""

    def __init__(self):
        # Inicializacion
        super().__init__()
        self.est_actualizar()

        # Eventos
        self.nestCerrar.clicked.connect(self.close)

    def est_actualizar(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle('¡Éxito!')
        self.resize(340, 200)
        self.setMinimumSize(QSize(340, 200))
        self.setMaximumSize(QSize(340, 200))
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.estApMat = QLineEdit(self.centralwidget)
        self.estApMat.setGeometry(QRect(140, 130, 181, 21))
        self.estApMat.setStyleSheet("")
        self.estApMat.setMaxLength(255)
        self.estApMat.setReadOnly(True)
        self.estApMat.setObjectName("estApMat")
        self.lblApMat = QLabel(self.centralwidget)
        self.lblApMat.setGeometry(QRect(20, 130, 111, 16))
        self.lblApMat.setObjectName("lblApMat")
        self.estApPat = QLineEdit(self.centralwidget)
        self.estApPat.setGeometry(QRect(140, 100, 181, 21))
        self.estApPat.setStyleSheet("")
        self.estApPat.setMaxLength(255)
        self.estApPat.setReadOnly(True)
        self.estApPat.setObjectName("estApPat")
        self.lblID = QLabel(self.centralwidget)
        self.lblID.setGeometry(QRect(20, 40, 91, 16))
        self.lblID.setObjectName("lblID")
        self.estNombres = QLineEdit(self.centralwidget)
        self.estNombres.setGeometry(QRect(140, 70, 181, 21))
        self.estNombres.setStyleSheet("")
        self.estNombres.setMaxLength(255)
        self.estNombres.setReadOnly(True)
        self.estNombres.setObjectName("estNombres")
        self.lblNombres = QLabel(self.centralwidget)
        self.lblNombres.setGeometry(QRect(20, 70, 71, 16))
        self.lblNombres.setObjectName("lblNombres")
        self.lblApPat = QLabel(self.centralwidget)
        self.lblApPat.setGeometry(QRect(20, 100, 111, 16))
        self.lblApPat.setObjectName("lblApPat")
        self.estID = QLineEdit(self.centralwidget)
        self.estID.setEnabled(True)
        self.estID.setGeometry(QRect(140, 40, 181, 21))
        self.estID.setAutoFillBackground(False)
        self.estID.setStyleSheet("")
        self.estID.setMaxLength(8)
        self.estID.setReadOnly(True)
        self.estID.setObjectName("estID")
        self.lblID_2 = QLabel(self.centralwidget)
        self.lblID_2.setGeometry(QRect(20, 10, 131, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblID_2.setFont(font)
        self.lblID_2.setObjectName("lblID_2")
        self.nestCerrar = QPushButton(self.centralwidget)
        self.nestCerrar.setGeometry(QRect(230, 160, 91, 32))
        self.nestCerrar.setObjectName("nestCerrar")
        _translate = QCoreApplication.translate
        self.lblApMat.setText(_translate("MainWindow", "Apellido materno:"))
        self.lblID.setText(_translate("MainWindow", "ID estudiante:"))
        self.lblNombres.setText(_translate("MainWindow", "Nombres:"))
        self.lblApPat.setText(_translate("MainWindow", "Apellido paterno:"))
        self.lblID_2.setText(_translate("MainWindow", "Estudiante electo:"))
        self.nestCerrar.setText(_translate("MainWindow", "Cerrar"))

    def setDatos(self, stid, nom, pat, mat):
        self.ident = stid
        self.nombre = nom
        self.apPat = pat
        self.apMat = mat

    def insDatos(self):
        self.estID.setText(str(self.ident))
        self.estNombres.setText(self.nombre)
        self.estApPat.setText(self.apPat)
        self.estApMat.setText(self.apMat)
        self.estApMat.setText(self.apMat)
        self.estApMat.setText(self.apMat)
