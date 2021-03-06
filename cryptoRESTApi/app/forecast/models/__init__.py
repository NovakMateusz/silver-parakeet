from typing import Dict, List

from pydantic import BaseModel

from app.models import InputModel, ErrorResponseModel

__all__ = ['PredictionErrorResponseModel', 'PredictionInputModel', 'PredictionResponseModel',
           'CumulativePredictionResponseModel', 'NextDayPredictionResponseModel']


class PredictionInputModel(InputModel):
    pass


class PredictionErrorResponseModel(ErrorResponseModel):
    pass


class PredictionResponseModel(BaseModel):
    name: str
    code: str
    prediction: Dict


class CumulativePredictionResponseModel(BaseModel):
    predictions: List[PredictionResponseModel]


class NextDayPredictionResponseModel(BaseModel):
    name: str
    code: str
    date: str
    prediction: float
