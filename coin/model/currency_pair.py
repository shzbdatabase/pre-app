from pydantic import BaseModel


class CurrencyPair(BaseModel):
    # base
    b: str
    # quote
    q: str
    # value
    v: float
    # timestamp
    t: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "b": "KRW",
                "q": "USDT",
                "v": 1310.0628327821566,
                "t": 1690961814924,
            }
        }
    }
