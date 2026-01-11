import redis

redis_client = redis.Redis(
    host = "localhost",
    port = 6379,
    decode_responses = True,
)

READY_QUEUE = "workqueue:ready"
PROCESSING_QUEUE = "workqueue:processing"
DEAD_QUEUE = "workqueue:dead"