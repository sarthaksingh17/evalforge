from pydantic import BaseModel, Field
from typing import Optional

class EvaluationRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    response: str = Field(..., min_length=1)
    rubric: Optional[str] = "Rate the response on accuracy, helpfulness and clarity"
    judge_model: str = "llama-3.3-70b-versatile"


class EvaluationResponse(BaseModel):
    evaluation_id: str
    score: int = Field(..., ge=1, le=10)
    reasoning: str
    latency_ms: float

    class Config:
        from_attributes = True