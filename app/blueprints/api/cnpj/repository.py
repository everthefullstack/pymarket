from app.utils.database_solution import DatabaseSolution


class CnpjRepository:
        
    __slots__ = ()
    
    def get_cnpjs(self, sql_where):
        
        try:
            db, schema = DatabaseSolution().get_database, DatabaseSolution().get_schema

            dataset = db.execute_sql(f"""SELECT json_agg(resultados) from
                                            (select *
                                            from 
                                                {schema}.tbestabelecimentos t1
                                            where {sql_where}) as resultados;
                                    """).fetchall()
            return dataset[0][0]
        
        except Exception as error:
            print(str(error))
            return error
    
