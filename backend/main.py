"""
Silent Signal - Main FastAPI Application
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
import structlog

from backend.config import settings
from backend.middleware.logging import LoggingMiddleware
from backend.middleware.rate_limit import RateLimitMiddleware
from backend.routes import auth, gestures, users, payments, search, admin, health, analytics

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting Silent Signal API", env=settings.APP_ENV)
    yield
    logger.info("Shutting down Silent Signal API")


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Silent Signal - Gesture-based communication platform",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# Templates
templates = Jinja2Templates(directory="frontend/templates")

# API Routes
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(gestures.router, prefix="/api/gestures", tags=["Gestures"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])

# Page Routes
@app.get("/")
async def root(request: Request):
    """Landing page"""
    return templates.TemplateResponse("landing.html", {"request": request})


@app.get("/dashboard")
async def dashboard(request: Request):
    """Analytics dashboard - Charts and statistics"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/capture")
async def capture_page(request: Request):
    """Gesture capture page - Camera interface"""
    return templates.TemplateResponse("capture.html", {"request": request})


@app.get("/test")
async def api_test(request: Request):
    """API testing page"""
    return templates.TemplateResponse("api_test.html", {"request": request})


@app.get("/pricing")
async def pricing(request: Request):
    """Pricing page"""
    return templates.TemplateResponse("pricing.html", {"request": request})


@app.get("/demo")
async def demo_mode(request: Request):
    """Demo mode - no authentication required"""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "demo_mode": True,
        "user": {"email": "demo@silentsignal.ai", "full_name": "Demo User"}
    })


@app.get("/setup")
async def setup_guide(request: Request):
    """Setup and configuration guide"""
    return templates.TemplateResponse("setup.html", {"request": request})


@app.get("/settings")
async def user_settings(request: Request):
    """User settings page"""
    return templates.TemplateResponse("settings.html", {"request": request})

# Static files (mount last to avoid catching other routes)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
