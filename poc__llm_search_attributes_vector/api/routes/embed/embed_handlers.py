"""
API handler for embedding.
"""
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from api.llm_search_app.agent import VectorEmbeddingBot


class EmbedInput(BaseModel):
    no_profiles: int
    llm_name: str
    llm_kwargs: Optional[str]


router = APIRouter(
    prefix="/v1/embed",
    tags=["embed"]
)


@router.post("/vector_embed")
def handle_embed(input: EmbedInput) -> Dict[str, Any]:
    vector_embeddings_bot = VectorEmbeddingBot(
        no_profiles_to_embed=input.no_profiles,
        model_name=input.llm_name,
        model_kwargs=input.llm_kwargs
    )
    resp = vector_embeddings_bot.create_embeddings()
    return {"message": resp}