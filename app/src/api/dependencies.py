"""Зависимости FastAPI приложения"""

from ..preprocess import BaselinePreprocessor
from ..predictor import BaselinePredictor
from ..config import app_config
from functools import lru_cache

@lru_cache
def baseline_predictor() -> BaselinePredictor:
    return BaselinePredictor(
        model_path=app_config.model_path,
        preprocessor=BaselinePreprocessor()
    )
