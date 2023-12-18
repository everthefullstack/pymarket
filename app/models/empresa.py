from playhouse.postgres_ext import PrimaryKeyField, CharField, FloatField
from app.models.base_model import BaseModel


class Empresas(BaseModel):

    id = PrimaryKeyField(primary_key=True)
    cnpj = CharField(unique = True)
    razao_social = CharField()
    natureza_juridica = CharField()
    capital_social = FloatField()
    porte_empresa = CharField()
    ente_federativo = CharField()
   
    class Meta:
        table_name = "tbempresas"

    @classmethod
    def upsert(cls, row):
        
        (cls
            .insert(row)
            .on_conflict(
                conflict_target=[cls.cnpj],
                preserve=[],
                update=row)
            .execute()
        )