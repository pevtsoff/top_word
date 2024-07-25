import json
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import Request
from top_word.api.api_service import ApiService
from top_word.common.exceptions import NoValidTopicExists

pytestmark = pytest.mark.asyncio


async def test_get_word_of_the_day_success(mocker: Mock) -> None:
    request = mocker.MagicMock(Request)
    request.app.state.redis_client = AsyncMock()
    request.app.state.redis_client.get.return_value = json.dumps(
        {"header": "Test Header", "body": "Test Body"}
    ).encode()

    service = ApiService()
    article = await service.get_article(request)

    assert article.header == "Test Header"
    assert article.body == "Test Body"


async def test_get_word_of_the_day_failure(mocker: Mock) -> None:
    request = mocker.MagicMock(Request)
    request.app.state.redis_client = AsyncMock()
    request.app.state.redis_client.get.return_value = None

    service = ApiService()

    with pytest.raises(NoValidTopicExists):
        await service.get_article(request)

