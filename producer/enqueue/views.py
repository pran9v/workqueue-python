import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EnqueueSerializer
from common.redis_client import redis_client, READY_QUEUE
from common.job import Job

@api_view(["POST"])
def enqueue(request):
    serializer = EnqueueSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    job = Job.create(**serializer.validated_data)
    redis_client.lpush(READY_QUEUE, json.dumps(job.__dict__))

    return Response({
        "status": "enqueued",
        "job_id": job.id
    })
