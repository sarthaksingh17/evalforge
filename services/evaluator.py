import time
import uuid
import os
from groq import AsyncGroq
from dotenv import load_dotenv
import json

load_dotenv()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

async def evaluate_response(prompt: str, response: str, rubric: str, judge_model: str):
    
    start_time = time.time()

    completion = await client.chat.completions.create(
        model=judge_model,
        messages=[
            {
                "role": "system",
                "content": """You are an expert evaluator. 
                Evaluate the given AI response and return ONLY a JSON object:
            {"score": <1-10>, "reasoning": "<string>"}"""
        },
        {
            "role": "user",
            "content": f"""Prompt: {prompt}
            AI Response: {response}
            Rubric: {rubric}
            Evaluate and return JSON only."""
        }
    ]
)

    end_time = time.time()
    latency_ms = (end_time - start_time) * 1000

    result = json.loads(completion.choices[0].message.content)

    return {
        "evaluation_id": str(uuid.uuid4()),
        "score": result["score"],
        "reasoning": result["reasoning"],
        "latency_ms": round(latency_ms, 2)
    }
