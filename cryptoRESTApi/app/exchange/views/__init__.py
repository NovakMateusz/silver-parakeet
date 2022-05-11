from asyncio import TimeoutError, CancelledError

from aiocache import SimpleMemoryCache
from aiohttp import ClientSession, ClientError, ClientResponseError
from pydantic import ValidationError
from sanic import json, Request
from sanic.log import logger

from app.exchange import exchange_blueprint
from app.exchange.models import ExchangeInputModel, ExchangeErrorResponseModel, ExternalServiceInputModel
from app.utils.auth import protected
from app.utils.constans import ExternalServiceResponseFieldsName
from app.utils.errors import extract_message_from_error


@exchange_blueprint.route('/state')
@protected
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
    try:
        async with aiohttp_session.get(url=request.app.config.EXTERNAL_RESOURCES_URL, params=parameters) as response:
            if response.status == 200:
                json_response = await response.json()
                logger.info(
                    "[Exchange] Response for %s code: %s" % (input_model.code, json_response))
                try:
                    json_response = json_response[ExternalServiceResponseFieldsName.main_key.value]
                except KeyError:
                    logger.error("[Exchange] KeyError: %s. Exceeded number of request to external REST API",
                                 str(ExternalServiceResponseFieldsName.main_key.value),)
                    response_model = ExchangeErrorResponseModel(endpoint=request.url,
                                                                message="Service Unavailable",
                                                                status_code=503)
                    return json(response_model.dict(), status=response_model.status_code)

                name = json_response[ExternalServiceResponseFieldsName.from_currency_name.value]
                code = json_response[ExternalServiceResponseFieldsName.from_currency_code.value]
                exchange_rate = json_response[ExternalServiceResponseFieldsName.exchange_rate.value]
                if name:
                    external_service_input_model = ExternalServiceInputModel(
                        code=code,
                        name=name,
                        exchange_rate=exchange_rate)
                else:
                    external_service_input_model = ExternalServiceInputModel(
                        code=code,
                        name=code,
                        exchange_rate=exchange_rate)

                logger.info("[Exchange] Caching new value for %s" % input_model.code)
                await cache.set(input_model.code, external_service_input_model)
            else:
                response_text = await response.text()
                logger.error("[Exchange] incorrect status code %d, response from the service %s" % response.status,
                             response_text)
                response_model = ExchangeErrorResponseModel(endpoint=request.url,
                                                            message="Internal Server Error",
                                                            status_code=500)
                return json(response_model.dict(), status=response_model.status_code)
    except TimeoutError as timeout_error:
        logger.error("[Exchange] TimeoutError: %s", str(timeout_error))
        response_model = ExchangeErrorResponseModel(endpoint=request.url,
                                                    message="Internal Server Error",
                                                    status_code=500)
        return json(response_model.dict(), status=response_model.status_code)
    except CancelledError as cancelled_error:
        logger.error("[Exchange] CancelledError: %s", str(cancelled_error))
        response_model = ExchangeErrorResponseModel(endpoint=request.url,
                                                    message="Internal Server Error",
                                                    status_code=500)
        return json(response_model.dict(), status=response_model.status_code)
    except ClientResponseError as client_response_error:
        logger.error("[Exchange] ClientResponseError: %s", str(client_response_error))
        response_model = ExchangeErrorResponseModel(endpoint=request.url,
                                                    message="Internal Server Error",
                                                    status_code=500)
        return json(response_model.dict(), status=response_model.status_code)
    except ClientError as client_error:
        logger.error("[Exchange] ClientError: %s", str(client_error))
        response_model = ExchangeErrorResponseModel(endpoint=request.url,
                                                    message="Internal Server Error",
                                                    status_code=500)
        return json(response_model.dict(), status=response_model.status_code)
    except KeyError as key_error:
        logger.error("[Exchange] ClientError: %s", str(key_error))
        response_model = ExchangeErrorResponseModel(endpoint=request.url,
                                                    message="Internal Server Error",
                                                    status_code=500)
        return json(response_model.dict(), status=response_model.status_code)
    else:
        return json(external_service_input_model.dict())
