import uuid
from dataclasses import dataclass
from typing import Dict

@dataclass
class Job:
    id: str
    type: str
    payload: Dict
    retries: int
    
    @staticmethod
    def create(type, payload, retries):
        return Job(
            id = str(uuid.uuid4()),
            type = type,
            payload = payload,
            retries = retries
        )