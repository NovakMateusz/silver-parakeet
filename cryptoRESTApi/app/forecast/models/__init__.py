from typing import Dict, List

from pydantic import BaseModel, validator

from app.utils.validators import known_symbols_validator, symbol_length_validator

__all__ = ['PredictionErrorResponseModel', 'PredictionInputModel', 'PredictionResponseModel',
           'CumulativePredictionResponseModel']


class PredictionInputModel(BaseModel):
    symbol: List[str]

    # validators
    _symbol_length_validator = validator('symbol', allow_reuse=True)(symbol_length_validator)
    _known_symbols_validator = validator('symbol', allow_reuse=True)(known_symbols_validator)


class PredictionErrorResponseModel(BaseModel):
    endpoint: str
    message: str
    status_code: int


class PredictionResponseModel(BaseModel):
    name: str
    symbol: str
    prediction: Dict


class CumulativePredictionResponseModel(BaseModel):
    predictions: List[PredictionResponseModel]
