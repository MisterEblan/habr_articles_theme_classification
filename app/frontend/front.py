"""Небольшой фронтенд"""

from typing import Dict, Union
from requests.exceptions import HTTPError
import streamlit as st
import requests

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

def request_classification(article: str) -> Dict[str, Union[bool, str]]:
    """Делает запрос в Hub Prediction API

    Args:
        article: статья для классификации.

    Returns:
        Dict[str, Union[bool, str]]:
            словарь-ответ от API.
    """
    response = requests.post(
        "http://backend:8000/api/v1/articles/predict",
        json={
            "article": article
        },
        verify=False,
        timeout=20
    )
    response.raise_for_status()

    return response.json()

st.title("Классификатор статей по хабам Habr")
st.write("В данный момент можно классифицировать хабы:")
st.write("1. artificial_intelligence")
st.write("2. maths")
st.write("3. it-infrastructure")
st.write("4. hr_management")
st.write("5. infosecurity")

with st.form("Классифицировать статью"):
    article = st.text_area(
        "Содержание статьи",
        height=350
    )
    
    submit = st.form_submit_button("Классифицировать статью")

if submit:
    try:
        prediction = request_classification(article)

        st.write("Скорее всего, статья относится к ")
        st.success(prediction["prediction"])

    except HTTPError as err:

        logger.error("HTTPError: %s", err)

        st.error("Что-то пошло не так при запросе!")

    except Exception as err:
        
        logger.error("ERROR: %s", err)

        st.error("Что-то пошло не так!")
