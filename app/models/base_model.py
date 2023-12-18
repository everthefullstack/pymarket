from peewee import Model
from app.utils.database_solution import DatabaseSolution


class BaseModel(Model):

    class Meta:
        
        _ds = DatabaseSolution()
        schema = _ds.get_schema
        database = _ds.get_database
        
