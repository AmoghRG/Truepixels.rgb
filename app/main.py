"""TruePixels.rgb - Main FastAPI Application Entry Point.

Conforms to Module Interface Contract Section 3.1 & 3.2.
"""
import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.m1_access.router_auth import router as auth_router
from app.m1_access.router_images import router as images_router
from app.m1_access.router_users import router as users_router
from app.shared.db import init_db
from app.shared.errors import (
    AppException,
    app_exception_handler,
    global_exception_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database tables
    init_db()
    yield


app = FastAPI(
    title="TruePixels.rgb API",
    description="An AI-Generated Image Detection System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_id_and_timing_middleware(request: Request, call_next):
    """Assigns unique request_id and measures server latency."""
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    return response


# Register exception handlers for contract compliance
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Mount M1 Routers under /api/v1
app.include_router(auth_router, prefix="/api/v1")
app.include_router(images_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "TruePixels.rgb API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
