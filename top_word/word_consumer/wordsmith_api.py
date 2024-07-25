import os
import xml.etree.ElementTree as ET

import httpx
from top_word.common import configure_logger, with_retry

logger = configure_logger(__name__)
WORDSMITH_URL = os.getenv("WORDSMITH_URL")


@with_retry(exceptions=httpx.HTTPStatusError)
async def fetch_word() -> str:
    if WORDSMITH_URL is None:
        raise ValueError("WORDSMITH_URL environment variable is not set")

    async with httpx.AsyncClient() as client:
        xml_resp = await client.get(url=WORDSMITH_URL)
        xml_resp.raise_for_status()

    root = ET.fromstring(xml_resp.text)
    item = root.find(".//item")

    if item is None:
        raise ValueError("No <item> element found in XML response")

    title_element = item.find("title")

    if title_element is None:
        raise ValueError("No <title> element found in <item>")

    word_of_the_day = title_element.text

    if word_of_the_day is None:
        raise ValueError("No text found in <title> element")

    logger.info("word of the day is '%s'", word_of_the_day)
    return word_of_the_day
