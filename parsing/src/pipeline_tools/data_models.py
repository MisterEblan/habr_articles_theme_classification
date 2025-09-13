from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel

class Page(BaseModel):
    """Представляет собой абстрактную страницу

    Attributes:
        id: идентификатор страницы.
        title: заголовок страницы.
        content: содержание страницы.
        hub: тема страницы.
    """
    id: Union[int, str]
    title: str
    content: str
    hub: str

class PageInfo(BaseModel):
    """Представляет собой необходимую информацию о странице

    Attributes:
        content: содержание страницы.
        hub: тема страницы.
    """
    content: str
    hub: str

class Feed(BaseModel):
    """Представляет ленту из страниц

    Attributes:
        pages: страницы в ленте.
    """
    pages: List[Page]


class HabrFeed(Feed):
    """Представляет ленту Habr"""
    pass
