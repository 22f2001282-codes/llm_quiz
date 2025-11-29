from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import os
from app.solver import handle_quiz
# main.py (place at repo root)
from app.main import app  # import the FastAPI object from app/main.py

app = FastAPI(title="LLM Quiz Solver - Starter")

class Task(BaseModel):
    email: str
    secret: str
    url: str

@app.post("/solve")
async def solve(task: Task):
    # validate secret (simple compare to env)
    if task.secret != os.getenv("MY_SECRET"):
        raise HTTPException(status_code=403, detail="Invalid secret")
    # run solver with timeout (3 minutes)
    try:
        result = await asyncio.wait_for(handle_quiz(task.dict()), timeout=180)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Timeout (3 minutes)")
    return result

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
