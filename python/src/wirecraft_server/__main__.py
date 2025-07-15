from typing import Literal

import click

from wirecraft_server._logger import init_logger
from wirecraft_server.context import ctx
from wirecraft_server.server import Server


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
    help="Set the database path (a file for SQLite, an url for PostgreSQL).",
    type=str,
)
@click.option(
    "--database-type",
    "-T",
    "database_type",
    default="sqlite",
    envvar="DATABASE_TYPE",
    help="Set the database type.",
    type=click.Choice(["sqlite", "postgresql"], case_sensitive=False),
)
@click.option(
    "--reset-database",
    "-R",
    "reset_database",
    default=False,
    envvar="RESET_DATABASE",
    help="Reset the database.",
    type=bool,
    is_flag=True,
    show_default=True,
)
def main(
    debug_options: list[str],
    log_level: str,
    bind: str,
    database: str,
    database_type: Literal["sqlite", "postgresql"],
    reset_database: bool = False,
) -> None:
    ctx.set(
        debug_options=debug_options,
        bind=bind,
        database=database,
        database_type=database_type,
        reset_database=reset_database,
    )
    init_logger(log_level)

    server = Server()
    server.start()


if __name__ == "__main__":
    main()
