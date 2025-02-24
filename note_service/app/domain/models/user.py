"""
Модель доменного уровня для пользователя.
"""

from pydantic import BaseModel

class User(BaseModel):
    """
    Сущность пользователя в системе.
    """
    id: str
    username: str
