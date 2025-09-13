from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk.definitions.param import ParamsDict

from pipeline_tools.data_models import HabrFeed
from pipeline_tools.parsers import HabrParser
from pipeline_tools.db import ClickhouseService

params = {
    "offset": 1,
    "n_pages": 5
}

def get_feeds(**context):

    offset = context["params"]["offset"]
    n_pages = context["params"]["n_pages"]

    habr_parser = HabrParser(
        "https://habr.com"
    )

    feeds = habr_parser.parse_with_offset(
        offset=offset,
        n_pages=n_pages
    )

    return [feed.model_dump() for feed in feeds]

def save_feeds(**context):
    task_instance = context["task_instance"]
    data = task_instance.xcom_pull(task_ids="get_feeds_task")
    feeds = [HabrFeed(**feed) for feed in data]

    clickhouse_service = ClickhouseService(
        host="clickhouse",
        port=9000
    )

    for feed in feeds:
        clickhouse_service.save(feed)

with DAG(
    dag_id="parse_habr_with_offset",
    description="Парсит несколько страниц ленты за раз",
    params=ParamsDict(params)
):
    get_feeds_task = PythonOperator(
        task_id="get_feeds_task",
        python_callable=get_feeds
    )

    save_feeds_task = PythonOperator(
        task_id="save_feeds_task",
        python_callable=save_feeds
    )

    get_feeds_task >> save_feeds_task
