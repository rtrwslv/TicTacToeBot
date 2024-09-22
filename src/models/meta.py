"""Module for meta."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from config.db import engine


NAMING_CONVENTION = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}


DEFAULT_SCHEMA = 'tictactoe'

metadata = MetaData(naming_convention=NAMING_CONVENTION, schema=DEFAULT_SCHEMA)
Base = declarative_base(metadata=metadata)


async def create_db() -> None:
    """
    Create the database tables based on the defined SQLAlchemy models.

    Returns:
        None: This function does not return a value.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
