from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime


class PlannerContext(BaseModel):
    goalDescription: str
    personaConstraints: List[str] = []
    requiredResources: List[str] = []


class PlannerTask(BaseModel):
    taskId: str
    taskType: Literal["generateContent", "replyComment"]
    priority: Literal["high", "medium", "low"]
    context: PlannerContext
    assignedWorkerId: Optional[str] = None
    createdAt: datetime
    status: Literal["pending", "inProgress", "review", "complete"]
