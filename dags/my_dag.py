from datetime import datetime, timedelta
from random import randint
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator,BranchPythonOperator

default_args = {
    'owner': 'satyendra',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def training_model():
    return randint(1,10)

def choose_best_model(ti):
    accuracies=ti.xcom_pull(task_ids=[
        'training_model_A',
        'training_model_B',
        'training_model_C'
    ])
    best_accuracy = max(accuracies)
    if(best_accuracy > 8):
        return 'accurate'
    return 'inaccurate'

with DAG(
    dag_id='my_dag_v1',
    default_args=default_args,
    description='This is our second dag that we write',
    start_date=datetime(2024,5,5),
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    training_model_A=PythonOperator(
        task_id='training_model_A',
        python_callable=training_model
    )
    training_model_B=PythonOperator(
        task_id='training_model_B',
        python_callable=training_model
    )
    training_model_C=PythonOperator(
        task_id='training_model_C',
        python_callable=training_model
    )
    choose_best_model_task=BranchPythonOperator(
        task_id='choose_best_model',
        python_callable=choose_best_model
    )
    accurate=BashOperator(
        task_id="accurate",
        bash_command="echo 'accurate'"
    )
    inaccurate=BashOperator(
        task_id="inaccurate",
        bash_command="echo 'inaccurate'"
    )

    [training_model_A, training_model_B, training_model_C] >> choose_best_model_task >> [accurate,inaccurate]


    
