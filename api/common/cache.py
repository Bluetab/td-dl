from api.app import app
import redis
from redis.exceptions import WatchError

def get_redis_client():
    return redis.from_url(url=app.config["REDIS_URI"])

def remove_cache(client):
    client.delete("data_fields:external_ids")

def cache_field_external_id(client, record):
    external_id = record["external_id"]
    if external_id.count(".") == 3:
        client.sadd("data_fields:external_ids", external_id)
