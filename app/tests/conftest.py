import pytest

from src.predictor import AbstractPredictor, BaselinePredictor
from src.config import app_config
from src.preprocess import BaselinePreprocessor

@pytest.fixture(scope="session")
def article() -> str:
    with open("tests/data/article.txt", "r", encoding="utf-8") as f:
        content = f.read()

    return content

@pytest.fixture(scope="session")
def baseline_predictor() -> AbstractPredictor:
    return BaselinePredictor(
        model_path=app_config.model_path,
        preprocessor=BaselinePreprocessor()
    )

@pytest.fixture(scope="session")
def baseline_preprocessor() -> BaselinePreprocessor:
    return BaselinePreprocessor()
