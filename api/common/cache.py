from api.app import app
import redis

def get_redis_client():
    return redis.from_url(url=app.config["REDIS_URI"])

def remove_cache(client):
    client.delete("data_fields:external_ids")

def cache_field_external_ids(client, external_ids):
    for chunk in chunks(external_ids, 100):
        client.sadd("data_fields:external_ids", *chunk)

# Yield successive n-sized chunks from l.
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
