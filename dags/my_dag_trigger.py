from datetime import datetime, timedelta
from random import randint
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator,BranchPythonOperator

default_args = {
    'owner': 'satyendra',
    'retries': 0,
    'retry_delay': timedelta(minutes=2)
}




with DAG(
    dag_id='my_dag_trigger',
    default_args=default_args,
    description='This is our third dag that we write',
    start_date=datetime(2024,5,5),
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    task_A=PythonOperator(
        task_id='task_id_A',
        python_callable=lambda: raise_exception("Failure of task")
    )

    task_B=PythonOperator(
        task_id='task_id_B',
        python_callable=lambda: raise_exception("Failure of task")
    )
    task_C=PythonOperator(
        task_id='task_id_C',
        python_callable=lambda: print("Execution of task C"),
        trigger_rule='all_failed'
    )

    task_D=PythonOperator(
        task_id='task_id_D',
        python_callable=lambda: print("Execution of task D"),
        
    )

    [task_A,task_B]>>task_C >> task_D