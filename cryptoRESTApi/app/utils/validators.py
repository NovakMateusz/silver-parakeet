from typing import List

from app.utils.constans import CODE_NAME_MAPPING

__all__ = ['code_length_validator', 'known_codes_validator']


def code_length_validator(value: List[str]) -> str:
    if not len(value) == 1:
        raise ValueError('Incorrect amount of parameters passed in request')
    return value[0].upper()


def known_codes_validator(value: str) -> str:
    if not (value in CODE_NAME_MAPPING.keys() or value == 'ALL'):
        raise ValueError('COde %s not supported' % value)
    return value


