from api.app import app
import redis
from redis.exceptions import WatchError

def get_redis_client():
    return redis.from_url(url=app.config["REDIS_URI"])


def remove_cache(client):
    lua = """
        if redis.call('TYPE', KEYS[1])['ok'] == 'hash' then
          redis.call('HDEL', KEYS[1], 'external_id')
          if redis.call('HLEN', KEYS[1]) == 0 then
              redis.call('DEL', KEYS[1])
          end
        end
        """
    delete_extenal_id = client.register_script(lua)
    for key in client.scan_iter("data_field:*"):
        delete_extenal_id(keys=[key])

def cache_field_external_id(client, record):
    external_id = record["external_id"]
    if external_id.count(".") == 3:
        external_id_key = external_id.replace(".", ":")
        key = "data_field:{}".format(external_id_key)
        client.hmset(key, {"external_id": external_id})
