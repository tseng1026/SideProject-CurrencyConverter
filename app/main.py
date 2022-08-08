from app.api.v1.api_router import api_router
from app.constants import settings
from fastapi import FastAPI

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
)

app.include_router(api_router, prefix=settings.API_PREFIX)
