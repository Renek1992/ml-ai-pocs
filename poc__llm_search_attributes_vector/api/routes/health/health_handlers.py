"""
API handler for health check.
"""
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Query


router = APIRouter(
    prefix="/v1/health",
    tags=["health"]
)

@router.get("/ping")
def handle_ping() -> Dict[str, Any]:
    return {"pong": True}