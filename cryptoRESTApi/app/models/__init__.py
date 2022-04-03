from typing import List

from pydantic import BaseModel, validator

from app.utils.validators import known_symbols_validator, symbol_length_validator


__all__ = ['InputModel']


class InputModel(BaseModel):
    symbol: List[str]

    # Validators
    _symbol_length_validator = validator('symbol', allow_reuse=True)(symbol_length_validator)
    _known_symbols_validator = validator('symbol', allow_reuse=True)(known_symbols_validator)
