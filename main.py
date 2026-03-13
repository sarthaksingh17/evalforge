from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import engine, Base, get_db
from models import Evaluation
from schemas import EvaluationRequest, EvaluationResponse
from services.evaluator import evaluate_response

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate(request: EvaluationRequest, db: AsyncSession = Depends(get_db)):
    
    result = await evaluate_response(
    request.prompt,
    request.response,
    request.rubric,
    request.judge_model
)
    
    evaluation = Evaluation(
        id=result["evaluation_id"],
        prompt=request.prompt,
        response=request.response,
        rubric=request.rubric,
        score=result["score"],
        reasoning=result["reasoning"],
        latency_ms=result["latency_ms"]
    )
    
    db.add(evaluation)
    await db.commit()
    await db.refresh(evaluation)
    
    return EvaluationResponse(
        evaluation_id=evaluation.id,
        score=evaluation.score,
        reasoning=evaluation.reasoning,
        latency_ms=evaluation.latency_ms
    )

@app.get("/evaluations", response_model=list[EvaluationResponse])
async def get_evaluations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Evaluation))
    evaluations = result.scalars().all()
    return evaluations

@app.get("/evaluations/{evaluation_id}", response_model=EvaluationResponse)
async def get_evaluation(evaluation_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Evaluation).where(Evaluation.id == evaluation_id))
    evaluation = result.scalar_one_or_none()
    
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    return evaluation