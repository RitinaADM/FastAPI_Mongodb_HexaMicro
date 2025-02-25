from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from note_service.app.application.note_manager import NoteManager
from note_service.app.domain.models.user import User
from jose import JWTError, jwt
from note_service.app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.auth_token_url)
def get_note_manager(request: Request) -> NoteManager:
    manager: NoteManager | None = getattr(request.app.state, "note_manager", None)
    if manager is None:
        raise HTTPException(status_code=500, detail="NoteManager not initialized")
    return manager

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return User(id=user_id, username="")
    except JWTError:
        raise credentials_exception