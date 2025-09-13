from typing import Final
from airflow import DAG
from airflow.sdk import Variable
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk.definitions.param import ParamsDict

from airflow.timetables.interval import CronDataIntervalTimetable
from pipeline_tools.data_models import HabrFeed
from pipeline_tools.parsers.habr import HabrParser
from pipeline_tools.db import ClickhouseService

params = {
    "offset": 1,
    "n_pages": 5
}

PAGES_PER_RUN: Final[int] = 5
HUB: Final[str] = "it-infrastructure"

def get_feeds(**context):

    offset = int(Variable.get("offset", default=1))
    n_pages = PAGES_PER_RUN

    habr_parser = HabrParser(
        "https://habr.com"
    )

    feeds = habr_parser.parse_hub_with_offset(
        hub=HUB,
        offset=offset,
        n_pages=n_pages
    )

    new_offset = offset + PAGES_PER_RUN
    Variable.set("offset", str(new_offset))

    return [feed.model_dump() for feed in feeds]

def save_feeds(**context):
    task_instance = context["task_instance"]
    data = task_instance.xcom_pull(task_ids="get_feeds_task")
    feeds = [HabrFeed(**feed) for feed in data]

    clickhouse_service = ClickhouseService(
        host="clickhouse",
    )

    for feed in feeds:
        clickhouse_service.save(feed)

with DAG(
    dag_id="Parsing_IT-Infrastructure_Hub",
    description="Парсит несколько страниц ленты за раз",
    schedule=CronDataIntervalTimetable("*/5 * * * *", timezone="Europe/Moscow"),
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
