from datetime import date, datetime, time
from typing import List, Type

from sqlalchemy import Column, Index
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.sqltypes import BigInteger, Float, Integer, String

from src.database.models import BaseModel
from src.schema.candles import PostCandleInput

TCandle = Type["Candle"]


class Candle(BaseModel):
    __tablename__ = "candles"
    candle_id = Column("candle_id", String(36), primary_key=True)
    id = Column("id", Integer)
    at = Column("at", BigInteger)
    from_ = Column("from_", BigInteger)
    to = Column("to", BigInteger)
    open = Column("open", Float)
    close = Column("close", Float)
    min = Column("min", Float)
    max = Column("max", Float)
    pair = Column("pair", String(10))
    timeframe = Column("timeframe", Integer, index=True)

    __table_args__ = (
        Index("ix_pair_timeframe", "pair", "timeframe"),
        Index("ix_pair_timeframe_to", "pair", "timeframe", "to"),
        Index("ix_pair_timeframe_at", "pair", "timeframe", "at"),
    )

    @property
    def hour(self) -> time:
        return datetime.fromtimestamp(self.from_).time().isoformat()

    @property
    def date(self) -> date:
        return datetime.fromtimestamp(self.from_).date().isoformat()

    @property
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(self.from_)

    @property
    def is_otc(self) -> bool:
        if "-OTC" in self.pair:
            return True

        return False

    @staticmethod
    def create(
        timeframe: int,
        pair: str,
        id: int,
        from_: int,
        at: int,
        to: int,
        open: float,
        close: float,
        min: float,
        max: float,
    ) -> TCandle:
        return Candle(
            candle_id=f"{timeframe}-{pair}-{id}",
            id=id,
            from_=from_,
            at=at,
            to=to,
            open=open,
            close=close,
            min=min,
            max=max,
            timeframe=timeframe,
            pair=pair,
        )

    @staticmethod
    def create_from_schema(schema: PostCandleInput) -> TCandle:
        return Candle(
            candle_id=f"{schema.timeframe}-{schema.pair}-{schema.id}",
            timeframe=schema.timeframe,
            pair=schema.pair,
            id=schema.id,
            from_=schema.from_,
            at=schema.at,
            to=schema.to,
            open=schema.open,
            close=schema.close,
            min=schema.min,
            max=schema.max,
        )

    @staticmethod
    def get(session: Session, *args, **kwargs) -> TCandle:
        return session.query(Candle).filter(*args).filter_by(**kwargs).first()

    @staticmethod
    def get_all(session: Session, *args, **kwargs) -> List[TCandle]:
        return session.query(Candle).filter(*args).filter_by(**kwargs).order_by(Candle.from_.desc()).all()
