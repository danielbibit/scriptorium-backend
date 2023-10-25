import logging
from typing import Annotated

import sqlalchemy
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
    mapped_column,
    sessionmaker,
)

from scriptorium.config import config

log = logging.getLogger(__name__)

engine = sqlalchemy.create_engine(config.DB_STRING_CONNECTION)
metadata = sqlalchemy.MetaData()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(MappedAsDataclass, DeclarativeBase):
    metadata = metadata
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
        log.debug("committing db")
    except Exception:
        log.debug("rolling back db")
        raise
    finally:
        log.debug("closing db")
        db.close()


intpk = Annotated[int, mapped_column(primary_key=True)]
