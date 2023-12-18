from playhouse.postgres_ext import PrimaryKeyField, CharField
from app.models.base_model import BaseModel


class Cnaes(BaseModel):

    id = PrimaryKeyField(primary_key=True)
    codigo = CharField(null = True, unique=True)
    descricao = CharField(null = True)

    class Meta:
        table_name = "tbcnaes"

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