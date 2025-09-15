from pydantic import BaseModel

from .predictions import Prediction

class PredictionRequest(BaseModel):
    """Запрос в сервис

    Attributes:
        article: статья, хаб которой нужно предсказать.
    """
    article: str

class PredictionResponse(BaseModel):
    """Ответ от сервиса

    Attributes:
        success: удачный ли ответ.
        prediction: предсказание модели.
    """
    success: bool
    prediction: Prediction
