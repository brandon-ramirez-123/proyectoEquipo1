from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///estudiante.sqlite')
Session = sessionmaker(bind=engine)

Base = declarative_base()
session = Session()

# def create_connection(db_file):
#     conn = None
#     try:
#         conn = sqlite3.connect(db_file)
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()
#
#
# if __name__ == '__declarative_base__':
#     create_connection(path.dirname(path.abspath(__file__)) + r"/../logica/estudiante.sqlite")
