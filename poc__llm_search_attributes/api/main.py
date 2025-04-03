"""
API entry point.
"""
from pydantic import BaseModel
from fastapi import FastAPI

from app.model.orchestrator import LlmOrchestrator



class UserInput(BaseModel):
    prompt: str




app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health-check")
async def say_hello():
    return {"message": "Healthy!"}


@app.get("/search")
async def search(input: UserInput):
    llm_orchestrator = LlmOrchestrator()
    resp = llm_orchestrator.generate_response(
        query=input.prompt
    )
    return {"message": resp}