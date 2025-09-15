from enum import Enum

class Prediction(Enum):
    """Предсказание модели - хабы, на которых она обучена"""
    AI                = "artificial_intelligence"
    MATHS             = "maths"
    INFOSEC           = "infosecurity"
    IT_INFRASTRUCTURE = "it-infrastructure"
    HR_MANAGEMENT     = "hr_management"
