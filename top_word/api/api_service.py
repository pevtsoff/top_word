import json
import os

from fastapi import Request
from top_word.common.exceptions import NoValidTopicExists
from top_word.common.models import TopicOfTheDay

REDIS_TOPIC_KEY = os.getenv("REDIS_TOPIC_KEY", "top_article")


class ApiService:
    @staticmethod
    async def get_article(request: Request) -> TopicOfTheDay:
        redis_client = request.app.state.redis_client
        article_str = await redis_client.get(REDIS_TOPIC_KEY)

        if not article_str:
            raise NoValidTopicExists(
                detail="No valid topic for the word of the day exists in redis now",
                status_code=404,
            )


        article = TopicOfTheDay(**json.loads(article_str.decode()))
        return article
