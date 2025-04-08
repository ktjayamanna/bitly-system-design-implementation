from fastapi import FastAPI
from .health import router as health_router
from .core import router as core_router
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from bitly.configs.app_configs import SENTRY_DSN, SENTRY_TRANSACTION_STYLE

sentry_sdk.init(
    dsn=SENTRY_DSN,
    send_default_pii=True,
    integrations=[
        FastApiIntegration(
            transaction_style=SENTRY_TRANSACTION_STYLE,
        ),
    ],
)

app = FastAPI(title="Read Microservice", version="1.0.0")

# Include routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(core_router, tags=["core"])
