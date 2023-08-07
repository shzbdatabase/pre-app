from typing import Union

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from motor import motor_asyncio

from app.setting import Settings
from coin.model.currency_pair import CurrencyPair
from coin.model.resample import TradeResample

settings = Settings()
app = FastAPI()

db_url = f"mongodb://{settings.mongo_user}:{settings.mongo_password}@{settings.mongo_host}:{settings.mongo_port}"
client = motor_asyncio.AsyncIOMotorClient(db_url)
db = client.persistence


@app.get(
    "/exchange_rate/{base}/{quote}",
    response_description="exchange rate pair",
    response_model=CurrencyPair,
)
async def read_exchange_rate_pair(base: str, quote: str):
    if base.startswith("BTC-") and quote.startswith("BTC-"):
        base = base.replace("-", "/")
        quote = quote.replace("-", "/")
        stream_name = "exchange_rate:upbit:binance"
    else:
        stream_name = "exchange_rate:base"

    pair = await db[stream_name].find_one(
        {"b": base, "q": quote}, sort=[("t", -1)], projection={"_id": False}
    )
    if pair is None:
        raise HTTPException(status_code=404, detail=f"exchange pari ({base}/{quote}) not found")

    return JSONResponse(status_code=status.HTTP_200_OK, content=pair)


@app.get(
    "/stream/ticker",
    response_description="support stream list",
    response_model=list[str],
)
async def read_stream_ticker():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=[
            "binance:future:BTC-USDT:trade",
            "upbit:spot:BTC-KRW:trade",
            "binance:future:BCH-USDT:trade",
            "upbit:spot:BCH-KRW:trade",
            "binance:future:ETH-USDT:trade",
            "upbit:spot:ETH-KRW:trade",
            "binance:future:ETC-USDT:trade",
            "upbit:spot:ETC-KRW:trade",
            "binance:future:XRP-USDT:trade",
            "upbit:spot:XRP-KRW:trade",
            "binance:future:DOGE-USDT:trade",
            "upbit:spot:DOGE-KRW:trade",
            "binance:future:DOT-USDT:trade",
            "upbit:spot:DOT-KRW:trade",
            "binance:future:STX-USDT:trade",
            "upbit:spot:STX-KRW:trade",
        ],
    )


@app.get(
    "/ticker/{exchange}/{market}/{symbol}/{timeframe}",
    response_description="latest ticker",
    response_model=list[TradeResample],
)
async def read_tickers(
    exchange: str, market: str, symbol: str, timeframe: str, size: Union[int, None] = None
):
    if exchange not in ["binance", "upbit"]:
        raise HTTPException(status_code=400, detail=f"wrong argument")

    if market not in ["future", "spot"]:
        raise HTTPException(status_code=400, detail=f"wrong argument")

    if timeframe not in ["1s", "1h", "24h", "48h"]:
        raise HTTPException(status_code=400, detail=f"wrong argument")

    if size is None:
        size = 10
    elif size > 100:
        raise HTTPException(status_code=400, detail=f"wrong argument")

    stream_name = f"{exchange}:{market}:{symbol.replace('-', '/')}:trade:{timeframe}"

    ticker = (
        await db[stream_name]
        .find({}, sort=[("t", -1)], projection={"_id": False})
        .to_list(length=size)
    )
    if ticker is None:
        raise HTTPException(status_code=404, detail=f"ticker not found")

    return JSONResponse(status_code=status.HTTP_200_OK, content=ticker)
