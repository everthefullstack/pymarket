from app.models.municipio import Municipios
from app.models.motivo import Motivos
from app.models.natureza import Naturezas
from app.models.pais import Paises
from app.models.simples import Simples
from app.models.cnae import Cnaes
from app.models.empresa import Empresas
from app.models.estabelecimento import Estabelecimentos
from app.models.setores import Setores
from app.models.portes import Portes
from app.models.update_tabela_geral import UpdateTabelaGeral
from app.models.update_bot import UpdateBot
from app.models.errors import Errors

class Tables:
    
    def __create_tables(self):
        
        tables = [Municipios,
                  Motivos,
                  Naturezas,
                  Paises,
                  Simples,
                  Cnaes,
                  Empresas,
                  Estabelecimentos,
                  Setores,
                  Portes,
                  UpdateTabelaGeral,
                  UpdateBot,
                  Errors]
        
        for table in tables:
            try:
                if table.table_exists():
                    print(f"Tabela {table._meta.table_name} já existe, não será criada.")
                    
                else:
                    table.create_table(safe=True)
                    print(f"Tabela {table._meta.table_name} criada com sucesso!")

            except Exception as error:
                print(f"Erro ao criar tabela => {error}")
    
    def init_app(self):
        self.__create_tables()


        