from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from user_service.app.core.config import settings
from user_service.app.application.user_manager import UserManager
from user_service.app.core.auth import decode_access_token
from user_service.app.domain.models.user import User, UserRole

from fastapi import Depends, HTTPException, status


# Определяем схемы авторизации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.auth_token_url)

def get_user_manager(request: Request) -> UserManager:
    manager: UserManager | None = getattr(request.app.state, "user_manager", None)
    if manager is None:
        raise HTTPException(status_code=500, detail="UserManager not initialized")
    return manager

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    manager: UserManager = Depends(get_user_manager)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    user = await manager.get_user(user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user