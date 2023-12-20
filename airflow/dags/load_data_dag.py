from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
import pandas as pd
import sys
import os

#rpath = os.path.abspath('../../scripts/')
#if rpath not in sys.path:
    #sys.path.insert(0, rpath)

#from write_csv_to_postgres import ExtractAndSaveToDatabase

#create_postgres_table = ExtractAndSaveToDatabase.create_postgres_table()
#write_to_postgres = ExtractAndSaveToDatabase.write_to_postgres()

default_args = {
    'owner': 'Mickiyas',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def load_data():
    file_path = '../raw-data/20181024_d1_0830_0900.csv'
    
    df = pd.read_csv(file_path)
    logger = logging.getLogger(__name__)
    logger.info("This is a log message")

with DAG(dag_id='load_data', default_args=default_args, schedule_interval='*/1 * * * *', catchup=False) as dag:
    task1 = PythonOperator(
        task_id='create_database_to_store_raw_data',
        python_callable=load_data
    )

    #task2 = PythonOperator(
        #task_id='save_raw_data_to_databse_tables',
       # python_callable=write_to_postgres
    #)
