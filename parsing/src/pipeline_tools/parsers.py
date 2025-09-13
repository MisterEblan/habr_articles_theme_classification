from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, TypeVar, Generic, Union
from bs4 import BeautifulSoup

import requests
import logging
import re

from .errors import (
    EmptyBodyError,
    HubNotFound,
    LinkTagError,
    LinksNotFound,
    InvalidUrlError,
    ZeroOffsetError
)
from .data_models import Feed, HabrFeed, Page, PageInfo

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



AbstractFeed = TypeVar("AbstractFeed", bound=Feed)
class FeedParser(ABC, Generic[AbstractFeed]):
    """Базовый класс для парсеров лент сайтов"""

    @abstractmethod
    def parse(self) -> AbstractFeed:
        """Метод для получения ленты сайта

        Returns:
            AbstractFeed: абстрактная лента страниц.
        """
        pass

    @abstractmethod
    def parse_with_offset(
            self,
            offset: int,
            n_pages: int = 5
    ) -> List[AbstractFeed]:
        """Метод для парсинга нескольких страниц ленты с оффсетом

        Args:
            offset: смещение ленты.
            n_pages: количество страниц ленты для парсинга.

        Returns:
            List[AbstractFeed]: список распаршенных лент.
        """
        pass

class HabrParser(
    FeedParser[HabrFeed]
    ):
    """Класс парсинга для Habr"""

    def __init__(self, base_url: str):
        """
        Args:
            base_url: базовая ссылка на habr.
        """
        self.base_url = base_url
        self.feed_url = f"{base_url}/ru/articles"


    def parse(self) -> HabrFeed:
        """Метод для получения ленты сайта

        Returns:
            AbstractFeed: абстрактная лента страниц.
        """
        logger.info("Fetching feed...")
        try:
            result = requests.get(self.feed_url)

            feed = self._parse_raw_result(result.text)
        except (requests.exceptions.ConnectionError):
            raise InvalidUrlError("Неверно введён URL")

        return feed

    def parse_with_offset(self, offset: int, n_pages: int = 5) -> List[HabrFeed]:
        """Метод для парсинга нескольких страниц ленты с оффсетом

        Args:
            offset: смещение ленты.
            n_pages: количество страниц ленты для парсинга.

        Returns:
            List[AbstractFeed]: список распаршенных лент.
        """
        logger.info(f"Парсим {n_pages} со смещением {offset}")

        if offset == 0:
            raise ZeroOffsetError("Смещение не может быть нулевым!")

        try:
            feeds = []
            for i in range(offset, offset + n_pages):
                url = f"{self.feed_url}/page{i}"

                logger.info(f"URL: {url}")

                result = requests.get(url)

                feed = self._parse_raw_result(result.text)

                feeds.append(feed)

            logger.info(f"Получено {len(feeds)} фидов")

            return feeds
        except requests.exceptions.ConnectionError:
            raise InvalidUrlError("Введён неверный URL")


    def _parse_page(self, page_url: str) -> PageInfo:
        """Парсит сырую HTML страницу по ссылке

        Args:
            page_url: ссылка на страницу.

        Returns:
            PageInfo: информация о странице.
        """
        url = self.base_url + page_url

        logger.debug(f"Getting content and hub from {url}")

        try:

            page_request = requests.get(url).text
            soup = BeautifulSoup(page_request, "html.parser")
            
            content_div = soup.find("div", class_="tm-article-body")

            containers = soup.find_all("div", class_="tm-separated-list")

            for container in containers:
                title_span = container.find("span", class_="tm-separated-list__title")
                if title_span and "Хабы" in title_span.text:
                    hubs_list = container.find("ul", class_="tm-separated-list__list")

            hubs = hubs_list.find_all("li")
            first_hub = None

            for hub in hubs:
                if hub and not "Блог" in hub.text or \
                    not "Блог компании" in hub.text:
                    first_hub = hub.get_text()

            if not first_hub:
                logging.warning("На странице не найден первый хаб")
                logging.warning("Хабы: %s", hubs)

                first_hub = "unknown"

            if not content_div:
                raise EmptyBodyError("На странице нет содержания")

            first_hub = self._normalize_hub(first_hub)
            content = content_div.get_text(" ")

            info = PageInfo(
                content=content,
                hub=first_hub,
           )

            return info
        except requests.exceptions.ConnectionError:
            raise InvalidUrlError("Введён неверный URL")

    def _parse_raw_result(self, result: str) -> HabrFeed:
        """Парсинг сырого HTML фида

        Args:
            result: сырой HTML.

        Returns:
            HabrFeed: лента страниц.
        """

        soup = BeautifulSoup(result, "html.parser")
        link_tags = soup.find_all("a", class_="tm-title__link")

        if not link_tags:
            raise LinksNotFound("Не было найдено тегов с ссылками в ленте")
        
        pattern = re.compile("articles/([0-9]+)")

        pages = []
        for link_tag in link_tags:
            try:
                href: Optional[str] = link_tag["href"]
                if not href:
                    raise LinkTagError("В теге нет ссылки")
                match = re.search(pattern, href)

                if not match:
                    raise LinkTagError(f"В ссылке {href} не найден ID\nMatch: {match}")

                article_id = match.group(1)

                article_title = link_tag.text

                page_info = self._parse_page(href)

                page = Page(
                    id=article_id,
                    title=article_title,
                    **page_info.model_dump()
                )

                pages.append(page)

            except LinkTagError as err:
                logger.warning(f"Пропускаем статью из-за ошибки LinkTagError:\n{err}")
                continue

        return HabrFeed(pages=pages)

    def _normalize_hub(self, hub: str) -> str:
        """Приводит все хабы к нижнему регистру

        Args:
            hub: хаб, который нужно преобразовать.

        Returns:
            str: преобразованный хаб.
        """

        return hub.strip().lower()
