"""Planner service: reads goals, decomposes to tasks, inserts into MongoDB `planner_queue`."""

from __future__ import annotations
import asyncio
import json
import uuid
from datetime import datetime
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

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


async def main(mongo_url: str = "mongodb://localhost:27017", db_name: str = "chimera"):
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]

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
            # insert into MongoDB collection named `planner_queue`
            await db.planner_queue.insert_one(task.model_dump())
            print("Inserted planner task", task.taskId)

    client.close()


if __name__ == "__main__":
    asyncio.run(main())
