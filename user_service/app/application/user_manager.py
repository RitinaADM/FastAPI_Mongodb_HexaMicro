import logging
from typing import Optional, List
from fastapi import HTTPException
from user_service.app.domain.models.user import User, UserCreate, UserUpdate
from user_service.app.domain.interfaces import UserRepository
from user_service.app.core.auth import get_password_hash, verify_password

logger = logging.getLogger(__name__)

class UserManager:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def register_user(self, user: UserCreate) -> User:
        logger.info("Registering user", extra={"context": f"username={user.username}"})
        existing_user = await self.repository.get_user_by_username(user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        hashed_password = get_password_hash(user.password)
        new_user = User(username=user.username, email=user.email, password_hash=hashed_password, role=user.role)
        return await self.repository.create_user(new_user)

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = await self.repository.get_user_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    async def get_user(self, user_id: str) -> User:
        logger.debug("Fetching user", extra={"context": f"user_id={user_id}"})
        user = await self.repository.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def update_user(self, user_id: str, user_update: UserUpdate) -> User:
        logger.info("Updating user", extra={"context": f"user_id={user_id}"})
        update_data = user_update.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        updated_user = await self.repository.update_user(user_id, update_data)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user

    async def delete_user(self, user_id: str) -> bool:
        logger.info("Deleting user", extra={"context": f"user_id={user_id}"})
        success = await self.repository.delete_user(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return success

    async def get_user_by_username(self, username: str) -> Optional[User]:
        logger.debug("Fetching user by username", extra={"context": f"username={username}"})
        return await self.repository.get_user_by_username(username)

    async def list_users(self) -> List[User]:
        logger.debug("Fetching all users")
        return await self.repository.list_users()  # Новый метод