import json
from common.redis_client import redis_client, READY_QUEUE, DEAD_QUEUE

def retry_job(job):
    if(job["retries"] == 0):
        redis_client.lpush(DEAD_QUEUE, json.dumps(job))
        print("Job moved to deadletter queue:", job["id"])
    else:
        job["retries"] -= 1
        redis_client.lpush(READY_QUEUE, json.dumps(job))
        print("Retrying job:", job["id"])