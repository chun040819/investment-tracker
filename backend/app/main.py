from fastapi import FastAPI

from app.core.config import settings
from app.routers import api_router

app = FastAPI(title=settings.app_name)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router)
