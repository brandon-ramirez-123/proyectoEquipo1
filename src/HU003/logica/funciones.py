import os
import re
import sqlite3
import traceback
import pandas as pd
from datetime import datetime


class operacionesEstudiante():
    rutadb = os.path.dirname(os.path.abspath(__file__)) + r"/../../../tests/estudiante.sqlite"
    regex = r'^[a-zA-ZÀÈÌÒÁÉÍÓÚÙÄËÏÖÜÇÑàèìòáéíóúùäëïöüçñ][a-zA-ZÀÈÌÒÁÉÍÓÚÙÄËÏÖÜÇÑàèìòáéíóúùäëïöüçñ ]+$'

    def validar_nombres(self, nomb):
        validar = re.match(self.regex, nomb, re.I)
        if nomb == "":
            return False
        elif not validar:
            return False
        else:
            return True

    def validar_apellidoP(self, apat):
        validar = re.match(self.regex, apat, re.I)
        if apat == "":
            return False
        elif not validar:
            return False
        else:
            return True

    def validar_apellidoM(self, amat):
        validar = re.match(self.regex, amat, re.I)
        if amat == "":
            return False
        elif not validar:
            return False
        else:
            return True

    def existe_id(self, id):
        conex = sqlite3.connect(self.rutadb)
        eleccion = conex.execute(
            "select * from estudiante where ID='" + str(id) + "'")
        res = eleccion.fetchone()
        conex.close()
        if res is None:
            return False
        else:
            return True

    def ejecutar_consulta(self, consulta):
        conex = sqlite3.connect(self.rutadb)
        ejecucion = conex.execute(consulta)
        conex.close()
        return ejecucion

    def mostrar_estudiantes(self):
        try:
            conex = sqlite3.connect(self.rutadb)
            return pd.read_sql_query("select * from estudiante", conex)
        except:
            traceback.print_exc()
            return False

    def mostrar_datos(self, id):
        if self.existe_id(id):
            conex = sqlite3.connect(self.rutadb)
            return pd.read_sql_query("select * from estudiante where ID='" + str(id) + "'", conex)
        else:
            return False

    def buscar_repetido(self, nomb, apat, amat):
        conex = sqlite3.connect(self.rutadb)
        eleccion = conex.execute(
            "select * from estudiante where nombres='" + nomb + "' and apellidoPaterno='" + apat + "' and apellidoMaterno='" + amat + "'")
        res = eleccion.fetchone()
        conex.close()
        if res is None:
            return False
        else:
            return True

    def agregar_estudiante(self, nomb, apat, amat):
        if self.validar_nombres(nomb) and self.validar_apellidoP(apat) and self.validar_apellidoM(amat):
            if self.buscar_repetido(nomb, apat, amat):
                traceback.print_exc()
            else:
                try:
                    conex = sqlite3.connect(self.rutadb)
                    eleccion = conex.cursor()
                    eleccion.execute(
                        "insert into estudiante (ID, nombres, apellidoPaterno, apellidoMaterno, agregado) values ((select id+1 from estudiante order by agregado desc limit 1),'" + nomb + "','" + apat + "','" + amat + "','" + str(
                            datetime.now()) + "')")
                    conex.commit()
                    conex.close()
                    return True
                except:
                    traceback.print_exc()
                    return False
        else:
            traceback.print_exc()
            return False

    def actualizar_estudiante(self, id, nomb, apat, amat):
        if id != "" and id != 0 and self.existe_id(id) and self.validar_nombres(nomb) and self.validar_apellidoP(
                apat) and self.validar_apellidoM(amat):
            try:
                conex = sqlite3.connect(self.rutadb)
                eleccion = conex.cursor()
                eleccion.execute(
                    "update estudiante set nombres='" + nomb + "', apellidoPaterno='" + apat + "', apellidoMaterno='" + amat + "', agregado='" + str(
                        datetime.now()) + "' where ID='" + str(id) + "'")
                conex.commit()
                conex.close()
                return True
            except:
                traceback.print_exc()
                return False
        else:
            return False

    def eliminar_estudiante(self, id):
        if id != "" and id != 0 and self.existe_id(id):
            try:
                conex = sqlite3.connect(self.rutadb)
                eleccion = conex.cursor()
                eleccion.execute(
                    "delete from estudiante where ID='" + str(id) + "'")
                conex.commit()
                conex.close()
                return True
            except:
                traceback.print_exc()
                return False
        else:
            return False
