import joblib
import asyncio

from abc import ABC, abstractmethod, abstractproperty
from sklearn.pipeline import Pipeline

from .data_models.predictions import Prediction
from .preprocess import AbstractPreprocessor, BaselinePreprocessor
from .helpers import Singleton

class AbstractPredictor(ABC):
    """Абстрактный класс предсказателя темы"""

    @abstractmethod
    async def predict(self, article: str) -> Prediction:
        """Предсказывает хаб статьи

        Args:
            article: текст статьи, хаб
                которой нужно предсказать.

        Returns:
            Prediction: предсказанный хаб.
        """
        pass

class BaselinePredictor(
    AbstractPredictor,
    Singleton
):
    """Предиктор, использующий TF-IDF + LogisticRegression"""

    def __init__(
            self,
            model_path: str,
            preprocessor: BaselinePreprocessor
    ):
        """
        Args:
            model_path: путь до локальной модели.
        """
        self.model: Pipeline = joblib.load(model_path)
        self.preprocessor = preprocessor

        if not self.model:
            raise ValueError("Модель не была загружена")

    async def predict(self, article: str) -> Prediction:
        preprocessed_article = await self.preprocessor.preprocess(
            article
        )
        predictions = await asyncio.to_thread(
            self.model.predict, [preprocessed_article]
        )

        return Prediction(predictions[0])
