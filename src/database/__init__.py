from contextlib import contextmanager

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.settings import SQLALCHEMY_DB_URI
from src.utils.logger import logger

db = create_engine(SQLALCHEMY_DB_URI)


@contextmanager
def master_session() -> Session:
    session = sessionmaker(db, autocommit=False, autoflush=False)()

    try:
        yield session
        session.commit()

    except Exception as e:
        logger.error("Error on database: %s" % " ".join(e.args))
        session.rollback()
        raise e


def create_all():
    meta = MetaData()
    meta.create_all(bind=db)
