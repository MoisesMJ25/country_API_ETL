
import os
import pandas as pd
import logging
from sqlalchemy import create_engine, MetaData, Column, String, Integer, NVARCHAR, DateTime, Table, inspect, exc
from sqlalchemy.types import NVARCHAR, Text

class lead:
    def __init__(self, config:dict, schema:str):
        self.config = config
        self.schema = schema
        self.db_engine = None
    
    def conn(self):
        credencials = {
            "REDSHIFT_USERNAME" : os.getenv('REDSHIFT_USERNAME'),
            "REDSHIFT_PASSWORD" : os.getenv('REDSHIFT_PASSWORD'),
            "REDSHIFT_HOST" : os.getenv('REDSHIFT_HOST'),
            "REDSHIFT_PORT" : os.getenv('REDSHIFT_PORT', '5439'),
            "REDSHIFT_DBNAME" : os.getenv('REDSHIFT_DBNAME')
        }

        url_conn = f"postgresql+psycopg2://{credencials['REDSHIFT_USERNAME']}:{credencials['REDSHIFT_PASSWORD']}@{credencials['REDSHIFT_HOST']}:{credencials['REDSHIFT_PORT']}/{credencials['REDSHIFT_DBNAME']}"
        self.db_engine = create_engine(url_conn)

        try:
            with self.db_engine.connect() as connection:
                result = connection.execute('SELECT 1;')
                if result:
                    logging.info("Connection created")
                return result
                
        except Exception as e:
            logging.error(f"Failed to create connection: {e}")

            raise
    
    def create_table(self, data, table_name:str):
        if self.db_engine is None:
            
            print(f'Trying the connection first! ------------> conn: {self.db_engine}')
            try:
                self.conn()

            except Exception as e:
                logging.error(f"Failed connection: {e}")
        
        try:
            metadata = MetaData(schema=self.schema)
            columns = []

            for col_name, col_type in zip(data.columns, data.dtypes):

                if pd.api.types.is_integer_dtype(col_type):
                    columns.append(Column(col_name, Integer))
                elif pd.api.types.is_float_dtype(col_type):
                    columns.append(Column(col_name, String))
                elif pd.api.types.is_string_dtype(col_type):
                    columns.append(Column(col_name, NVARCHAR (length=60000)))
                elif pd.api.types.is_datetime64_any_dtype(col_type):
                    columns.append(Column(col_name, DateTime))  
                else:
                    raise TypeError(f"Unsupported dtype: {col_type}")

            inspector = inspect(self.db_engine)
            table_exists = inspector.has_table(table_name, schema=self.schema)

            if table_exists:
                try:
                    with self.db_engine.connect() as connection:
                        connection.execute(f'DROP TABLE IF EXISTS "{self.schema}"."{table_name}"')
                    print(f"Table {table_name} dropped successfully.")

                except exc.SQLAlchemyError as e:
                    print(f"Error occurred while dropping the table: {e}")
                    raise
            
            Table(table_name, metadata, *columns)

            data.to_sql(table_name, self.db_engine, index=False, if_exists='append', schema=self.schema)
            print(table_name, 'data.........................................OK')

            return 1
        except Exception as e:
            logging.error(f"Check this: {e}")
            print(f"Failed to upload table {table_name}: {e}")
            return 0


    def upload_data(self, data:pd.DataFrame, data_name:str):
        try:
            data.to_sql(
                data_name,
                con=self.db_engine,
                if_exists='replace',
                index=False
                        )
            print(f'Data have been uploaded to {self.schema}.{data_name} table in redshift')
        except Exception as e:
            print('Error, we have a problem uploading the data to redshift:\n{e}')
            raise
    
    def close_conn(self):
        if self.db_engine:
            self.db_engine.dispose()
            logging.info("Connection to Redshift closed.")
        else:
            logging.warning("No active connection to close.")
