from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import master_session, read_session
from src.database.models import Candle
from src.schema import CandleCreateModel, CandleGetModel, CandleModel
from src.utils.miscellaneous import normalize_pairs

candles_router = APIRouter()


@candles_router.post("/", response_model=List[CandleModel])
async def get_candles(body: CandleGetModel, session: Session = Depends(read_session)):
    pairs = normalize_pairs(body.pairs, body.otc)

    return Candle.get_all(
        session,
        Candle.from_.between(body.start_datetime.timestamp(), body.end_datetime.timestamp()),
        Candle.pair.in_(pairs),
        Candle.timeframe == body.timeframe,
    )


@candles_router.put("/")
async def put_candles(candles: List[CandleCreateModel], session: Session = Depends(master_session)):
    # TODO: Fazer algum esquema para bloquear esse endpoint(decorador), usando o IP ou alguma autorização
    for candle in candles:
        session.merge(Candle.create_from_schema(candle))
    session.commit()

    return {"message": "Total candles updated: %s" % len(candles)}
