from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic
from ..data_models import Feed

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
