from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver import Chrome as ChromeDriver
from selenium.webdriver.common.by import By
from threading import Thread
from datetime import datetime
from app.models.errors import Errors
from app.models.update_bot import UpdateBot
from app.utils.database_solution import DatabaseSolution
import wget, os, shutil


class BotReceitaFederal:

    __slots__ = ("settings", "motivos", "municipios", "naturezas", "paises", "simples", "cnaes", 
                 "empresas", "estabelecimentos", "link_arq", "link_site", "path", "data")

    def __init__(self, settings, data) -> None:
        self.settings = settings
        self.motivos = []
        self.municipios = []
        self.naturezas = []
        self.paises = []
        self.simples = []
        self.cnaes = []
        self.empresas = []
        self.estabelecimentos = []
        self.link_arq = self.settings.LINK_RFB_ARQ
        self.link_site = self.settings.LINK_RFB_SITE
        self.path = self.settings.PATH_ARQ_RFB
        self.data = data
        
    def __create_driver(self):

        service = ChromeService(ChromeDriverManager().install())
        options = ChromeOptions()
        options.add_argument("--headless=new")
        
        driver = ChromeDriver(service=service, options=options)
        driver.set_page_load_timeout(10)

        return driver
    
    def __fetch_links(self):

        driver = self.__create_driver()
        driver.get(self.link_arq)
        
        for s in self.__slots__:
            
            if s == "motivos":
                links = driver.find_elements(By.PARTIAL_LINK_TEXT, s.capitalize())
                self.motivos = [self.link_arq + l.text for l in links]

            if s == "municipios":
                links = driver.find_elements(By.PARTIAL_LINK_TEXT, s.capitalize())
                self.municipios = [self.link_arq + l.text for l in links]
            
            if s == "naturezas":
                links = driver.find_elements(By.PARTIAL_LINK_TEXT, s.capitalize())
                self.naturezas = [self.link_arq + l.text for l in links]
            
            if s == "paises":
                links = driver.find_elements(By.PARTIAL_LINK_TEXT, s.capitalize())
                self.paises = [self.link_arq + l.text for l in links]
            
            if s == "simples":
                links = driver.find_elements(By.PARTIAL_LINK_TEXT, s.capitalize())
                self.simples = [self.link_arq + l.text for l in links]

            if s == "cnaes":
                links = driver.find_elements(By.PARTIAL_LINK_TEXT, s.capitalize())
                self.cnaes = [self.link_arq + l.text for l in links]

            if s == "empresas":
                links = driver.find_elements(By.PARTIAL_LINK_TEXT, s.capitalize())
                self.empresas = [self.link_arq + l.text for l in links]

            if s == "estabelecimentos":
                links = driver.find_elements(By.PARTIAL_LINK_TEXT, s.capitalize())
                self.estabelecimentos = [self.link_arq + l.text for l in links]
            
        driver.quit()
    
    def __donwload_files(self, arquivos):

        path = os.path.abspath(".")
        path = path.replace("/app", "")
        path = path.replace("/utils", "")
        path = path.replace("\\app", "")
        path = path.replace("\\utils", "")
        path = os.path.join(path, self.path)

        for a in arquivos:
            print(f"Baixando o arquivo do link {a}\n")
            wget.download(a, f"{self.path}_{self.data.strftime('%Y%m%d')}")
            print(f"Arquivo {a} baixado com sucesso!\n")

    def __verify_last_update_rfb(self):
        
        driver = self.__create_driver()
        driver.get(self.link_site)
        driver.implicitly_wait(5)

        data_site = driver.find_element(By.XPATH, '//*[@id="collapseSidebar"]/div/div[2]/p/div[4]/div')
        data_site = datetime.strptime(data_site.text.replace("Última alteração: ", ""), '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        
        return data_site
        
    def __get_last_update_db(self):

        data = None

        try:
            ds = DatabaseSolution().get_database

            with ds.atomic() as transaction:
                
                try:
                    data = list(UpdateBot
                                .select(UpdateBot.data_hora)
                                .order_by(UpdateBot.data_hora.desc())
                                .limit(1)
                                .dicts())
                    if data:
                        data = data[0]["data_hora"].strftime('%Y-%m-%d %H:%M:%S')
                        
                except Exception as error:
                    Errors.create(procedimento="bot_receita_federal/__get_last_update",
                                  erro=f"{error}",
                                  data_hora=datetime.now())
        
        except Exception as error:
            Errors.create(procedimento="bot_receita_federal/__get_last_update",
                            erro=f"{error}",
                            data_hora=datetime.now())
        
        return data

    def __save_last_update_db(self, data):
        try:
            ds = DatabaseSolution().get_database

            with ds.atomic() as transaction:
                
                try:
                    UpdateBot(data_hora = data).save()

                except Exception as error:
                    transaction.rollback()
                    Errors.create(procedimento="bot_receita_federal/__save_last_update_db",
                                  erro=f"{error}",
                                  data_hora=datetime.now())
        
        except Exception as error:
            Errors.create(procedimento="bot_receita_federal/__get_last_update",
                            erro=f"{error}",
                            data_hora=datetime.now())
        
    def __donwload_all(self):
        
        Thread(target=self.__donwload_files, args=[self.motivos]).start()
        Thread(target=self.__donwload_files, args=[self.municipios]).start()
        Thread(target=self.__donwload_files, args=[self.naturezas]).start()
        Thread(target=self.__donwload_files, args=[self.paises]).start()
        Thread(target=self.__donwload_files, args=[self.simples]).start()
        Thread(target=self.__donwload_files, args=[self.cnaes]).start()
        Thread(target=self.__donwload_files, args=[self.empresas]).start()
        Thread(target=self.__donwload_files, args=[self.estabelecimentos]).start()

    def process(self):

        try:
            
            data_site = datetime.strptime(self.__verify_last_update_rfb(), '%Y-%m-%d %H:%M:%S')
            data_db = datetime.strptime(self.__get_last_update_db(), '%Y-%m-%d %H:%M:%S') if self.__get_last_update_db() else None

            if not data_db or (data_db < data_site):

                if os.path.isdir(f"{self.path}_{self.data.strftime('%Y%m%d')}"):
                    shutil.rmtree(f"{self.path}_{self.data.strftime('%Y%m%d')}")

                os.mkdir(f"{self.path}_{self.data.strftime('%Y%m%d')}")

                self.__fetch_links()
                self.__donwload_all()
                self.__save_last_update_db(data_site)
        
        except Exception as error:
            Errors.create(procedimento="bot_receita_federal/process",
                          erro=f"{error}",
                          data_hora=datetime.now()) 
