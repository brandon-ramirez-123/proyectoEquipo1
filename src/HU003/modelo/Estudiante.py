from sqlalchemy import Column, Integer, String, DateTime
from .declarative_base import Base


class Estudiante(Base):
    __tablename__ = "estudiante"
    ID = Column(Integer, primary_key=True)
    nombres = Column(String)
    apellidoPaterno = Column(String)
    apellidoMaterno = Column(String)
    agregado = Column(DateTime)

    # __esid__ = 0
    # __enom__ = ""
    # __eapa__ = ""
    # __eama__ = ""
    # __eagr__ = ""
    #
    # def __init__(self, ID, nombres, apellidoPaterno, apellidoMaterno, agregado):
    #     self.esid = ID
    #     self.enom = nombres
    #     self.eapa = apellidoPaterno
    #     self.eama = apellidoMaterno
    #     self.eagr = agregado
