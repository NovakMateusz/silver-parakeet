from pydantic import BaseModel

from app.models import InputModel


class ExchangeInputModel(InputModel):
    pass


class ExchangeErrorResponseModel(BaseModel):
    endpoint: str
    message: str
    status_code: int


class ExchangeResponseModel(BaseModel):
    name: str
    symbol: str
    exchange_rate: float

