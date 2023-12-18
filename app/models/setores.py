from playhouse.postgres_ext import PrimaryKeyField, JSONField, DateField
from app.models.base_model import BaseModel


class Setores(BaseModel):

    id = PrimaryKeyField(primary_key=True)
    conteudo = JSONField()
    data = DateField()

    class Meta:
        table_name = "tbsetores"
