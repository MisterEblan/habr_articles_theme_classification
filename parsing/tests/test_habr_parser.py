from requests.exceptions import InvalidURL
from src.pipeline_tools.data_models import HabrFeed, Page
from src.pipeline_tools.parsers import FeedParser
from src.pipeline_tools.errors import InvalidUrlError, ZeroOffsetError 

import pytest

def test_fetch_feed(
        habr_parser: FeedParser,
        caplog
):
    with caplog.at_level("DEBUG"):
        feed = habr_parser.parse()

        
        assert feed, "Пришла пустая лента"
        assert isinstance(feed, HabrFeed), f"Ожидался специальный класс, пришёл {type(feed)}"
        assert all(isinstance(page, Page) for page in feed.pages), "Все статьи должны быть представлены классом Page"

def test_nonvalid_url(
        habr_parser: FeedParser
):
    habr_parser.base_url = "https://thisurldoesntexists.com"

    with pytest.raises(InvalidUrlError):
        feed = habr_parser.parse()

# def test_5_feeds(
#     habr_parser: FeedParser,
#     caplog
# ):
#
#     with caplog.at_level("DEBUG"):
#         feeds_1 = habr_parser.parse_with_offset(1)
#         feeds_2 = habr_parser.parse_with_offset(5)
#
#         assert all(
#             feed_1 != feed_2
#             for feed_1 in feeds_1
#             for feed_2 in feeds_2
#         )

def test_0_offset(
        habr_parser: FeedParser
):
    with pytest.raises(ZeroOffsetError):
        habr_parser.parse_with_offset(0)
