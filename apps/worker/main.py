"""Worker service: pops tasks from `task_queue`, simulates work, pushes to `review_queue`."""

from __future__ import annotations
import asyncio
import json
import uuid

import redis.asyncio as redis

from .models import WorkerOutput


async def process_task(task_json: str) -> WorkerOutput:
    # minimal fake processing
    task = json.loads(task_json)
    content_id = uuid.uuid4().hex
    confidence = round(0.7 + (hash(task.get("taskId", "")) % 30) / 100, 2)
    notes = f"Generated for goal: {task.get('context',{}).get('goalDescription','') }"
    await asyncio.sleep(2)
    return WorkerOutput(contentId=content_id, confidence=confidence, notes=notes)


async def main(redis_url: str = "redis://localhost:6379/0"):
    r = redis.from_url(redis_url)
    print("Worker started, waiting for tasks...")
    while True:
        item = await r.blpop("task_queue", timeout=5)
        if not item:
            await asyncio.sleep(1)
            continue
        _, task_json = item
        out = await process_task(task_json)
        await r.rpush("review_queue", out.model_dump_json())
        print("Pushed review item", out.contentId)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker stopped")
