from playhouse.postgres_ext import PrimaryKeyField, CharField, DateTimeField, JSONField, IntegerField
from app.models.base_model import BaseModel
import datetime


class UpdateTabelaGeral(BaseModel):

    id = PrimaryKeyField(primary_key=True)
    tabela = CharField()
    id_registro_tabela = IntegerField()
    colunas_afetadas = JSONField()
    data_hora_modificacao = DateTimeField(default=datetime.datetime.now)
   
    class Meta:
        table_name = "tbupdatetabelageral"

