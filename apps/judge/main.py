"""Judge service: pops from `review_queue`, evaluates confidence, logs decisions or HITL events."""

from __future__ import annotations
import asyncio
import json

import redis.asyncio as redis

from .models import JudgeDecision, HITLEvent


async def evaluate(item_json: str) -> None:
    data = json.loads(item_json)
    content_id = data.get("contentId")
    confidence = float(data.get("confidence", 0))
    notes = data.get("notes")

    if confidence >= 0.75:
        dec = JudgeDecision(contentId=content_id, approved=True, riskScore=1 - confidence, notes=notes)
        print("APPROVED:", dec.model_dump())
    else:
        hitl = HITLEvent(contentId=content_id, riskReason="low_confidence", escalationLevel="high")
        print("HITL_ESCALATION:", hitl.model_dump())


async def main(redis_url: str = "redis://localhost:6379/0"):
    r = redis.from_url(redis_url)
    print("Judge started, waiting for review items...")
    while True:
        item = await r.blpop("review_queue", timeout=5)
        if not item:
            await asyncio.sleep(1)
            continue
        _, review_json = item
        await evaluate(review_json)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Judge stopped")
