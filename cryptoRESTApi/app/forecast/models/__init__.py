from typing import Dict, List

from pydantic import BaseModel

from app.models import InputModel

__all__ = ['PredictionErrorResponseModel', 'PredictionInputModel', 'PredictionResponseModel',
           'CumulativePredictionResponseModel']


class PredictionInputModel(InputModel):
    pass


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
