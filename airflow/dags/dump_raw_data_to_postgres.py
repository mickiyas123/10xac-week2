from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
import sys
import pandas as pd
import os
from sqlalchemy import create_engine, text


# cwd=os.getcwd()
# sys.path.append(f'../raw-data/')
# sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))

engine = create_engine(
    'postgresql+psycopg2://airflow:airflow@host.docker.internal:5478/postgres'
    )

def load_csv_as_list(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file, delimiter=";")
        for row in csv_reader:
            modified_row = row[:1] + row[4:-1]
            data.append(modified_row)
    return data
def write_to_database():
    file_path = '/opt/airflow/dags/20181024_d1_0830_0900.csv'
    df = pd.read_csv(file_path,index_col=False, delimiter='; ', engine='python')
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


default_args = {
    'owner': '10 academy',
    'start_date':datetime(2003, 1, 1),
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_to_dum_raw_data_to_postgres',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:
    task_one = PostgresOperator(
        task_id='create_raw_data_storing_tables',
        postgres_conn_id='week_two_dwh',
        sql="sql/raw_data_schema.sql"
    )
    
    # task_two = PythonOperator(
    #     task_id='load_raw_data_to_postgres',
    #     python_callable=write_to_database
    # )
    
    task_three = BashOperator(
        task_id="run_dbt",
        bash_command='dbt_run'
    )

    task_one >> task_three
    
