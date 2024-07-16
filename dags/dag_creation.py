from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from utils import email_success, email_failed


default_args = {
    'owner': 'Moisés',
    'start_date': datetime(2024,6,25),
    'retries':2,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    default_args=default_args,
    dag_id="dag_ETL_Country_API",
    start_date=datetime(2024, 7, 3),
    schedule="@daily",
    doc_md='dag que realiza ETL desde una API de países',
    catchup=False,
    on_success_callback=email_success,
    on_failure_callback=email_failed
) as dag:
    
    only_task = BashOperator(
        task_id='ETL_API',
        bash_command='python ${AIRFLOW_HOME}/dags/utils/__main__.py'
    )

    only_task
