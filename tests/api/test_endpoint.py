import json
from typing import AsyncGenerator
from unittest.mock import AsyncMock, Mock

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from top_word.api.api_service import ApiService
from top_word.api.fastapi_app import create_fastapi_app  # Adjust the import based on your app's location
from top_word.exceptions import NoValidTopicExists

pytestmark = pytest.mark.asyncio

TEST_TOPIC = {"header": "Test Header", "body": "Test Body"}

@pytest_asyncio.fixture
async def client(mocker: Mock) -> AsyncGenerator[AsyncClient, None]:
    mock_redis_client = AsyncMock()
    mock_redis_client.get.return_value = json.dumps(TEST_TOPIC).encode()
    mocker.patch("top_word.api.fastapi_app.connect_to_redis", return_value=mock_redis_client)

    app = create_fastapi_app()
    app.state.redis_client = mock_redis_client

    async with (LifespanManager(app) as manager, AsyncClient(app=manager.app, base_url="http://test") as client):
        yield client


@pytest_asyncio.fixture
async def client_no_valid_topic_exists_exception(mocker: Mock) -> AsyncGenerator[AsyncClient, None]:
    mock_redis_client = AsyncMock()
    mock_redis_client.get.return_value = json.dumps(TEST_TOPIC).encode()
    mocker.patch("top_word.api.fastapi_app.connect_to_redis", return_value=mock_redis_client)

    api_service_mock = AsyncMock()
    api_service_mock.get_article.side_effect = NoValidTopicExists(
        detail="No valid topic for the word of the day exists in redis now",
        status_code=404,
    )

    app = create_fastapi_app()
    app.state.redis_client = mock_redis_client
    app.dependency_overrides[ApiService] = lambda: api_service_mock

    async with (LifespanManager(app) as manager, AsyncClient(app=manager.app, base_url="http://test") as client):
        yield client


# positive tests
@pytest.mark.asyncio
async def test_get_word_of_the_day_success(client: AsyncClient) -> None:
    response = await client.get("/word_of_the_day/")

    assert response.status_code == 200
    assert response.json() == TEST_TOPIC


# negative tests
@pytest.mark.asyncio
async def test_get_word_of_the_day_success3(client: AsyncClient) -> None:
    response = await client.get("/non_existing_path/")

    assert response.status_code == 404
    assert response.json() == {"detail": {"body": None, "error_codes": None, "errors": "Not Found", "status_code": 404}}


@pytest.mark.asyncio
async def test_get_word_of_the_day_no_topic(client_no_valid_topic_exists_exception: AsyncClient) -> None:
    response = await client_no_valid_topic_exists_exception.get("/word_of_the_day/")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "body": None,
            "error_codes": None,
            "errors": "No valid topic for the word of the day exists in redis now",
            "status_code": 404,
        }
    }
