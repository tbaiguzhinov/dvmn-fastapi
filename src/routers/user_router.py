from fastapi import APIRouter

from models.user_models import UserModel

user_router = APIRouter(prefix="/users", tags=['users'])


@user_router.get("/me", response_model=UserModel, summary='Получить учетные данные пользователя')
async def get_user_info():
    data = {
        "email": "google@google.com",
        "isActive": True,
        "profileId": "1",
        "registeredAt": "2025-06-15T18:29:56+00:00",
        "updatedAt": "2025-06-15T18:29:56+00:00",
        "username": "user123",
    }
    return data
