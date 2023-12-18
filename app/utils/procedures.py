from datetime import datetime
from app.utils.database_solution import DatabaseSolution
from app.models.errors import Errors


#crescimento e declinio dos setores
def procedure_cresc_dec_setores():

    ds = DatabaseSolution()
    db = ds.get_database
    schema = ds.get_schema

    with db.atomic() as transaction:

        try:
            db.execute_sql(f"CALL {schema}.pr_cresc_dec_setores();")
            db.commit()

        except Exception as error:
            transaction.rollback()
            Errors.create(procedimento="procedures/procedure_cresc_dec_setores",
                          erro=str(error),
                          data_hora=datetime.now())
            
#porte das empresas de cada setor
def procedure_portes_emp_por_setor():
    
    ds = DatabaseSolution()
    db = ds.get_database
    schema = ds.get_schema

    with db.atomic() as transaction:

        try:
            db.execute_sql(f"CALL {schema}.pr_portes_emp_por_setor();")
            db.commit()

        except Exception as error:
            transaction.rollback()
            Errors.create(procedimento="procedures/procedure_portes_emp_por_setor",
                          erro=str(error),
                          data_hora=datetime.now())