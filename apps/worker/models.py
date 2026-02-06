from __future__ import annotations
from pydantic import BaseModel


class WorkerOutput(BaseModel):
    contentId: str
    confidence: float
    notes: str
