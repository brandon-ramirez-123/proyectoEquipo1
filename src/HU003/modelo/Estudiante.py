from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from .declarative_base import Base


class Estudiante(Base):
    __tablename__ = "estudiante"
    ID = Column(Integer, primary_key=True)
    nombres = Column(String)
    apellidoPaterno = Column(String)
    apellidoMaterno = Column(String)
    agregado = Column(DateTime)
