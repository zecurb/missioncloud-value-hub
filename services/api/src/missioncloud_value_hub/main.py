from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from missioncloud_value_hub.api.routes.health import router as health_router
from missioncloud_value_hub.api.routes.value import router as value_router
from missioncloud_value_hub.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="FinOps value intelligence and optimization API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(value_router, prefix=settings.api_prefix)
