from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application instance.

    This service acts as the main backend entrypoint for:
    - Evidence upload and registration.
    - Evidence retrieval.
    - Integrity verification against blockchain-backed hashes.
    """
    app = FastAPI(
        title="Blockchain-Backed Digital Forensics & Chain-of-Custody API",
        version="0.1.0",
        description=(
            "Backend service for managing digital evidence, custody events, "
            "and integrity verification, backed by PostgreSQL and Ethereum."
        ),
    )

    # CORS configuration can be tightened for specific frontends/environments.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api")

    return app


app = create_application()

