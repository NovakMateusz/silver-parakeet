from sanic import Blueprint, json, Request

__all__ = ['health_blueprint']

health_blueprint = Blueprint('health_blueprint')


@health_blueprint.get('/health')
async def health_view(request: Request):
    return json({"status": "ok"})
