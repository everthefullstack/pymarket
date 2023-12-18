from playhouse.postgres_ext import PrimaryKeyField, DateTimeField, IntegerField
from app.models.base_model import BaseModel


class UpdateBot(BaseModel):

    id = PrimaryKeyField(primary_key=True)
    data_hora = DateTimeField()
   
    class Meta:
        table_name = "tbupdatebot"
