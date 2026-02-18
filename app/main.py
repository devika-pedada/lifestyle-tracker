from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.logging import setup_logging
from app.routes.auth_routes import router as auth_router

setup_logging()

app = FastAPI(
    title="Lifestyle Tracker API", description="Backend for tracking habits, health, and productivity", version="1.0.0"
)

# Include routes
app.include_router(health_router)
app.include_router(auth_router)
