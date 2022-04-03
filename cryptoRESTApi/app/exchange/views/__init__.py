from aiocache import SimpleMemoryCache
from pydantic import ValidationError
from sanic import json, Request

from app.exchange import exchange_blueprint
from app.exchange.models import ExchangeInputModel, ExchangeErrorResponseModel
from app.utils.errors import extract_message_from_error


@exchange_blueprint.route('/state')
async def currency_state_view(request: Request):
    try:
        input_model = ExchangeInputModel(**request.args)
    except ValidationError as error:
        response_model = ExchangeErrorResponseModel(endpoint=request.url,
                                                    message=extract_message_from_error(error),
                                                    status_code=400)
        return json(response_model.dict(), status=response_model.status_code)
    cache: SimpleMemoryCache = request.app.ctx.aiocache
    cached_value = cache.get(input_model.symbol)
    if cached_value:
      pass


