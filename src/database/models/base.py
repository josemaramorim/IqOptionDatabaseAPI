import datetime as dt
from typing import Dict

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    def populate_object(self, **data: Dict) -> None:
        columns = self.__table__.columns.keys()
        for key, value in data.items():
            if key in columns:
                setattr(self, key, value)

    def to_dict(self) -> dict:
        return {col: getattr(self, col) for col in self.__mapper__.attrs.keys()}

    def to_json(self) -> dict:
        data = self.to_dict()

        for col, value in data.items():
            if isinstance(value, dt.datetime) or isinstance(value, dt.date):
                data[col] = value.isoformat()

            elif isinstance(value, list):
                data[col] = [obj.to_json() if isinstance(obj, BaseModel) else None for obj in value]

        return data

    def save(self, session: Session) -> None:
        session.add(self)

    def delete(self, session: Session) -> None:
        session.delete(self)
        session.commit()

    def merge(self, session: Session) -> None:
        session.merge(self)
