from asyncio import AbstractEventLoop
import pickle
from typing import Dict
from socket import AF_INET

import aiohttp
from aiocache import Cache, SimpleMemoryCache
from dropbox import Dropbox
from sanic import Sanic
from sanic.log import logger
import ujson
from prophet import Prophet

from app.utils.constans import NAME_CODE_MAPPING

__all__ = ['init_aiohttp_session', 'load_models', 'init_aiocache']


async def init_aiohttp_session(app: Sanic, loop: AbstractEventLoop):
    app.ctx.aiohttp_session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(
        resolver=aiohttp.AsyncResolver(),
        family=AF_INET,
        ssl=False),
        json_serialize=ujson.dumps,

    )


async def init_aiocache(app: Sanic, loop: AbstractEventLoop):
    app.ctx.aiocache = Cache(Cache.MEMORY)


async def load_models(app: Sanic, loop: AbstractEventLoop):
    import warnings
    import logging
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=DeprecationWarning)
    logging.getLogger("pystan").propagate = False

    dropbox_key = app.config.DROPBOX_API_KEY
    models_path = app.config.MODELS_PATH
    logger.info("[Loading Models] Connecting to DropBox")
    dbx: Dropbox = Dropbox(dropbox_key)
    _, response = dbx.files_download(path=models_path)
    if response.status_code != 200:
        logger.critical(
            "[Loading Models] Problem with DropBox API, can not load models. Status code: %d' % response.status_code"
        )
        raise ConnectionError('Problem with DropBox API, can not load models. Status code: %d' % response.status_code)
    logger.info("[Loading Models] Models downloaded from DropBox ")
    logger.info("[Loading Models] Preparing models")
    models_dict: Dict = pickle.loads(response.content)
    forecast_dictionary = {}
    for key in models_dict.keys():
        model: Prophet = models_dict[key]['model']
        future = model.make_future_dataframe(periods=365)
        temp_model = model.predict(future)
        temp_model = temp_model[['ds', 'yhat']].set_index('ds')
        forecast_dictionary[NAME_CODE_MAPPING[key]] = temp_model.rename(columns={'yhat': 'Close'})
    app.ctx.forecast_dictionary = forecast_dictionary

    logger_parent = logger.parent
    handler_to_delete = logger_parent.handlers[0]
    logger_parent.removeHandler(handler_to_delete)

    logger.info("[Loading Models] Models ready to use")
