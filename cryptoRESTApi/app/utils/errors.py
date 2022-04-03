from pydantic import ValidationError


def extract_message_from_error(error: ValidationError) -> str:
    return error.errors()[0]['msg']
