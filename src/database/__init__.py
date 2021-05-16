from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.settings import SQLALCHEMY_DB_URI
from src.utils.logger import logger

db = create_engine(SQLALCHEMY_DB_URI)


def master_session() -> Session:
    session = sessionmaker(db, autocommit=False, autoflush=False)()

    try:
        yield session
        session.commit()

    except Exception as e:
        logger.error("Error on database: %s" % " ".join(e.args))
        session.rollback()
        raise e

    finally:
        session.close()


def read_session() -> Session:
    session = sessionmaker(db, autocommit=False, autoflush=False)()

    try:
        yield session

    finally:
        session.close()
