from typing import Dict

from pydantic import BaseModel

from app.models import InputModel, ErrorResponseModel

__all__ = ['HistoricalDataInputModel', 'HistoricalDataErrorResponseModel', 'HistoricalDataResponseModel']


class HistoricalDataInputModel(InputModel):
    pass


class HistoricalDataErrorResponseModel(ErrorResponseModel):
    pass


class HistoricalDataResponseModel(BaseModel):
    name: str
    code: str
    history: Dict
