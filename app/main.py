from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from middleware.security import check_token_valid
from app.routers import user_management, role, modules, brands, products, chat
from app.utils.email_utils import send_hello_email
from app.utils.logging_config import logger
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

app = FastAPI()

# Initialize Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Exception handler for rate limit
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."},
    )

# Apply token validation middleware
app.middleware("http")(check_token_valid)

# Global logging for all requests and exceptions
@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        logger.info(f"{request.method} {request.url.path} - {response.status_code}")
        return response
    except Exception as e:
        logger.exception(f"Unhandled error at {request.url.path}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"}
        )

# Root route
@app.get("/")
def root():
    logger.info("Root endpoint '/' accessed")
    return "Demo-Project"

# CORS settings
origins = ["http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers registration
app.include_router(user_management.router)
app.include_router(role.router)
app.include_router(modules.router)
app.include_router(brands.router)
app.include_router(products.router)
app.include_router(chat.router)

# APScheduler background job setup
scheduler = BackgroundScheduler()

def scheduled_email_job():
    logger.info("Running scheduled email job")
    send_hello_email("hemil.goyani@mobifly.tech")

@app.on_event("startup")
def start_scheduler():
    logger.info("🚀 Application startup")
    scheduler.add_job(scheduled_email_job, trigger="cron", hour=11, minute=0)
    scheduler.start()
    logger.info("🕒 Scheduler started: runs daily at 11:00 AM")

@app.on_event("shutdown")
def shutdown_scheduler():
    logger.info("🛑 Application shutdown")
    scheduler.shutdown()
