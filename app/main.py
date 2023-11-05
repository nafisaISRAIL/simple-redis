import json
import os
from aiohttp import web
import redis.asyncio as redis
from aiohttp.web import Application, Response


REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.StrictRedis(host=REDIS_HOST, port=6379, decode_responses=True)


async def get_all_keys(_) -> Response:
    keys = []
    for key in await redis_client.keys():
        value = await redis_client.get(key)
        keys.append({key: value})
    return Response(status=200, body=json.dumps(keys), content_type="application/json")


async def add_key(request) -> Response:
    data = await request.json()
    await redis_client.set(data["key"], data["value"])
    return Response(status=200, body=json.dumps(data), content_type="application/json")


async def delete_key(request) -> Response:
    data = await request.json()
    await redis_client.delete(data["key"])
    return Response(status=204, content_type="application/json")


async def init() -> Application:
    app = Application()
    app.add_routes([
        web.get('/', get_all_keys),
        web.post('/', add_key),
        web.delete('/', delete_key)])
    return app

if __name__ == "__main__":
    application = init()
    web.run_app(application, port=8080)
