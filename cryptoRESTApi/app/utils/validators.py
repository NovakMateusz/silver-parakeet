from typing import List

from app.utils.constans import SYMBOL_NAME_MAPPING

__all__ = ['symbol_length_validator', 'known_symbols_validator']


def symbol_length_validator(value: List[str]) -> str:
    if not len(value) == 1:
        raise ValueError('Incorrect amount of parameters passed in request')
    return value[0].upper()


def known_symbols_validator(value: str) -> str:
    if not (value in SYMBOL_NAME_MAPPING.keys() or value == 'ALL'):
        raise ValueError('Symbol %s not supported' % value)
    return value


