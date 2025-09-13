from pipeline_tools.db import ClickhouseService
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

import pandas as pd

def save_db_to_csv(**context):
    db_service = ClickhouseService(
        host="clickhouse"
    )

    all_pages = db_service.get_all()

    pages_dicts = [
        page.model_dump() 
        for page in all_pages
    ]

    now = datetime.now()
    now = datetime.strftime(now, "%d_%m_%Y_%H_%M")
    filename = f"./habr_dataset_{now}.csv"

    df = pd.DataFrame(pages_dicts)

    df.to_csv(
        filename,
        index=False,
        encoding="utf-8"
    )

    print(f"Сохранено {len(pages_dicts)} страниц в {filename}")

with DAG(
    dag_id="Save_DB_to_CSV",
    description="Сохраняет базу данных в CSV файл",
    schedule="@hourly"
):
    t1 = PythonOperator(
        task_id="save_to_csv_task",
        python_callable=save_db_to_csv
    )

    t1
