from app.utils.database_solution import DatabaseSolution
from app.models.municipio import Municipios
from app.models.cnae import Cnaes
from app.models.empresa import Empresas
from app.models.estabelecimento import Estabelecimentos
from app.models.simples import Simples
from app.models.motivo import Motivos
from app.models.pais import Paises
from app.models.natureza import Naturezas
from app.models.errors import Errors
from datetime import datetime
import os, sys, zipfile, pandas as pd, numpy as np


class EtlReceitaFederal:
     
    __slots__ = ("arquivos", "settings", "delimeter", "encoding", "chunksize", "dtype", "data",)

    def __init__(self, settings, data) -> None:
        self.arquivos = ["motivos", "municipios", "naturezas", "paises", "simples", "cnaes", "empresas", "estabelecimentos"]
        self.settings = settings
        self.delimeter = ";"
        self.encoding = "latin-1"
        self.chunksize = 10000
        self.dtype = str
        self.data = data

    def __insert_many_data(self, num, arquivo, chunk):

        try:

            print(f"Inserindo o chunk número {num}, arquivo {arquivo}, chunksize {self.chunksize}. insert_many_data")

            classe = self.__fetch_class_name(arquivo)
            ds = DatabaseSolution().get_database

            with ds.atomic() as transaction:

                try:
                    classe.insert_many(rows=chunk.to_records(index=False)).execute()

                except Exception as error:
                    transaction.rollback()
                    Errors.create(procedimento="etl_receita_federal/__insert_many_data",
                          erro=f"{error} / {arquivo}",
                          data_hora=datetime.now())
                    
                    return False
                
            return True
        
        except Exception as error:
            Errors.create(procedimento="etl_receita_federal/__insert_many_data",
                          erro=f"{error} / {arquivo}",
                          data_hora=datetime.now())
            return False
    
    def __insert_single_data(self, num, arquivo, chunk):

        try:

            print(f"Inserindo o chunk número {num}, arquivo {arquivo}, chunksize {self.chunksize}. insert_single_data")

            classe = self.__fetch_class_name(arquivo)
            ds = DatabaseSolution().get_database

            for row in chunk.to_records(index=False):

                with ds.atomic() as transaction:
                    try:

                        new_row = self.__create_dict_update(classe._meta.fields, row.tolist())
                        classe.upsert(row=new_row)
                        transaction.commit()

                    except Exception as error:
                        transaction.rollback()
                        Errors.create(procedimento="etl_receita_federal/__insert_single_data",
                                      erro=f"{error} / {arquivo} / {new_row}",
                                      data_hora=datetime.now())
                        

        except Exception as error:
            Errors.create(procedimento="etl_receita_federal/__insert_single_data",
                          erro=f"{error} / {arquivo}",
                          data_hora=datetime.now())
    
    def __insert_data(self, num, arquivo, chunk):

        confirm = self.__insert_many_data(num, arquivo, chunk)

        if confirm:
            pass
        else: 
            confirm = self.__insert_single_data(num, arquivo, chunk)

    def __create_dict_update(self, cols, row):
        
        combined_dict = None
        
        try:
            col = [key for key in cols][1:]

            if len(col) == len(row):
                combined_dict = dict(zip(col, row))

        except Exception as error:
            Errors.create(procedimento="etl_receita_federal/__create_dict_update",
                          erro=f"{error}",
                          data_hora=datetime.now())
        
        return combined_dict
    
    def __fetch_class_name(self, arquivo):
        classe = getattr(sys.modules[__name__], self.__clean_name(arquivo))
        return classe
    
    def __clean_name(self, arquivo):
        try:
            arquivo = arquivo.replace(".zip", "")
            arquivo = "".join(arq for arq in arquivo if arq.isalpha())
            return arquivo
        
        except Exception as error:
            Errors.create(procedimento="etl_receita_federal/__clean_name",
                          erro=f"{error} / {arquivo}",
                          data_hora=datetime.now())
    
    def __clean_nan(self, chunk):
        chunk.fillna("NC", inplace=True)
        return chunk

    def __sanitize_municipio(self, pre_sanitized, arquivo):
        try:
            return pre_sanitized
        
        except Exception as error:
            Errors.create(procedimento="etl_receita_federal/__sanitize_municipio",
                          erro=f"{error} / {arquivo}",
                          data_hora=datetime.now())
    
    def __sanitize_cnaes(self, pre_sanitized, arquivo):
        try:
            return pre_sanitized
        
        except Exception as error:
            Errors.create(procedimento="etl_receita_federal/__sanitize_cnaes",
                          erro=f"{error} / {arquivo}",
                          data_hora=datetime.now())
    
    def __sanitize_empresas(self, pre_sanitized:pd.DataFrame, arquivo):
        
        try:
            pre_sanitized.iloc[:,[4]] = np.array([float(value.replace(',', '.')) for value in pre_sanitized.iloc[:,[4]].values[0]])
            pre_sanitized = pre_sanitized.drop(pre_sanitized.columns[3], axis=1)
            return pre_sanitized
        
        except Exception as error:
            Errors.create(procedimento="etl_receita_federal/__sanitize_empresas",
                          erro=f"{error} / {arquivo}",
                          data_hora=datetime.now())
    
    def __sanitize_estabelecimentos(self, pre_sanitized, arquivo):
        try:
            pre_sanitized.iloc[:,[6, 10, 29]] = np.where(pre_sanitized.iloc[:,[6,10,29]].eq('NC') | pre_sanitized.iloc[:,[6,10,29]].eq("0"), "15000101", pre_sanitized.iloc[:,[6, 10, 29]])
            return pre_sanitized
        
        except Exception as error:
            Errors.create(procedimento="etl_receita_federal/__sanitize_estabelecimentos",
                          erro=f"{error} / {arquivo}",
                          data_hora=datetime.now())
    
    def __sanitize_motivos(self, pre_sanitized, arquivo):
        try:
            return pre_sanitized
        
        except Exception as error:
            Errors.create(procedimento="etl_receita_federal/__sanitize_motivos",
                          erro=f"{error} / {arquivo}",
                          data_hora=datetime.now())
    
    def __sanitize_naturezas(self, pre_sanitized, arquivo):
        try:
            return pre_sanitized
        
        except Exception as error:
            Errors.create(procedimento="etl_receita_federal/__sanitize_naturezas",
                          erro=f"{error} / {arquivo}",
                          data_hora=datetime.now())
    
    def __sanitize_paises(self, pre_sanitized, arquivo):
        try:
            return pre_sanitized
        
        except Exception as error:
            Errors.create(procedimento="etl_receita_federal/__sanitize_paises",
                          erro=f"{error} / {arquivo}",
                          data_hora=datetime.now())
    
    def __sanitize_simples(self, pre_sanitized, arquivo):
        try:
            return pre_sanitized
        
        except Exception as error:
            Errors.create(procedimento="etl_receita_federal/__sanitize_simples",
                          erro=f"{error} / {arquivo}",
                          data_hora=datetime.now())
            
    def __data_sanitizer(self, chunk, arquivo):
        try:
            pre_sanitized = self.__clean_nan(chunk)
            sanitized = None

            match arquivo:
                case "Municipios":
                    sanitized = self.__sanitize_municipio(pre_sanitized, arquivo)
                case "Cnaes":
                    sanitized = self.__sanitize_cnaes(pre_sanitized, arquivo)
                case "Empresas":
                    sanitized = self.__sanitize_empresas(pre_sanitized, arquivo)
                case "Estabelecimentos":
                    sanitized = self.__sanitize_estabelecimentos(pre_sanitized, arquivo)
                case "Motivos":
                    sanitized = self.__sanitize_motivos(pre_sanitized, arquivo)
                case "Naturezas":
                    sanitized = self.__sanitize_naturezas(pre_sanitized, arquivo)
                case "Paises":
                    sanitized = self.__sanitize_paises(pre_sanitized, arquivo)
                case "Simples":
                    sanitized = self.__sanitize_simples(pre_sanitized, arquivo)

            return sanitized
        
        except Exception as error:
            Errors.create(procedimento="etl_receita_federal/__data_sanitizer",
                          erro=f"{error} / {arquivo}",
                          data_hora=datetime.now())

    def __fetch_file_names(self):

        try:

            lista_arquivos = []
            for arquivo in self.arquivos:
                lista = [arq for arq in os.listdir(f"{self.settings.DATABASE_FILES}_{self.data.strftime('%Y%m%d')}") if arquivo in arq.lower()]
                if lista:
                    lista_arquivos.append(lista)
            
            return lista_arquivos

        except Exception as error:
            Errors.create(procedimento="etl_receita_federal/__fetch_file_names",
                          erro=f"{error}",
                          data_hora=datetime.now())

    def __etl_file(self, arquivo):

        if arquivo == "Empresas0.zip":
            file = zipfile.ZipFile(f"{self.settings.DATABASE_FILES}_{self.data.strftime('%Y%m%d')}/{arquivo}")
            with file.open(file.filelist[0].filename, "r") as dataset:

                try:
                    for num, chunk in enumerate(pd.read_csv(dataset, 
                                                            encoding=self.encoding, 
                                                            delimiter=self.delimeter, 
                                                            chunksize=self.chunksize, 
                                                            dtype=self.dtype,
                                                            header=None)):
                        
                        sanitized_chunk = self.__data_sanitizer(chunk, self.__clean_name(arquivo))
                        self.__insert_data(num, arquivo, sanitized_chunk)

                except Exception as error:
                    Errors.create(procedimento="etl_receita_federal/__etl_file",
                                erro=f"{error} / {arquivo}",
                                data_hora=datetime.now())

    def process(self):
        
        ini = datetime.now()

        lista_arquivos = self.__fetch_file_names()

        for arquivos in lista_arquivos:
            for arquivo in arquivos:
                self.__etl_file(arquivo)

        fim = datetime.now()

        print(f"Começou em {ini} e terminou em {fim}")
