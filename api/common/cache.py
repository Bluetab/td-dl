from api.app import app
import redis
from redis.exceptions import WatchError

def get_redis_client():
    return redis.from_url(url=app.config["REDIS_URI"])

def remove_cache(client):
    for key in client.scan_iter("data_field:*"):
        with client.pipeline() as pipe:
            while 1:
                try:
                    pipe.watch(key)
                    pipe.multi()
                    pipe.hdel(key, "external_id")
                    if pipe.hlen(key) == 0:
                        pipe.delete(key)

                    pipe.execute()
                    break

                except WatchError:
                    continue

def cache_field_external_id(client, record):
    system = record["system"]
    group = record["group"]
    structure = record["structure"]
    field = record["field"]
    external_id = record["external_id"]
    key = "data_field:{}:{}:{}:{}".format(system, group, structure, field)
    client.hmset(key, {"external_id": external_id})
