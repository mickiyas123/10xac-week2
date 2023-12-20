import psycopg2
import os
import traceback
import logging
import pandas as pd
import sys
from dotenv import load_dotenv
from sqlalchemy import  Column, Integer, String, MetaData, Table, Float
import csv

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
        'name': 'raw_vehicle',
        'columns': [
            Column('track_id', Integer, primary_key=True),
            Column('type', String),
            Column('traveled_d', Float),
            Column('avg_speed', Float),
        ]
    },
    {
        'name': 'raw_vehicle_trajectory',
        'columns': [
            Column('id', Integer, primary_key=True),
            Column('track_id', Integer),
            Column('lat', Float),
            Column('lon', Float),
            Column('speed', Float),
            Column('lon_acc', Float),
            Column('lat_acc', Float),
            Column('time', Float)
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

def load_csv_as_list(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file, delimiter=";")
        for row in csv_reader:
            modified_row = row[:1] + row[4:-1]
            data.append(modified_row)
    return data
def write_to_postgres():
    file_path = '../raw-data/20181024_d1_0830_0900.csv'
    #raw_vehichle = Table('raw_vehichle', connection.metadata, autoload_with=engine)

    df = pd.read_csv(file_path,index_col=False, delimiter='; ')

    raw_vehicle_data = df[['track_id', 'type', 'traveled_d', 'avg_speed']]
    raw_vehicle_data.to_sql('raw_vehicle', con=engine, if_exists='append', index=False)
    csv_data = load_csv_as_list(file_path)
    column_names = csv_data[0]
    data_rows = csv_data[1:]
    raw_vechicle_trajectory_list = []
    for i in range(0, len(data_rows)):
        id = data_rows[i][0]
        for j in range(1, len(data_rows[i]), 6):
            sublist = data_rows[i][j:j + 6]
            sublist.insert(0, id)
            raw_vechicle_trajectory_list.append(sublist)
    df_trajectory = pd.DataFrame(raw_vechicle_trajectory_list, columns=["track_id", "lat", "lon", "speed", "lon_acc", "lat_acc", "time"])
    df_trajectory.to_sql('raw_vehicle_trajectory', con=engine, if_exists='append', index=False)
create_postgres_table()
write_to_postgres()
