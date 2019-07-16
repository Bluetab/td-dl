from api.app import app
import redis

def cache_structures_external_ids(system_external_ids):
    r = redis.from_url(url=app.config["REDIS_URI"])
    keys = r.keys("structures:external_ids:*")
    keys = list(map(lambda bkey: f"{str(bkey, 'utf-8')}", keys))
    if keys:
        r.delete(*keys)

    pipe = r.pipeline()
    for system_external_id, external_ids in system_external_ids.items():
        redis_key = f"structures:external_ids:{system_external_id}"
        for chunk in chunks(external_ids, 200):
            pipe.sadd(redis_key, *chunk)
    pipe.execute()

# Yield successive n-sized chunks from l.
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
