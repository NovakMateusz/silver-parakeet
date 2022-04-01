from sanic import json, Request

from app.health import health_blueprint


@health_blueprint.get('/health')
async def health_view(request: Request):
    return json({"status": "ok"})
