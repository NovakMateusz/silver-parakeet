from urllib.parse import urlencode, urljoin

from aiocache import SimpleMemoryCache
from aiohttp import ClientSession
from pydantic import ValidationError
from sanic import json, Request
from sanic.log import logger

from app.exchange import exchange_blueprint
from app.exchange.models import ExchangeInputModel, ExchangeErrorResponseModel, ExternalServiceInputModel
from app.utils.constans import ExternalServiceResponseFieldsName
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
    logger.info("[Exchange] receive new request, checking %s code" % input_model.code)
    cached_value = await cache.get(input_model.code)
    if cached_value:
        logger.info("[Exchange] using cached value for %s" % input_model.code)
        return json(cached_value.dict())

    aiohttp_session: ClientSession = request.app.ctx.aiohttp_session
    parameters = {'function': 'CURRENCY_EXCHANGE_RATE',
                  'from_currency': input_model.code,
                  'to_currency': 'USD',
                  'apikey': request.app.config.EXTERNAL_RESOURCES_KEY}

    logger.info("[Exchange] No cache value for %s, sending new request to external resources" % input_model.code)
    async with aiohttp_session.get(url=request.app.config.EXTERNAL_RESOURCES_URL, params=parameters) as response:
        if response.status == 200:
            json_response = await response.json()
            json_response = json_response['Realtime Currency Exchange Rate']
            external_service_input_model = ExternalServiceInputModel(
                code=json_response[ExternalServiceResponseFieldsName.from_currency_code.value],
                name=json_response[ExternalServiceResponseFieldsName.from_currency_name.value],
                exchange_rate=json_response[ExternalServiceResponseFieldsName.exchange_rate.value])

            logger.info("[Exchange] Caching new value for %s" % input_model.code)
            await cache.set(input_model.code, external_service_input_model)
            return json(external_service_input_model.dict())


# TO DO: Error handling for currency_state_view
