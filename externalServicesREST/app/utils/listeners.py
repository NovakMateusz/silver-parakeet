from asyncio import AbstractEventLoop

import aiohttp
from sanic import Sanic
import ujson

__all__ = ['init_aiohttp_session']


async def init_aiohttp_session(app: Sanic, loop: AbstractEventLoop):
    app.ctx.aiohttp_session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(
        resolver=aiohttp.AsyncResolver()),
        json_serialize=ujson.dumps
    )
