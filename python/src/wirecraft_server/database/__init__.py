from pathlib import Path
from typing import Any

from alembic import context as alembic_context
from alembic.config import Config
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory
from sqlalchemy import Connection
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel

from ..context import ctx
from .models import Cable as Cable, Device as Device, LevelState as LevelState
from .session import async_session as async_session


async def init_db(engine: AsyncEngine):
    """
    Init the database by running all the migrations.
    In a normal scenario, we should use the `alembic upgrade head` command to apply all migrations.
    However, I prefer the migration to be run automatically when the server starts, so we can ensure that the database is always up to date.
    In a sync environment, we would use `command.upgrade(config, "head")` to apply the migrations.
    But in an async environment, because the loop already exists at this point, we would need to use asyncio.create_task in env.py.

    I don't want to use this because we should keep a reference to the task and wait until it is finished, but we can get any value from `command.upgrade`.
    Instead, we re-implement the migration logic, and directly use run_sync to apply the migration (because Alembic doesn't support asynchronous).
    """

    config = Config()
    config.set_main_option("sqlalchemy.url", str(engine.url))
    path = Path(__file__).parent / "migrations"
    config.set_main_option("script_location", path.as_posix())

    script = ScriptDirectory.from_config(config)

    def upgrade(rev: Any, context: Any):
        return script._upgrade_revs("head", rev)  # pyright: ignore[reportPrivateUsage]

    def do_run_migrations(connection: Connection) -> None:
        alembic_context.configure(connection=connection, target_metadata=SQLModel.metadata)

        with alembic_context.begin_transaction():
            alembic_context.run_migrations()

    with EnvironmentContext(
        config,
        script,
        fn=upgrade,
        as_sql=False,
        starting_rev=None,
        destination_rev="head",
        tag=None,
    ):
        async with engine.connect() as conn:
            if ctx.reset_database:
                raise RuntimeError(
                    "Resetting the database implies more logic that is not implemented yet. Please delete manually the database files."
                )
                # await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(do_run_migrations)
