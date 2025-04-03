"""
API entry point.
"""
from fastapi import FastAPI
from api.routes.health import health_handlers
from api.routes.search import search_handlers
from api.routes.embed import embed_handlers

app = FastAPI()

app.include_router(health_handlers.router)
app.include_router(search_handlers.router)
app.include_router(embed_handlers.router)


@app.get("/")
async def root():
    return {"message": "Hello World!!!!!"}