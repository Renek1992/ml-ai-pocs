"""
API handler for search.
"""
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from api.llm_search_app.agent import VectorEmbeddingBot


class SearchInput(BaseModel):
    prompt: str
    llm_name: str
    llm_kwargs: str
    no_results: int


router = APIRouter(
    prefix="/v1/search",
    tags=["search"]
)


@router.get("/sim_search")
def handle_search(input: SearchInput) -> Dict[str, Any]:
    print(f"""
        >>>>> {input}
        >>>>> {input.prompt}
        >>>>> {input.llm_name}
        >>>>> {input.llm_kwargs}
        >>>>> {input.no_results}
    """)
    vector_embeddings_bot = VectorEmbeddingBot(
        query=input.prompt,
        model_name=input.llm_name,
        model_kwargs=input.llm_kwargs,
        no_of_matches=input.no_results
    )
    resp = vector_embeddings_bot.create_response()
    return {"message": resp}