import logging
from logging.config import fileConfig
from alembic import context
from flask import current_app
from sqlalchemy import create_engine

config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.env")


def get_engine():
    """Creates an SQLAlchemy engine directly."""
    db_uri = current_app.config.get("SQLALCHEMY_DATABASE_URI")
    if not db_uri:
        logger.error("Database URI is not set in Flask config.")
        raise RuntimeError("Database URI is missing")
    return create_engine(db_uri)


def run_migrations():
    """Handles both online and offline migrations."""
    engine = get_engine()
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=None)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    context.configure(url=current_app.config["SQLALCHEMY_DATABASE_URI"])
    with context.begin_transaction():
        context.run_migrations()
else:
    run_migrations()
