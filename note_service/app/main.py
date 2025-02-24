"""
Основная точка входа приложения Note Service.
Используется FastAPI с управлением ресурсами через lifespan, что соответствует принципам
гексагональной архитектуры: бизнес-логика (application/domain) отделена от инфраструктуры.
"""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from note_service.app.core.container import Container
from note_service.app.core.config import settings
from note_service.app.presentation.api.notes import router as notes_router
from note_service import __version__

# Настройка логирования с использованием конфигурации из settings
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Note Service",
    version=__version__,
    description="A simple note management microservice built with hexagonal architecture."
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Глобальный обработчик исключений, возвращающий статус 500 при возникновении ошибки.
    """
    logger.error("Unhandled exception: %s", str(exc), extra={"context": f"request_path={request.url.path}"})
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan-менеджер для инициализации и корректного завершения работы приложения.
    Здесь создаётся контейнер зависимостей и инициализируется менеджер заметок.
    """
    logger.info("Initializing application", extra={"context": "lifespan=start"})
    container = Container(settings)
    app.state.container = container
    app.state.note_manager = await container.get_note_manager()
    await app.state.note_manager.repository.init_indexes()
    logger.info("Application initialized", extra={"context": "lifespan=ready"})
    yield
    await container.close()
    logger.info("Application shutdown", extra={"context": "lifespan=shutdown"})

app.router.lifespan_context = lifespan
app.include_router(notes_router)

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server", extra={"context": "server=start"})
    uvicorn.run(app, host="0.0.0.0", port=8000)
