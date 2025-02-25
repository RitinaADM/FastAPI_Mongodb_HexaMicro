import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from user_service.app.core.container import Container
from user_service.app.core.config import settings
from user_service.app.presentation.api.users import router as users_router
from user_service.app.presentation.api.auth import router as auth_router

from user_service import __version__

# Настройка логирования
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="User Service",
    version=__version__,
    description="A user management and authentication microservice."
)
# Добавляем middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8002"],  # Разрешаем все origins (или укажите конкретные, например, ["http://localhost:8002"])
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, OPTIONS и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception: %s", str(exc), extra={"context": f"request_path={request.url.path}"})
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing application", extra={"context": "lifespan=start"})
    container = Container(settings)
    app.state.container = container
    app.state.user_manager = await container.get_user_manager()
    await app.state.user_manager.repository.init_indexes()
    logger.info("Application initialized", extra={"context": "lifespan=ready"})
    yield
    await container.close()
    logger.info("Application shutdown", extra={"context": "lifespan=shutdown"})

app.router.lifespan_context = lifespan
app.include_router(auth_router)
app.include_router(users_router)

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server", extra={"context": "server=start"})
    uvicorn.run(app, host="0.0.0.0", port=8000)