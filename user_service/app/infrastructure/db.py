from typing import Optional, List
from bson.objectid import ObjectId, InvalidId
from datetime import datetime
from user_service.app.domain.models.user import User
from user_service.app.domain.interfaces import UserRepository
import logging

logger = logging.getLogger(__name__)

class MongoUserRepository(UserRepository):
    def __init__(self, db) -> None:
        self.collection = db.get_collection("users")

    async def init_indexes(self) -> None:
        await self.collection.create_index("username", unique=True)
        logger.info("User indexes initialized")

    async def create_user(self, user: User) -> User:
        user_dict = user.dict(exclude={"id"})
        result = await self.collection.insert_one(user_dict)
        user.id = str(result.inserted_id)
        return user

    async def get_user(self, user_id: str) -> Optional[User]:
        logger.debug(f"Fetching user with id: {user_id}")
        try:
            object_id = ObjectId(user_id)
        except (InvalidId, TypeError):
            return None
        document = await self.collection.find_one({"_id": object_id})
        if document:
            document["_id"] = str(document["_id"])
            return User.parse_obj(document)
        return None

    async def update_user(self, user_id: str, user_data: dict) -> Optional[User]:
        try:
            object_id = ObjectId(user_id)
        except (InvalidId, TypeError):
            return None
        update_command = {"$set": {**user_data, "updated_at": datetime.utcnow()}}
        document = await self.collection.find_one_and_update(
            {"_id": object_id},
            update_command,
            return_document=True
        )
        if document:
            document["_id"] = str(document["_id"])
            return User.parse_obj(document)
        return None

    async def delete_user(self, user_id: str) -> bool:
        try:
            object_id = ObjectId(user_id)
        except (InvalidId, TypeError):
            return False
        result = await self.collection.delete_one({"_id": object_id})
        return result.deleted_count > 0

    async def get_user_by_username(self, username: str) -> Optional[User]:
        document = await self.collection.find_one({"username": username})
        if document:
            document["_id"] = str(document["_id"])
            return User.parse_obj(document)
        return None

    async def list_users(self) -> List[User]:
        users = []
        async for document in self.collection.find():
            document["_id"] = str(document["_id"])
            users.append(User.parse_obj(document))
        return users