from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel

class Page(BaseModel):
    id: Union[int, str]
    title: str
    content: str
    hub: str

class PageInfo(BaseModel):
    content: str
    hub: str

class Feed(BaseModel):
    pages: List[Page]


class HabrFeed(Feed):
    pass
