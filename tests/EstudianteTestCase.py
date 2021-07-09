import unittest
from datetime import datetime

from src.HU003.logica.funciones import operacionesEstudiante
from src.HU003.modelo.Estudiante import Estudiante
from src.HU003.modelo.declarative_base import Base, Session, engine


class TCestudiante(unittest.TestCase):
    def setUp(self):
        # Importa operaciones para las pruebas
        self.operaciones = operacionesEstudiante()
        # Crea bd
        Base.metadata.create_all(engine)
        # Nueva sesion
        session = Session()
        # Estudiantes
        estudiante1 = Estudiante(apellidoPaterno="Ramos", apellidoMaterno="Ortega", nombres="Juan Carlos",
                                 agregado=datetime.now())
        estudiante2 = Estudiante(apellidoPaterno="Solis", apellidoMaterno="Matos", nombres="Pedro",
                                 agregado=datetime.now())
        estudiante3 = Estudiante(apellidoPaterno="Paredes", apellidoMaterno="Torres", nombres="Luis Alberto",
                                 agregado=datetime.now())
        estudiante4 = Estudiante(apellidoPaterno="Garcia", apellidoMaterno="Mateo", nombres="Miguel Angel",
                                 agregado=datetime.now())
        # Agrega estudiantes
        session.add(estudiante1)
        session.add(estudiante2)
        session.add(estudiante3)
        session.add(estudiante4)
        session.commit()
        # Fin
        session.close()

    def tearDown(self):
        # Deconstruccion luego de la prueba
        self.session = Session()
        estudiantes = self.session.query(Estudiante).all()
        for estudiante in estudiantes:
            self.session.delete(estudiante)
        self.session.commit()
        self.session.close()

    def test_agregar_estudiante(self):
        print("Antes:")
        print(self.operaciones.mostrar_estudiantes())
        resultado = self.operaciones.agregar_estudiante("Abcd", "Efgh", "Ijkl")
        # resultado = self.operaciones.agregar_estudiante("Luis Alberto", "Paredes", "Torres")
        print("Despues:")
        print(self.operaciones.mostrar_estudiantes())
        self.assertEqual(resultado, True)

    def test_actualizar_estudiante(self):
        id = 2
        print("Electo:")
        print(self.operaciones.mostrar_datos(id))
        print("Todos antes:")
        print(self.operaciones.mostrar_estudiantes())
        resultado = self.operaciones.actualizar_estudiante(id, "Abcd", "Efgh", "Ijkl")
        print("Cambios en:")
        print(self.operaciones.mostrar_datos(id))
        print("Todos después:")
        print(self.operaciones.mostrar_estudiantes())
        self.assertEqual(resultado, True)

    def test_eliminar_estudiante(self):
        id = 3
        print("Electo:")
        print(self.operaciones.mostrar_datos(id))
        print("Todos antes:")
        print(self.operaciones.mostrar_estudiantes())
        resultado = self.operaciones.eliminar_estudiante(id)
        print("Eliminado:")
        print(self.operaciones.mostrar_datos(id))
        print("Todos después:")
        print(self.operaciones.mostrar_estudiantes())
        self.assertEqual(resultado, True)

    def test_elegir_estudiante(self):
        id = 4
        print("Electo:")
        resultado = self.operaciones.mostrar_datos(id)
        print(resultado)
        self.assertIsNot(resultado, False)

    def test_ver_estudiantes(self):
        print("Estudiantes:")
        resultado = self.operaciones.mostrar_estudiantes()
        print(resultado)
        self.assertIsNot(resultado, False)
