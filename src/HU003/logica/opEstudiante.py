from datetime import datetime
from src.HU003.modelo.Estudiante import Estudiante
from src.HU003.modelo.declarative_base import Session, engine, Base


def anadeBase():
    # Crea la base de datos
    Base.metadata.create_all(engine)
    # Abre sesión
    session = Session()
    # Crea estudiantes
    estudiante1 = Estudiante(apellidoPaterno="Ramos", apellidoMaterno="Ortega", nombres="Juan Carlos",
                             agregado=datetime.now())
    estudiante2 = Estudiante(apellidoPaterno="Solis", apellidoMaterno="Matos", nombres="Pedro",
                             agregado=datetime.now())
    estudiante3 = Estudiante(apellidoPaterno="Paredes", apellidoMaterno="Torres", nombres="Luis Alberto",
                             agregado=datetime.now())
    estudiante4 = Estudiante(apellidoPaterno="Garcia", apellidoMaterno="Mateo", nombres="Miguel Angel",
                             agregado=datetime.now())
    # Agrega registros
    session.add(estudiante1)
    session.add(estudiante2)
    session.add(estudiante3)
    session.add(estudiante4)
    session.commit()
    # Fin
    session.close()


if True:
    try:
        anadeBase()
    except:
        print("Error")
