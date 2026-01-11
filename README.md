# WorkQueue (Python)

A Redis-backed work queue implementation with a Django-based producer and a custom standalone worker, designed to demonstrate asynchronous job processing, failure handling, and system decoupling.

> **Note:** This project intentionally avoids high-level task frameworks (e.g., Celery) to make queue semantics, retries, and failure modes explicit and inspectable.

## Overview

The system separates job submission from job execution:

- The **producer** exposes an HTTP API to enqueue jobs.
- The **queue** (Redis) stores jobs durably.
- The **worker** consumes and executes jobs asynchronously.
- Failed jobs are retried a bounded number of times and then dead-lettered.

This design follows common patterns used in real-world background processing systems.

## High-Level Architecture

```
Client
  |
  |  POST /enqueue
  v
Django Producer
  |
  |  LPUSH
  v
Redis (READY_QUEUE)
  |
  |  BRPOP
  v
Worker Process
  |
  |  execute job
  |
  +--> success  -> remove from queue
  |
  +--> failure  -> retry or DEAD_QUEUE
```

## Job Model

A job is a data-only description of work, not execution logic.

Example job payload:

```json
{
  "id": "uuid",
  "type": "send_email",
  "payload": {
    "to": "user@example.com"
  },
  "retries": 3
}
```

**Key Points:**

- Jobs are serialized to JSON before being stored in Redis.
- Redis stores strings, not structured objects.
- Jobs may execute more than once (at-least-once delivery).

## Execution Semantics

### Delivery Guarantee

- **At-least-once execution**
- Jobs may run more than once
- Jobs are never silently lost

### Failure Handling

Each job carries a retry counter

On failure:
- `retries` are decremented
- job is re-queued

When `retries` reach zero:
- job is moved to a dead-letter queue

### Dead-Letter Queue

- Stores terminally failed jobs
- Used for inspection and debugging
- Prevents silent failure

## Why Django for the Producer

- Enforces a strict request/response lifecycle
- Provides input validation at the system boundary
- Keeps job submission isolated from execution
- Avoids long-running work inside HTTP requests

Django is used intentionally as a thin API layer, not as a task executor.

## Why a Custom Worker (Not Celery)

This project intentionally does not use Celery or similar frameworks.

**Reasons:**

- Queue behavior is explicit, not abstracted
- Retry logic is visible and controllable
- Failure modes are easier to reason about
- Demonstrates understanding of distributed job processing fundamentals

This is a learning and demonstration project, not a framework wrapper.

## Concurrency Model

- One worker process
- Multiple threads via `ThreadPoolExecutor`
- Suitable for I/O-bound workloads
- Horizontal scaling supported by running multiple workers against the same Redis instance

## Project Structure

```
workqueue-python/
├── producer/        # Django producer (HTTP boundary)
├── worker/          # Standalone worker process
├── common/          # Shared job and Redis contracts
├── .gitignore
└── README.md
```

## Running the Project

### Prerequisites

- Python 3.10+
- Redis

### Start Redis

```bash
redis-server
```

### Start Producer

```bash
cd producer
python manage.py runserver
```

### Start Worker

```bash
python -m worker.worker
```

### Enqueue a Job

```bash
POST http://127.0.0.1:8000/enqueue/

{
  "type": "send_email",
  "payload": {
    "to": "test@example.com"
  },
  "retries": 3
}
```

## Design Trade-offs

- Exactly-once execution is not attempted due to complexity
- Jobs must be idempotent
- Redis Lists are used instead of Streams for simplicity
- Execution state is kept minimal and explicit

## What This Project Demonstrates

- Asynchronous job processing
- Decoupling of HTTP and background execution
- Failure-aware system design
- Bounded retries and dead-letter queues
- Practical Redis usage
- Python packaging and module execution
- Clear separation of concerns
