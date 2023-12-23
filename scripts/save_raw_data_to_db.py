import psycopg2
import os
import traceback
import pandas as pd
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import csv

rpath = os.path.abspath('..')
if rpath not in sys.path:
    sys.path.insert(0, rpath)
load_dotenv()

host ="localhost"  # os.getenv("HOST")
user = "airflow"   # os.getenv("USER")
password = "airflow" # os.getenv("PASSWORD")
port = 5478 # os.getenv("PORT")
database = "vehicle_dwh" #  os.getenv("DB")
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
class ExtractAndSaveToDatabase:
    def load_csv_as_list(self, file_path):
        data = []
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file, delimiter=";")
            for row in csv_reader:
                modified_row = row[:1] + row[4:-1]
                data.append(modified_row)
        return data
    def check_csv_file(self, file_path):
        """"
         check if csv file has been loaded before and the status of the csv file has been loaded before it return false
        """
        csv_file_name = file_path.split("/")[1]
        with engine.connect() as connection:
            check_status_query = text("SELECT status FROM csv_file_name WHERE name = :csv_file_name AND status = 'completed'")
            status_result = connection.execute(check_status_query, csv_file_name=csv_file_name).fetchone()

        if status_result:
            return True
        return False
    def write_to_database(self):
        file_path = '../raw-data/20181024_d1_0830_0900.csv'
        #check_csv = self.check_csv_file(file_path)
        #if (not check_csv):
           # raise ValueError("The CSV file has already been loaded and its status is 'completed'.")
        df = pd.read_csv(file_path,index_col=False, delimiter='; ')
        raw_vehicle_data = df[['track_id', 'type', 'traveled_d', 'avg_speed']]
        raw_vehicle_data.to_sql('raw_vehicle', con=engine, if_exists='append', index=False)
        csv_data = self.load_csv_as_list(file_path)
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
