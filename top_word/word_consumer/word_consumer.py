import asyncio
import os
from datetime import datetime

from dotenv import load_dotenv
from top_word.common import configure_logger, flush_data_to_redis, repeat
from top_word.models import TopicOfTheDay, WordOfTheDay
from top_word.word_consumer.openai_api import generate_topic
from top_word.word_consumer.wordsmith_api import fetch_word

load_dotenv()
logger = configure_logger(__name__)


REDIS_WORD_KEY = os.getenv("REDIS_WORD_KEY", "top_word")
REDIS_TOPIC_KEY = os.getenv("REDIS_TOPIC_KEY", "top_article")
WORD_CHANGE_TIMEOUT: int = int(os.getenv("WORD_CHANGE_TIMEOUT", 86400))


async def store_word_article() -> None:
    word: str = await fetch_word()
    word_data: WordOfTheDay = WordOfTheDay(word=word, timestamp=datetime.now().isoformat())
    article: TopicOfTheDay = await generate_topic(word)

    await flush_data_to_redis(REDIS_WORD_KEY, word_data.json())
    await flush_data_to_redis(REDIS_TOPIC_KEY, article.json())


def word_consumer_main() -> None:
    """Runs the task periodically"""
    loop = asyncio.get_event_loop()
    loop.create_task(repeat(WORD_CHANGE_TIMEOUT, store_word_article))

    try:
        loop.run_forever()

    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == "__main__":
    word_consumer_main()
