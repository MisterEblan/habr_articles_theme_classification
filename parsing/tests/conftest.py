import pytest
import json

from src.pipeline_tools.data_models import HabrFeed
from src.pipeline_tools.db import DatabaseService, ClickhouseService
from src.pipeline_tools.parsers import FeedParser, HabrParser

@pytest.fixture
def habr_link() -> str:
    return "https://habr.com"

@pytest.fixture
def habr_parser(habr_link: str) -> FeedParser:
    return HabrParser(base_url=habr_link)

@pytest.fixture
def habr_feed() -> HabrFeed:
    with open("tests/data/feed.json", "r") as f:
        content = json.load(f)

    return HabrFeed(**content)

@pytest.fixture
def clickhouse_service() -> DatabaseService:
    return ClickhouseService(
        host="localhost",
        user="admin",
        password="admin",
        database="habr_data"
    )
