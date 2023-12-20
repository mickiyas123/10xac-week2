from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from random import randint



def training_model():
    return randint(1, 10)

# Create instance of dag class
with DAG("my_dag", start_date=datetime(2023, 11, 19),
         schedule_interval="@daily", catchup=False) as dag:
    # Add Task 
    training_model_A = PythonOperator(
        task_id="training_model_A",
        python_callable=training_model
    )
    
    training_model_A = PythonOperator(
        task_id="training_model_B",
        python_callable=training_model
    )
    
    training_model_A = PythonOperator(
        task_id="training_model_C",
        python_callable=training_model
    )