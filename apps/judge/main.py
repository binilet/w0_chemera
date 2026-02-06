"""Judge service: pulls from `review_queue`, evaluates confidence, logs decisions or HITL events."""

from __future__ import annotations
import asyncio
import json

from motor.motor_asyncio import AsyncIOMotorClient

from .models import JudgeDecision, HITLEvent


async def evaluate(doc: dict) -> None:
    content_id = doc.get("contentId")
    confidence = float(doc.get("confidence", 0))
    notes = doc.get("notes")

    if confidence >= 0.75:
        dec = JudgeDecision(contentId=content_id, approved=True, riskScore=1 - confidence, notes=notes)
        print("APPROVED:", dec.model_dump())
    else:
        hitl = HITLEvent(contentId=content_id, riskReason="low_confidence", escalationLevel="high")
        print("HITL_ESCALATION:", hitl.model_dump())
        # also insert into hitl_queue
        return hitl


async def main(mongo_url: str = "mongodb://localhost:27017", db_name: str = "chimera"):
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    print("Judge started, polling review_queue...")
    while True:
        doc = await db.review_queue.find_one_and_delete({})
        if not doc:
            await asyncio.sleep(1)
            continue
        res = await evaluate(doc)
        if res is not None:
            await db.hitl_queue.insert_one(res.model_dump())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Judge stopped")
