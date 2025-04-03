from fastapi import FastAPI
from .health import router as health_router
from .core import router as core_router

app = FastAPI(title="Write Microservice", version="1.0.0")

# Include routers
app.include_router(health_router, tags=["health"])
app.include_router(core_router, tags=["core"])
