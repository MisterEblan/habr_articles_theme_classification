from abc import ABC, abstractmethod
import logging
from typing import Generic, List, TypeVar

import clickhouse_connect
import warnings

from clickhouse_connect.driver.summary import QuerySummary

from .data_models import HabrFeed, Page
from .parsers import AbstractFeed

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

AbstractDatabaseOutput = TypeVar("AbstractDatabaseOutput")


class DatabaseService(ABC, Generic[AbstractFeed, AbstractDatabaseOutput]):
    """Базовый класс для работы с базами данных"""

    @abstractmethod
    def save(self, feed: AbstractFeed) -> AbstractDatabaseOutput:
        """Метод для сохранения фида в базу данных"""
        
        pass

    @abstractmethod
    def get_all(self) -> List[Page]:
        """Метод для получения всех записей из БД"""

        pass


class ClickhouseService(DatabaseService[HabrFeed, QuerySummary]):
    """Класс для работы с ClickHouse"""

    def __init__(
        self,
        host: str,
        user: str="admin",
        password: str ="admin",
        database: str="habr_data",
    ):
        """
        Args:
            host: хост Clickhouse.
            user: пользователь в Clickhouse.
            password: пароль пользователя.
            database: база данных в Clickhouse.
        """
        self.user = user
        self.password = password

        self.client = clickhouse_connect.get_client(
            host=host,
            username=user,
            password=password,
            database=database
        )

        assert self.client.query("SELECT version()")

    def _is_page_exists(self, id: str) -> bool:
        """Проверка на наличие страницы в базе данных

        Args:
            id: идентификатор страницы.

        Returns:
            bool: найдена ли страница в БД.
        """
        logger.debug(f"Проверка статьи \"{id}\" на существование в базе данных")
        result = self.client.query(
            f"SELECT title FROM habr_dataset WHERE id={id}"
        ).result_columns

        logger.info(f"Result columns: {result}")
        logger.info("Columns type: %s", type(result))

        return bool(result)

    def save(self, feed: HabrFeed) -> QuerySummary:
        """Сохраняет ленту страниц в БД

        Args:
            feed: лента страниц.

        Returns:
            QuerySummary: сводка по операции.
        """
        logger.info(f"Сохранение {len(feed.pages)} страниц")

        for page in feed.pages:
            if self._is_page_exists(str(page.id)):
                feed.pages.remove(page)
                logger.warning(
                    f"Статья \"{page.title}\" уже есть в базе данных"
                )
                continue


        data_tuples = [
            (str(page.id), page.title, page.content, page.hub)
            for page in feed.pages
        ]

        result = self.client.insert(
            "habr_dataset",
            data_tuples,
            column_names=["id", "title", "content", "hub"]
                           )

        return result


    def get_all(self) -> List[Page]:
        """Получение всех страниц из базы данных

        Returns:
            List[Page]: список всех страниц из базы данных.
        """
        logger.info("Getting all pages")

        data = self.client.query("SELECT * FROM habr_dataset")
        data_tuples = data.result_set

        logger.info(f"Получили {len(data_tuples)} страниц")

        pages = [
            Page(
                id=data_tuple[0],
                title=data_tuple[1],
                content=data_tuple[2],
                hub=data_tuple[3]
            )
            for data_tuple in data_tuples
        ]


        return pages
