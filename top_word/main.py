import click
from top_word.api.fastapi_app import start_rest_api
from top_word.word_consumer.word_consumer import word_consumer_main


@click.group()
def cli() -> None:
    pass


@cli.command()
def word_consumer() -> None:
    word_consumer_main()


@cli.command()
def api() -> None:
    start_rest_api()


if __name__ == "__main__":
    cli()
