from fastapi import FastAPI
from app.api.health import router as health_router

app = FastAPI(
title="Lifestyle Tracker API",
description="Backend for tracking habits, health, and productivity",
version="1.0.0"
)

# Include routes
app.include_router(health_router)
