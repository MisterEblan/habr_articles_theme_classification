from typing import List
from src.pipeline_tools.db import DatabaseService
from src.pipeline_tools.data_models import HabrFeed, Page

import pytest

def test_feed(
    habr_feed: HabrFeed
):
    assert habr_feed

def test_clickhouse(
    clickhouse_service: DatabaseService,
    habr_feed: HabrFeed
):
    clickhouse_service.save(habr_feed)

    clickhouse_service.client.command("DELETE FROM habr_dataset WHERE 1=1")

def test_duplicate_clickhouse(
    clickhouse_service: DatabaseService,
    habr_feed: HabrFeed
):
    clickhouse_service.save(habr_feed)

    clickhouse_service.save(habr_feed)

    clickhouse_service.client.command("DELETE FROM habr_dataset WHERE 1=1")

def test_get_all(
    clickhouse_service: DatabaseService,
    habr_feed: HabrFeed
):
    clickhouse_service.save(habr_feed)

    data = clickhouse_service.get_all()

    assert isinstance(data, list)
    assert all(
        isinstance(el, Page) for el in data
    )

    clickhouse_service.client.command("DELETE FROM habr_dataset WHERE 1=1")
