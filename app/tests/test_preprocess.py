import pytest

from src.preprocess import BaselinePreprocessor

@pytest.mark.asyncio
async def test_preprocess(
        article: str,
        baseline_preprocessor: BaselinePreprocessor
):

    preprocessed = await baseline_preprocessor.preprocess(article)

    assert preprocessed == article.lower(), \
        "Ожидалось, что текст будет приведён к нижнему регистру"
