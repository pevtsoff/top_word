import asyncio
import os
import re

from dotenv import load_dotenv
from openai import AsyncOpenAI
from top_word.common import configure_logger, with_retry
from top_word.exceptions import InvalidTopicData
from top_word.models import TopicOfTheDay

load_dotenv()
openai_client = AsyncOpenAI()
logger = configure_logger(__name__)


OPENAI_MODEL_NAME = os.environ.get("OPENAI_MODEL_NAME", "gpt-4o")
OPENAI_MAX_TOKENS = int(os.environ.get("OPENAI_MAX_TOKENS", 300))
INSTRUCTIONS = """
You need to generate a topic with header and body for the single word or phrase of the day
which is given to you as the only input.The header should be no more 50 chars including spaces.
The body should be no more than 250 chars, including spaces!
The format of the output message shall be
Header: <Word of the day>

Body: <Unveil the word of the day meaning in some interesting situations>
"""

extract_pattern = re.compile(r"Header: (?P<Header>.*?)\n\nBody: (?P<Body>[\s\S]*)", re.IGNORECASE)
OPENAI_TIMEOUT = int(os.getenv("OPENAI_TIMEOUT", 60))


@with_retry(exceptions=Exception)
async def generate_topic(word: str) -> TopicOfTheDay:
    completion = await openai_client.chat.completions.create(
        model=OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": INSTRUCTIONS},
            {"role": "user", "content": word},
        ],
        stream=False,
        max_tokens=OPENAI_MAX_TOKENS,
        timeout=OPENAI_TIMEOUT,
    )

    return extract_data(str(completion.choices[0].message.content))


def extract_data(raw_message: str) -> TopicOfTheDay:
    match = extract_pattern.search(raw_message)

    if match:
        header = match.group("Header")
        body = match.group("Body")
        print(f"{body.__len__()=}")
        return TopicOfTheDay(header=header.strip(), body=body.strip())

    else:
        raise InvalidTopicData("Cant extract data from OpenAI Response")


if __name__ == "__main__":
    print(asyncio.run(generate_topic("coffee")))
