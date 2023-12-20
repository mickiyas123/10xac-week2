import psycopg2
import os
import traceback
import logging
import pandas as pd
import sys
from dotenv import load_dotenv
from sqlalchemy import  Column, Integer, String, MetaData, Table, Float

rpath = os.path.abspath('..')
if rpath not in sys.path:
    sys.path.insert(0, rpath)
load_dotenv()

from db_connection.connect_to_postgres import ConnectToPostgresDb

db_host = os.getenv("POSTGRES_HOST")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_port = os.getenv("POSTGRES_PORT")
db_database = os.getenv("POSTGRES_DB")
db_params = {
    'host': db_host,
    'user': db_user,
    'password': db_password,
    'port': db_port,
    'database': db_database
}
connection = ConnectToPostgresDb(db_params)
engine = connection.get_engine()

print(db_params)

def create_postgres_table():
    tables_info = [
    {
        'name': 'raw_vehichle',
        'columns': [
            Column('track_id', Integer, primary_key=True),
            Column('type', String),
            Column('traveled_d', Float),
            Column('avg_speed', Float),
        ]
    },
    {
        'name': 'raw_vechicle_trajectory',
        'columns': [
            Column('id', Integer, primary_key=True),
            Column('track_id', Integer),
            Column('lat', Float),
            Column('lon', Float),
            Column('speed', Float),
            Column('lon_acc', Float),
            Column('lat_acc', Float),
            Column('time', Integer)
            ]
        },
    # Add more tables as needed
    ]

    # Create tables using the engine
    result = connection.create_tables(tables_info)

    if result == "Success":
        print("Tables created successfully!")
    else:
        status, error_message = result
        print(f"Table creation failed. Error: {error_message}")
def write_to_postgres():
    file_path = '../raw-data/20181024_d1_0830_0900.csv'
    df = pd.read_csv(file_path)
    raw_vehicle_data = df[['track_id', 'type', 'traveled_d', 'avg_speed']]
    repeated_columns = df.columns[4:]
write_to_postgres()
