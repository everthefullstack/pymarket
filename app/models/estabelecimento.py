from playhouse.postgres_ext import PrimaryKeyField, CharField, DateField, TextField
from app.models.base_model import BaseModel
from peewee import SQL


class Estabelecimentos(BaseModel):

    id = PrimaryKeyField(primary_key=True)
    cnpj_basico = CharField(null = True)
    cnpj_ordem = CharField(null = True)
    cnpj_dv = CharField(null = True)
    identificador_mf = CharField(null = True)
    nome_fantasia = CharField(null = True)
    situacao_cadastral = CharField(null = True)
    data_situacao_cadastral = DateField(null = True)
    motivo_situacao_cadastral = CharField(null = True)
    nome_cidade_exterior = CharField(null = True)
    pais = CharField(null = True)
    data_inicio_atividade = DateField(null = True)
    cnae_primario = CharField(null = True)
    cnae_secundario = TextField(null = True)
    tipo_logradouro = CharField(null = True)
    logradouro = CharField(null = True)
    numero = CharField(null = True)
    complemento = CharField(null = True)
    bairro = CharField(null = True)
    cep = CharField(null = True)
    uf = CharField(null = True)
    municipio = CharField(null = True)
    ddd1 = CharField(null = True)
    telefone1 = CharField(null = True)
    ddd2 = CharField(null = True)
    telefone2 = CharField(null = True)
    ddd3 = CharField(null = True)
    telefone3 = CharField(null = True)
    email = CharField(null = True)
    situacao_especial = CharField(null = True)
    data_situacao_especial = DateField(null = True)
   
    class Meta:
        table_name = "tbestabelecimentos"
        #constraints = [SQL('UNIQUE (cnpj_basico, cnpj_ordem, cnpj_dv)')]

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