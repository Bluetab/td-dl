from api.app import app
import redis

def cache_field_external_ids(external_ids):
    r = redis.from_url(url=app.config["REDIS_URI"])
    pipe = r.pipeline()
    pipe.delete("data_fields:external_ids")
    for chunk in chunks(external_ids, 200):
        pipe.sadd("data_fields:external_ids", *chunk)
    pipe.execute()

# Yield successive n-sized chunks from l.
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
