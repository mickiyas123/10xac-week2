from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
import pandas as pd
import logging

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
        task_id='load_data_task_one',
        python_callable=load_data
    )
