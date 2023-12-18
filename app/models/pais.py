from playhouse.postgres_ext import PrimaryKeyField, CharField
from app.models.base_model import BaseModel


class Paises(BaseModel):

    id = PrimaryKeyField(primary_key=True)
    codigo = CharField(unique=True)
    descricao = CharField()

    class Meta:
        table_name = "tbpaises"

    @classmethod
    def upsert(cls, row):
        
        (cls
            .insert(row)
            .on_conflict(
                conflict_target=[cls.codigo],
                preserve=[],
                update=row)
            .execute()
        )