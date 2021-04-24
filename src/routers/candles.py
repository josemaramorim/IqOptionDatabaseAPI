from typing import Dict, List

from fastapi import APIRouter

from src.database import master_session
from src.database.models import Candle
from src.schema import CandleOutput, PostCandleInput, PutCandleInput
from src.utils.miscellaneous import normalize_pairs

candles_router = APIRouter()


@candles_router.post("/candles", response_model=List[CandleOutput])
async def get_candles(body: PostCandleInput):
    pairs = normalize_pairs(body.pairs, body.otc)
    with master_session() as session:
        candles = Candle.get_all(
            session,
            Candle.from_.between(body.start_datetime.timestamp(), body.end_datetime.timestamp()),
            Candle.pair.in_(pairs),
            Candle.timeframe == body.timeframe,
        )

        return [candle.to_json() for candle in candles]


@candles_router.put("/candles")
async def put_candles(candles: List[PutCandleInput]) -> Dict[str, str]:
    # TODO: Fazer algum esquema para bloquear esse endpoint(decorador), usando o IP ou alguma autorização
    with master_session() as session:
        for candle in candles:
            session.merge(Candle.create_from_schema(candle))

    return {"message": "Total candles updated: %s" % len(candles)}
