from typing import List

from pydantic import BaseModel, validator

from app.utils.validators import known_codes_validator, code_length_validator


__all__ = ['InputModel', 'ErrorResponseModel']


class InputModel(BaseModel):
    code: List[str]

    # Validators
    _symbol_length_validator = validator('code', allow_reuse=True)(code_length_validator)
    _known_codes_validator = validator('code', allow_reuse=True)(known_codes_validator)


class ErrorResponseModel(BaseModel):
    endpoint: str
    message: str
    status_code: int
