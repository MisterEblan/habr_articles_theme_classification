from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="Hub Predictor API",
    description="API для предсказания хаба статьи."
)

app.include_router(router)
