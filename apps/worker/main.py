"""Worker service: pulls tasks from `planner_queue`, simulates work, inserts into `review_queue`."""

from __future__ import annotations
import asyncio
import json
import uuid

from motor.motor_asyncio import AsyncIOMotorClient

from .models import WorkerOutput


async def process_task(doc: dict) -> WorkerOutput:
    # minimal fake processing
    content_id = uuid.uuid4().hex
    confidence = round(0.7 + (hash(doc.get("taskId", "")) % 30) / 100, 2)
    notes = f"Generated for goal: {doc.get('context', {}).get('goalDescription', '')}"
    await asyncio.sleep(2)
    return WorkerOutput(contentId=content_id, confidence=confidence, notes=notes)


async def main(mongo_url: str = "mongodb://localhost:27017", db_name: str = "chimera", worker_id: str | None = None):
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    worker_id = worker_id or uuid.uuid4().hex
    print("Worker started, polling planner_queue...", worker_id)

    while True:
        # atomically find one pending task and mark it inProgress
        doc = await db.planner_queue.find_one_and_update(
            {"status": "pending"},
            {"$set": {"status": "inProgress", "assignedWorkerId": worker_id}},
            sort=[("_id", 1)],
            return_document=True,
        )
        if not doc:
            await asyncio.sleep(1)
            continue

        out = await process_task(doc)
        # insert into review_queue
        await db.review_queue.insert_one(out.model_dump())
        # update original task status to review
        await db.planner_queue.update_one({"_id": doc["_id"]}, {"$set": {"status": "review"}})
        print("Worker produced content", out.contentId)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker stopped")
