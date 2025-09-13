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
        """Метод для получения ленты сайта"""

        pass

    @abstractmethod
    def parse_with_offset(self, offset: int, n_pages: int = 5) -> List[AbstractFeed]:
        """Метод для парсинга нескольких страниц ленты с оффсетом"""
        pass

class HabrParser(
    FeedParser[HabrFeed]
    ):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.feed_url = f"{base_url}/ru/articles"


    def parse(self) -> HabrFeed:
        logger.info("Fetching feed...")
        try:
            result = requests.get(self.feed_url)

            feed = self._parse_raw_result(result.text)
        except (requests.exceptions.ConnectionError):
            raise InvalidUrlError("Неверно введён URL")

        return feed

    def parse_with_offset(self, offset: int, n_pages: int = 5) -> List[HabrFeed]:
        logger.info(f"Парсим {n_pages} со смещением {offset}")

        if offset == 0:
            raise ZeroOffsetError("Смещение не может быть нулевым!")

        try:
            feeds = []
            for i in range(offset, n_pages):
                url = f"{self.feed_url}/page{i}"

                logger.debug(f"URL: {url}")

                result = requests.get(url)

                feed = self._parse_raw_result(result.text)

                feeds.append(feed)

            logger.info(f"Получено {len(feeds)} фидов")

            return feeds
        except requests.exceptions.ConnectionError:
            raise InvalidUrlError("Введён неверный URL")


    def _parse_page(self, page_url: str) -> PageInfo:
        url = self.base_url + page_url

        logger.debug(f"Getting content and hub from {url}")

        try:

            page_request = requests.get(url).text
            soup = BeautifulSoup(page_request, "html.parser")
            
            content_div = soup.find("div", class_="tm-article-body")
            hubs_list = soup.find("ul", class_="tm-separated-list__list")
            first_hub = hubs_list.find("li").get_text()

            if not first_hub:
                raise HubNotFound("На странице не найден первый хаб")

            if not content_div:
                raise EmptyBodyError("На странице нет содержания")

            content = content_div.get_text(" ")

            info = PageInfo(
                content=content,
                hub=first_hub,
           )

            return info
        except requests.exceptions.ConnectionError:
            raise InvalidUrlError("Введён неверный URL")

    def _parse_raw_result(self, result: str) -> HabrFeed:

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
