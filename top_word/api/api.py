import logging

from fastapi import APIRouter, Depends, Request
from top_word.api.api_service import ApiService
from top_word.common.models import TopicOfTheDay

router = APIRouter(prefix="/word_of_the_day", tags=["word_of_the_day"])
logger = logging.getLogger("api")


@router.get("/", response_model=TopicOfTheDay)
async def get_word_of_the_day(request: Request, service: ApiService = Depends()) -> TopicOfTheDay:
    return await service.get_article(request)
