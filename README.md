<h1 align="center">EvalForge — LLM Evaluation Platform</h1>

EvalForge is a production-style AI evaluation system that scores and analyzes LLM responses using another LLM as a judge.
It is built with an asynchronous FastAPI backend, a Streamlit frontend, and uses Supabase PostgreSQL to store evaluation results.

The platform allows users to submit a prompt, an AI response, and a rubric, then receive structured evaluation results including a score, reasoning, and latency metrics.

Live App
https://evalforge-llm-evaluator.streamlit.app/

## Overview
EvalForge evaluates AI-generated responses using the LLM-as-judge pattern. You provide a prompt and an AI response, choose a model and rubric, and EvalForge returns a score (1-10) with detailed reasoning. Every evaluation is logged to a PostgreSQL database for analysis.
This mirrors real-world AI evaluation pipelines used by frontier AI labs to measure model quality at scale.

## Architecture
<img width="464" height="377" alt="image" src="https://github.com/user-attachments/assets/fbd9eb1d-3b36-4ede-9104-f6ad49382600" />

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI |
| Language | Python |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy (Async) |
| Database | PostgreSQL (Supabase) |
| LLM Judge | Groq API (LLaMA 3.3 70B Versatile, LLaMA 3 8B) |
| Frontend | Streamlit |
| Backend Hosting | Render |
| Frontend Hosting | Streamlit Cloud |


## API Endpoints 

### POST /evaluate
Submit a response for evaluation.
#### Request body:
<img width="772" height="258" alt="image" src="https://github.com/user-attachments/assets/1c819a6b-8224-4bc3-b0f9-2d1c5237f767" />

#### Response:
<img width="794" height="224" alt="image" src="https://github.com/user-attachments/assets/6aef85e7-1739-47a8-84c3-3d59a4a3f1ba" />

#### GET /evaluations
Returns all past evaluations.
#### GET /evaluations/{evaluation_id}
Returns a specific evaluation by ID.

## Database Schema
<img width="408" height="272" alt="image" src="https://github.com/user-attachments/assets/5b178537-c745-41ca-8ff6-35ec6af24c1b" />

## Design Decisions
**Why async FastAPI?**  
LLM API calls are I/O bound and slow. Async allows the server to handle multiple evaluation requests concurrently without blocking.

**Why Pydantic v2?**  
Two validation layers — input validation catches bad data before it reaches the LLM, while output validation ensures the judge response is always structured correctly.

**Why UUID for primary key?**  
Sequential integer IDs are predictable and guessable. UUIDs are globally unique and secure, which is important when evaluation IDs are exposed in API responses.

**Why LLM-as-judge?**  
Rule-based metrics like BLEU and ROUGE cannot measure reasoning quality or helpfulness. A powerful LLM judge evaluates responses the way a human expert would, at scale.

 ### **~Built by Sarthak Singh**

