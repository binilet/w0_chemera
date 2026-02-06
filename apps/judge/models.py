from __future__ import annotations
from pydantic import BaseModel


class JudgeDecision(BaseModel):
    contentId: str
    approved: bool
    riskScore: float | None = None
    notes: str | None = None


class HITLEvent(BaseModel):
    contentId: str
    riskReason: str
    escalationLevel: str
