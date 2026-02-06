"""Planner service: reads goals, decomposes to tasks, pushes to Redis `task_queue`."""

from __future__ import annotations
import asyncio
import json
import uuid
from datetime import datetime
from typing import List

import redis.asyncio as redis

from .models import PlannerTask, PlannerContext


def mock_llm_decompose(goal: dict) -> List[dict]:
    """Mock LLM decomposition: returns a list of task payloads for a goal."""
    task = {
        "taskType": "generateContent",
        "priority": "medium",
        "context": {
            "goalDescription": goal.get("title", "generate content"),
            "personaConstraints": [],
            "requiredResources": [f"trend://{goal.get('trend',{}).get('topic','unknown')}"],
        },
    }
    return [task]


async def main(redis_url: str = "redis://localhost:6379/0"):
    r = redis.from_url(redis_url)

    # read local goals.json
    with open("apps/planner/goals.json", "r", encoding="utf-8") as f:
        goals = json.load(f)

    for goal in goals:
        tasks = mock_llm_decompose(goal)
        for t in tasks:
            task = PlannerTask(
                taskId=uuid.uuid4().hex,
                taskType=t["taskType"],
                priority=t["priority"],
                context=PlannerContext(**t["context"]),
                assignedWorkerId=None,
                createdAt=datetime.utcnow(),
                status="pending",
            )
            # push to Redis list named `task_queue`
            await r.rpush("task_queue", task.model_dump_json())
            print("Enqueued task", task.taskId)

    await r.close()


if __name__ == "__main__":
    asyncio.run(main())
