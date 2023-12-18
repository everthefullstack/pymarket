from app.utils.etl_receita_federal import EtlReceitaFederal
from app.utils.bot_receita_federal import BotReceitaFederal
from app.utils.procedures import procedure_cresc_dec_setores, procedure_portes_emp_por_setor
from dynaconf import Dynaconf
from datetime import datetime


data = datetime.now()
settings = Dynaconf(settings_files=["settings.toml", ".env"], environments=True, load_dotenv=True)

BotReceitaFederal(settings=settings, data=data).process()
EtlReceitaFederal(settings=settings, data=data).process()

procedure_cresc_dec_setores()
procedure_portes_emp_por_setor()
