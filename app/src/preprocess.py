from abc import ABC, abstractmethod

class AbstractPreprocessor(ABC):
    """Абстрактный класс для препроцессора данных"""

    @abstractmethod
    async def preprocess(self, article: str) -> str:
        """Предобрабатывает текст статьи для определённой модели

        Args:
            article: текст статьи

        Returns:
            str: преобразованный текст статьи.
        """
        pass

class BaselinePreprocessor(AbstractPreprocessor):
    """Препроцессор для Baseline-модели"""

    async def preprocess(self, article: str) -> str:
        """Приводит текст к нижнему регистру

        Args:
            article: текст статьи

        Returns:
            str: преобразованный текст статьи.
        """
        return article.lower()
