from playhouse.postgres_ext import PrimaryKeyField, CharField
from app.models.base_model import BaseModel


class Simples(BaseModel):

    id = PrimaryKeyField(primary_key=True)
    cnpj_basico = CharField(unique=True)
    opcao_simples = CharField()
    data_opcao_simples = CharField()
    data_exclusao_simples = CharField()
    opcao_mei = CharField()
    data_opcao_mei = CharField()
    data_exclusao_mei = CharField()
   
    class Meta:
        table_name = "tbsimples"

    @classmethod
    def upsert(cls, row):
        
        (cls
            .insert(row)
            .on_conflict(
                conflict_target=[cls.cnpj_basico],
                preserve=[],
                update=row)
            .execute()
        )