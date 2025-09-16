"""Роуты"""

from fastapi import APIRouter, Depends

from src.api.dependencies import baseline_predictor
from src.data_models.api import PredictionRequest, PredictionResponse
from src.predictor import BaselinePredictor

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/articles"
)

@router.post("/predict", response_model=PredictionResponse)
async def predict_hub(
        request: PredictionRequest,
        baseline_predictor: BaselinePredictor = Depends(baseline_predictor)
):
    """Предсказывает хаб статьи из PredictionRequest"""
    prediction = await baseline_predictor.predict(request.article)

    logger.info("Prediction: %s", prediction)

    return PredictionResponse(
        success=True,
        prediction=prediction
    )
