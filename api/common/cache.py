from api.app import app
import redis

def get_redis_client():
    return redis.from_url(url=app.config["REDIS_URI"])

def cache_field_external_id(client, record):
    system = record["system"]
    group = record["group"]
    structure = record["structure"]
    field = record["field"]
    external_id = record["external_id"]
    key = "data_field:{}:{}:{}:{}".format(system, group, structure, field)
    client.hmset(key, {"external_id": external_id})
