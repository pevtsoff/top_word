# Word of the day

This is a test assignment described in [task](./task.md)
Set of two microservices.

1. word_consumer - fetches the word of the day from wordsmith,
   generate GPT article for it and stores in redis. It used ChatGPT as  LLM model
2. api - fastapi based endpoint which fetches the article from redis and give it to the rest api clients

## Build and launch

```shell
1.Create a .env file from .env.template. Fill in the OPENAI_API_KEY variable with your key
2.docker compose build
3.docker compose up

```


## Run tests in docker compose

```shell
docker compose -f docker-compose-test up
```

## Local launch

```shell
1.pip install poetry
2.poetry install
3.Run 
api:
python top_word/main.py api
word-consumer:
python top_word/main.py word-consumer
```

## Run tests locally

```shell
pytest tests
```

## Request examples:

1. Get the word of the day

Typical scenario

```shell
Request:
curl http://0.0.0.0:8000/word_of_the_day/

Response:
{
   "header":"Ept: The Competent Ally",
   "body":"Ept, describing skillful and efficient behavior, contrasts with \"inept.\" For example, an ept programmer swiftly navigates code challenges. In a team project, an ept organizer ensures smooth coordination and timely result delivery. Skillfulness truly shines in every ept action."
}
```

In case there is any issue with word_consumer microservice

```
Request:
curl http://0.0.0.0:8000/word_of_the_day/


Response:
{
   "detail":{
      "errors":"No valid topic for the word of the day exists in redis now",
      "body":null,
      "status_code":404,
      "error_codes":null
   }
}

```

## watch all redis keys

```shell
redis-cli KEYS "*"
```
