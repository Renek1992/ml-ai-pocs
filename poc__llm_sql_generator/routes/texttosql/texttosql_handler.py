"""
API handler for health check.
"""
from logging import Logger
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Query




router = APIRouter(
    prefix="/v1/texttosql",
    tags=["texttosql"]
)

@router.get("/{query}")
def handle_texttosql() -> Dict[str, Any]:
    return {"pong": True}