from typing import Any, Generator
from unittest.mock import AsyncMock, patch

import pytest
from top_word.exceptions import InvalidTopicData
from top_word.word_consumer.openai_api import extract_data, generate_topic

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_openai_client() -> Generator[Any, None, None]:
    with patch("top_word.word_consumer.openai_api.openai_client") as mock_client:
        yield mock_client


class MockChoice:
    def __init__(self, content: str) -> None:
        self.message = AsyncMock()
        self.message.content = content


@pytest.fixture
def valid_openai_response() -> MockChoice:
    return MockChoice("Header: Coffee\n\nBody: Coffee is a brewed drink prepared from roasted coffee beans.")


@pytest.fixture
def invalid_openai_response() -> MockChoice:
    return MockChoice("Invalid response format")


async def test_generate_topic_success(mock_openai_client: AsyncMock, valid_openai_response: AsyncMock) -> None:
    mock_openai_client.chat.completions.create = AsyncMock(return_value=AsyncMock(choices=[valid_openai_response]))

    word = "coffee"
    result = await generate_topic(word)
    assert result.header == "Coffee"
    assert result.body == "Coffee is a brewed drink prepared from roasted coffee beans."


def test_extract_data_success() -> None:
    raw_message = "Header: Coffee\n\nBody: Coffee is a brewed drink prepared from roasted coffee beans."
    result = extract_data(raw_message)
    assert result.header == "Coffee"
    assert result.body == "Coffee is a brewed drink prepared from roasted coffee beans."


# negative tests
async def test_generate_topic_exception(mock_openai_client: AsyncMock) -> None:
    mock_openai_client.chat.completions.create = AsyncMock(side_effect=Exception("OpenAI error"))

    word = "coffee"
    with pytest.raises(Exception, match="OpenAI error"):
        await generate_topic(word)


def test_extract_data_invalid_format() -> None:
    raw_message = "Invalid response format"
    with pytest.raises(InvalidTopicData):
        extract_data(raw_message)
