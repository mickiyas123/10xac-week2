import psycopg2
from sqlalchemy import create_engine, text, Column, Integer, String, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError

class ConnectToPostgresDb:
    def __init__(self, db_params):
        try:
            print(type(db_params['host']))
            self.engine = create_engine(f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}")
            self.metadata = MetaData()
            self.metadata.bind = self.engine
        except Exception as error:
            raise Exception("Cannot connect to the database. Please try again.")
    def get_engine(self):
        return self.engine
    def create_tables(self, tables):
        try:
            for table_info in tables:
                table_name = table_info['name']
                columns = table_info['columns']
                table = Table(table_name, self.metadata, *columns)
                table.create(self.engine, checkfirst=True)
            return "Success"
        except SQLAlchemyError as e:
            error_message = f"Error creating tables: {str(e)}"
            return "Failure", error_message

