"""
Endpoint definition for v1.
"""
from fastapi import FastAPI, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from routes.health import health_handler


def create_app_v1() -> FastAPI:
    app = FastAPI()
    
    # set routes for fastapi app
    app.include_router(health_handler.router)


    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )

    return app