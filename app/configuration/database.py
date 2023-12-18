import psycopg2 as pg
import sqlite3 as sql
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dynaconf import settings

class Database:

    __slots__ = ("database_solution", "database_uri", "database_name", "database_schema", "database_path")

    def __init__(self) -> None:
        self.database_solution = settings.DATABASE_SOLUTION
        self.database_uri = settings.DATABASE_URI
        self.database_name = settings.DATABASE_NAME
        self.database_schema = settings.DATABASE_SCHEMA
        self.database_path = settings.DATABASE_PATH
    
    def __create_sql_postgres(self):
        try:
            sqls = [f"CREATE DATABASE {self.database_name}",
                    f"CREATE SCHEMA IF NOT EXISTS {self.database_schema}"]
            
            conn = pg.connect(self.database_uri)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            with cursor as curr:
                curr.execute(f"SELECT datname FROM pg_database WHERE datname = '{self.database_name}'")
                result = curr.fetchone()

                if result:
                    print("ja existe o banco de dados e não será criado.")
                
                else:
                    curr.execute(sqls[0])
                    conn.commit()

            conn = pg.connect(f"{self.database_uri}{self.database_name}")
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            with cursor as curr:
                curr.execute(sqls[1])
                conn.commit()
                

        except Exception as error:
            print(str(error))

    def __create_database_path(self):
        try:
            if not os.path.isdir(self.database_path):
                os.mkdir(self.database_path)
            
            else:
                print(f"Já existe o diretório {self.database_path}, o mesmo não será criado.")

        except Exception as error:
            print(str(error))

    def __create_sql_sqlite(self):
        try:
            
            conn = sql.connect(self.database_path + self.database_name +".db")
            conn.commit()
            conn.close()
        
        except Exception as error:
            print(str(error))

    def __config_database(self):
        match self.database_solution:
            case "postgresql":
                self.__create_sql_postgres()

            case "sqlite3":
                self.__create_database_path()
                self.__create_sql_sqlite()

    def init_app(self):
        self.__config_database()
        
