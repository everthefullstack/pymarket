from app.utils.database_solution import DatabaseSolution


class CnaeRepository:

    __slots__ = ()
    
    def get_cnaes(self, sql_where):
        
        try:
            db, schema = DatabaseSolution().get_database, DatabaseSolution().get_schema

            dataset = db.execute_sql(f"""SELECT json_agg(resultados) from
                                            (select 
                                                t1.descricao, 
                                                t2.cnae_primario, 
                                                t2.cnae_secundario, 
                                                concat(t2.cnpj_basico, t2.cnpj_ordem, t2.cnpj_dv) as cnpj  
                                            from 
                                                {schema}.tbcnaes t1
                                            inner join
                                                {schema}.tbestabelecimentos t2 on t2.cnae_primario = t1.codigo 
                                            where {sql_where}) as resultados;
                                    """).fetchall()
            return dataset[0][0]
        
        except Exception as error:
            return error