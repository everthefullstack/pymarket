from app.utils.database_solution import DatabaseSolution


class DashboardRepository:

    __slots__ = ()
    
    def get_dash_cresc_dec_set(self, dataset):

        try:
            db, schema = DatabaseSolution().get_database, DatabaseSolution().get_schema

            dataset = db.execute_sql(f"""select conteudo from {schema}.tbsetores 
                                     where id = {dataset["data_ini"]} or id = {dataset["data_fim"]}
                                     order by id;""").fetchall()
            return dataset
    
        except Exception as error:
            return error

    def get_dash_porte_set(self, dataset):

        try:
            db, schema = DatabaseSolution().get_database, DatabaseSolution().get_schema

            dataset = db.execute_sql(f"""select conteudo from {schema}.tbportes 
                                     where id = {dataset["data_ini"]} or id = {dataset["data_fim"]}
                                     order by id;""").fetchall()
            return dataset
    
        except Exception as error:
            return error
    
    def get_periodo_setores(self):

        try:
            db, schema = DatabaseSolution().get_database, DatabaseSolution().get_schema

            dataset = db.execute_sql(f"""select id, data from {schema}.tbsetores order by id;""").fetchall()
            return dataset
    
        except Exception as error:
            return error
    
    def get_periodo_portes(self):

        try:
            db, schema = DatabaseSolution().get_database, DatabaseSolution().get_schema

            dataset = db.execute_sql(f"""select id, data from {schema}.tbportes order by id;""").fetchall()
            return dataset
    
        except Exception as error:
            return error
        