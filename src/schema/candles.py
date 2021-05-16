from datetime import datetime
from typing import List

from pydantic import BaseModel, validator
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class BaseCandle(BaseModel):
    id: int
    at: int
    from_: int
    to: int
    open: float
    close: float
    min: float
    max: float
    pair: str
    timeframe: int


class CandleGetModel(BaseModel):
    start_datetime: datetime
    end_datetime: datetime
    pairs: List[str]
    timeframe: int
    otc: bool = False

    @validator("timeframe")
    def validate_timeframe(timeframe: int) -> int:
        if timeframe not in [1, 5, 15]:
            raise HTTPException(HTTP_400_BAD_REQUEST, {"message": "Invalide value for timeframe (must be 1, 5 or 15)"})

        return timeframe


class CandleCreateModel(BaseCandle):
    pass


class CandleModel(BaseCandle):
    class Config:
        orm_mode = True

    @classmethod
    def alias_generator(cls, string: str) -> str:
        return string.strip("_")
