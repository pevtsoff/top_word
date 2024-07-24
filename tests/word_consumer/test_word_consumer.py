from typing import Any, Generator
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from top_word.word_consumer.wordsmith_api import fetch_word

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_httpx_get() -> Generator[AsyncMock, None, None]:
    with patch("httpx.AsyncClient.get") as mock_get:
        yield mock_get


async def test_fetch_word_success(mock_httpx_get: AsyncMock) -> None:
    mock_response = AsyncMock()
    mock_response.text = """
        <rss>
            <channel>
                <item>
                    <title>ExampleWord</title>
                </item>
            </channel>
        </rss>
    """
    mock_response.raise_for_status = AsyncMock()
    mock_httpx_get.return_value = mock_response

    word = await fetch_word()
    assert word == "ExampleWord"


async def test_fetch_word_missing_item(mock_httpx_get: AsyncMock) -> None:
    mock_response = AsyncMock()
    mock_response.text = """
        <rss>
            <channel>
                <title>ExampleWord</title>
            </channel>
        </rss>
    """
    mock_response.raise_for_status = AsyncMock()
    mock_httpx_get.return_value = mock_response

    with pytest.raises(ValueError, match="No <item> element found in XML response"):
        await fetch_word()


async def test_fetch_word_missing_title(mock_httpx_get: AsyncMock) -> None:
    mock_response = AsyncMock()
    mock_response.text = """
        <rss>
            <channel>
                <item>
                    <description>Example Description</description>
                </item>
            </channel>
        </rss>
    """
    mock_response.raise_for_status = AsyncMock()
    mock_httpx_get.return_value = mock_response

    with pytest.raises(ValueError, match="No <title> element found in <item>"):
        await fetch_word()


async def test_fetch_word_no_word_in_title(mock_httpx_get: AsyncMock) -> None:
    mock_response = AsyncMock()
    mock_response.text = """
        <rss>
            <channel>
                <item>
                    <title></title>
                </item>
            </channel>
        </rss>
    """
    mock_response.raise_for_status = AsyncMock()
    mock_httpx_get.return_value = mock_response

    with pytest.raises(ValueError, match="No text found in <title> element"):
        await fetch_word()


@pytest.mark.parametrize("attempts", [1, 2, 3])
async def test_fetch_word_with_retry(mock_httpx_get: AsyncMock, attempts: int) -> None:
    # Mock to fail for `attempts-1` times and succeed on the last attempt
    counter = {"value": 0}

    def side_effect(*args: Any, **kwargs: Any) -> Any:
        if counter["value"] < attempts - 1:
            counter["value"] += 1
            raise httpx.HTTPStatusError("HTTP error", request=AsyncMock(), response=AsyncMock())
        return mock_response

    mock_response = AsyncMock()
    mock_response.text = """
        <rss>
            <channel>
                <item>
                    <title>ExampleWord</title>
                </item>
            </channel>
        </rss>
    """
    mock_response.raise_for_status = AsyncMock()

    mock_httpx_get.side_effect = side_effect

    word = await fetch_word()
    assert word == "ExampleWord"
