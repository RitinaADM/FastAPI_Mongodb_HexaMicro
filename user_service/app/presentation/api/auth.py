from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from user_service.app.application.user_manager import UserManager
from user_service.app.core.dependencies import get_user_manager, get_current_user
from user_service.app.domain.models.user import UserView, UserCreate, UserUpdate, User, UserRole
from user_service.app.core.auth import create_access_token
from user_service.app.core.metrics import REQUEST_COUNT, REQUEST_LATENCY
from datetime import timedelta
from time import time

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserView)
async def register_user(
    user: UserCreate,
    manager: UserManager = Depends(get_user_manager)
) -> UserView:
    start_time = time()
    REQUEST_COUNT.labels(method="POST", endpoint="/api/auth/register").inc()
    try:
        created_user = await manager.register_user(user)  # Роль уже фиксирована внутри register_user как USER
        return created_user
    finally:
        REQUEST_LATENCY.labels(endpoint="/api/auth/register").observe(time() - start_time)


@router.post("/login", response_model=dict)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    manager: UserManager = Depends(get_user_manager)
) -> dict:
    start_time = time()
    REQUEST_COUNT.labels(method="POST", endpoint="/api/auth/login").inc()
    user = await manager.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.id, "role": user.role},  # Добавляем роль в токен
        expires_delta=access_token_expires
    )
    REQUEST_LATENCY.labels(endpoint="/api/auth/login").observe(time() - start_time)
    return {"access_token": access_token, "token_type": "bearer"}