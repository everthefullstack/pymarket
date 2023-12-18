import dynaconf
from peewee import SqliteDatabase
from playhouse.postgres_ext import PostgresqlExtDatabase


class DatabaseSolution:

    def __init__(self) -> None:
        self.__schema = ""
        self.__database = ""
        self.__settings = dynaconf.settings
        self.__set_attrs_db()

    def __set_attrs_db(self):
        match self.__settings.DATABASE_SOLUTION:
            
            case "postgresql":
                self.__schema = self.__settings.DATABASE_SCHEMA
                self.__database = PostgresqlExtDatabase(self.__settings.DATABASE_URI + self.__settings.DATABASE_NAME, autocommit=True, autoconnect=True, autorollback=True)
            
            case "sqlite3":
                self.__schema = None
                self.__database = SqliteDatabase(self.__settings.DATABASE_PATH + self.__settings.DATABASE_NAME + ".db")

    @property
    def get_schema(self):
        return self.__schema
    
    @property
    def get_database(self):
        return self.__database