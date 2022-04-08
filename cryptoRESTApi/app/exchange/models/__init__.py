from pydantic import BaseModel, validator

from app.models import InputModel, ErrorResponseModel
from app.utils.validators import known_codes_validator


class ExchangeInputModel(InputModel):
    pass


class ExchangeErrorResponseModel(ErrorResponseModel):
    pass


class ExchangeResponseModel(BaseModel):
    name: str
    code: str
    exchange_rate: float


class ExternalServiceInputModel(BaseModel):
    code: str
    name: str
    exchange_rate: float

    # Validators
    _known_code_validator = validator('code', allow_reuse=True)(known_codes_validator)
