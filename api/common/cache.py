from api.app import app
import redis
from redis.exceptions import WatchError

def get_redis_client():
    return redis.from_url(url=app.config["REDIS_URI"])


def remove_cache(client):
    lua = """
            redis.call('HDEL', KEYS[1], 'external_id')
            if redis.call('HLEN', KEYS[1]) == 0 then
                redis.call('DEL', KEYS[1])
            end
        """
    delete_extenal_id = client.register_script(lua)
    for key in client.scan_iter("data_field:*"):
        delete_extenal_id(keys=[key])

def cache_field_external_id(client, record):
    system = record["system"]
    group = record["group"]
    structure = record["structure"]
    field = record["field"]
    external_id = record["external_id"]
    key = "data_field:{}:{}:{}:{}".format(system, group, structure, field)
    client.hmset(key, {"external_id": external_id})
