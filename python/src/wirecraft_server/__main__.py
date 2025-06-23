from pathlib import Path

import click

from wirecraft_server._logger import init_logger
from wirecraft_server.context import ctx
from wirecraft_server.server import Server


def init_server():
    server = Server()
    return server


@click.command()
@click.option(
    "--debug", "-d", "debug_options", multiple=True, default=[], envvar="DEBUG", help="Enable debug mode options."
)
@click.option("--log-level", "-l", "log_level", default="INFO", envvar="LOG_LEVEL", help="Set the log level.")
@click.option("--bind", "-b", "bind", default="localhost", envvar="BIND", help="Set the bind interface.")
@click.option(
    "--database",
    "-D",
    "database",
    default="database.db",
    envvar="DATABASE",
    help="Set the database file.",
    type=click.Path(file_okay=True, dir_okay=False, writable=True, resolve_path=True),
)
def main(debug_options: list[str], log_level: str, bind: str, database: str):
    ctx.set(debug_options=debug_options, bind=bind, database=Path(database))
    init_logger(log_level)

    server = init_server()
    server.start()


if __name__ == "__main__":
    main()
