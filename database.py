from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_table = os.getenv('DB_DATABASE')


DB_URL = engine.URL.create(
    drivername="mysql+pymysql",
    username=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    database=db_table,
)


class EngineConn:
    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle=500)

    def sessionmaker(self):
        session = sessionmaker(bind=self.engine)
        #session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn