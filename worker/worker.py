import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))


import json
from concurrent.futures import ThreadPoolExecutor

from common.redis_client import redis_client
from common.redis_client import READY_QUEUE
from common.redis_client import PROCESSING_QUEUE

from worker.handlers import handle_job
from worker.retry import retry_job

executor = ThreadPoolExecutor(max_workers=4)

def worker_loop():
    print("worker loop started")
    while True:
        result = redis_client.brpop(READY_QUEUE)
        # brpop returns (queue_name, job_data)
        
        job_data = result[1]
        
        redis_client.lpush(PROCESSING_QUEUE, job_data)
        
        executor.submit(process_job, job_data)
        
def process_job(job_data):
    job = json.loads(job_data) # json string to dict
    
    try:
        handle_job(job)
        redis_client.lrem(PROCESSING_QUEUE, 1, job_data)
        print("Job completed successfully", job["id"])
        
    except Exception as e:
        retry_job(job)
        print("Job failed, retrying", job["id"], e)
        
if __name__ == "__main__":
    worker_loop()