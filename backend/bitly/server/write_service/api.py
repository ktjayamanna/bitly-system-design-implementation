from fastapi import FastAPI
from .health import router as health_router
from .core import router as core_router
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from dotenv import load_dotenv
import os

load_dotenv('backend/.vscode/.env')

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    send_default_pii=True,
    integrations=[
        FastApiIntegration(
            transaction_style=os.getenv("SENTRY_TRANSACTION_STYLE", "url"),  # Use URL path as transaction name
        ),
    ],
)

app = FastAPI(title="Write Microservice", version="1.0.0")

# Include routers
app.include_router(health_router, tags=["health"])
app.include_router(core_router, tags=["core"])
