from fastapi import APIRouter, Depends, HTTPException, status, Form
from user_service.app.application.user_manager import UserManager
from user_service.app.core.dependencies import get_user_manager, get_current_user, get_admin_user
from user_service.app.domain.models.user import UserView, UserCreate, UserUpdate, User, UserRole

router = APIRouter(prefix="/api/users", tags=["users"])


# Новый эндпоинт: список всех пользователей (только для админов)
@router.get("/", response_model=list[UserView])
async def list_users(
    admin_user: User = Depends(get_admin_user),  # Заменяем current_user
    manager: UserManager = Depends(get_user_manager)
) -> list[UserView]:
    users = await manager.list_users()
    return users

@router.get("/me", response_model=UserView)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> UserView:
    return current_user

# Новый эндпоинт: обновление пароля
@router.post("/me/password", response_model=dict)
async def change_password(
    current_password: str = Form(...),
    new_password: str = Form(...),
    current_user: User = Depends(get_current_user),
    manager: UserManager = Depends(get_user_manager)
) -> dict:
    user = await manager.authenticate_user(current_user.username, current_password)
    if not user:
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    update_data = UserUpdate(password=new_password)
    await manager.update_user(current_user.id, update_data)
    return {"message": "Password updated successfully"}

# Получение пользователя по ID (только для администраторов)
@router.get("/{user_id}", response_model=UserView)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    manager: UserManager = Depends(get_user_manager)
) -> UserView:
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user")
    return await manager.get_user(user_id)


# Обновление пользователя (себя или для админа)
@router.put("/{user_id}", response_model=UserView)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    manager: UserManager = Depends(get_user_manager)
) -> UserView:
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    # Ограничиваем изменение роли только для админов
    if user_update.role and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can change roles")
    return await manager.update_user(user_id, user_update)


# Удаление пользователя (себя или для админа)
@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    manager: UserManager = Depends(get_user_manager)
) -> dict:
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    success = await manager.delete_user(user_id)
    return {"success": success}


# Новый эндпоинт: сброс пароля (для админов или через email в будущем)
@router.post("/{user_id}/reset-password", response_model=dict)
async def reset_password(
    user_id: str,
    new_password: str = Form(...),
    current_user: User = Depends(get_current_user),
    manager: UserManager = Depends(get_user_manager)
) -> dict:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    update_data = UserUpdate(password=new_password)
    await manager.update_user(user_id, update_data)
    return {"message": "Password reset successfully"}