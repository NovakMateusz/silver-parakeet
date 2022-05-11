from asyncio import AbstractEventLoop
from datetime import datetime, date, timedelta
import pickle
from typing import Dict
from socket import AF_INET

import aiohttp
from aiocache import Cache
from dropbox import Dropbox
from dropbox.exceptions import BadInputError
from sanic import Sanic
from sanic.log import logger
import ujson
from prophet import Prophet
import pandas as pd


from app.utils.constans import NAME_CODE_MAPPING

__all__ = ['init_aiohttp_session', 'load_models', 'init_aiocache', 'load_historical_data']

pd.options.mode.chained_assignment = None


async def init_aiohttp_session(app: Sanic, loop: AbstractEventLoop):
    logger.info("[AIOHTTP Session initiation] Process start")
    app.ctx.aiohttp_session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(
        resolver=aiohttp.AsyncResolver(),
        family=AF_INET,
        ssl=False),
        json_serialize=ujson.dumps,

    )
    logger.info("[AIOHTTP Session initiation] Session created")


async def init_aiocache(app: Sanic, loop: AbstractEventLoop):
    logger.info("[AIOCACHE initiation] Process start")
    app.ctx.aiocache = Cache(Cache.MEMORY)
    logger.info("[AIOCACHE Session initiation] Cache created")


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
    try:
        _, response = dbx.files_download(path=models_path)
    except BadInputError as error:
        logger.error("[Loading Models] Error occurred while while connection to DropBox")
        raise BadInputError(error.request_id, error.message)
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


async def load_historical_data(app: Sanic, loop: AbstractEventLoop):
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop(['Vol.', 'Change %'], axis=1)
        columns_to_convert = list(df.columns)
        columns_to_convert.remove('Date')
        for column in columns_to_convert:
            df[column] = df[column].str.replace(',', '')
        df = df[['Date', 'Price']]
        df = df.astype({'Price': 'float'})
        return df

    logger.info("[Loading historical data] Proces start")
    historical_data_dict: Dict = {}
    for file in app.config.DATA_DIR.glob('*HistoricalData.csv'):
        filename = file.name
        currency_name = filename.split('HistoricalData.csv')[0]
        raw_df = pd.read_csv(filepath_or_buffer=str(file),
                             parse_dates=['Date'],
                             date_parser=lambda dates: datetime.strptime(dates, '%b %d, %Y'),
                             dtype=str
                             )
        clean_df = clean_dataframe(raw_df)
        df = clean_df.loc[clean_df['Date'] > str(date.today() - timedelta(days=365))]
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        df.set_index('Date', inplace=True)
        df = df[::-1]
        historical_data_dict[NAME_CODE_MAPPING[currency_name]] = df
    app.ctx.historical_data = historical_data_dict
    logger.info("[Loading historical data] All datasets loaded into memory")
