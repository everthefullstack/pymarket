from playhouse.postgres_ext import PrimaryKeyField, CharField, DateTimeField, TextField
from app.models.base_model import BaseModel


class Errors(BaseModel):

    id = PrimaryKeyField(primary_key=True)
    procedimento = CharField()
    erro = TextField()
    data_hora = DateTimeField()
   
    class Meta:
        table_name = "tberrors"
