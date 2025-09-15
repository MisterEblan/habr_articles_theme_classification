import pytest

from src.predictor import AbstractPredictor, BaselinePredictor
from src.preprocess import BaselinePreprocessor
from src.data_models.predictions import Prediction
from src.config import app_config

def test_singleton(
    baseline_predictor: AbstractPredictor,
):
    assert baseline_predictor is BaselinePredictor(
        model_path=app_config.model_path,
        preprocessor=BaselinePreprocessor()
    )

@pytest.mark.asyncio
async def test_predict(
        article: str,
        baseline_predictor: AbstractPredictor
):
    prediction: Prediction = await baseline_predictor.predict(article)

    print(prediction)

    assert prediction, "Ожидалось не пустое предсказание"
    assert isinstance(prediction, Prediction), \
        "Ожидалось, что будет получен специальный класс"
