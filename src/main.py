from datetime import datetime

from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(root_path="/frontend-api")

user_router = APIRouter(prefix="", tags=['users'])


class UserModel(BaseModel):
    email: str
    isActive: bool
    profileId: int
    registeredAt: datetime
    updatedAt: datetime
    username: str


@user_router.get("/users/me", response_model=UserModel)
def get_user_info():
    data = {
        "email": "example@example.com",
        "isActive": True,
        "profileId": "1",
        "registeredAt": "2025-06-15T18:29:56+00:00",
        "updatedAt": "2025-06-15T18:29:56+00:00",
        "username": "user123",
    }
    return data


app.include_router(user_router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="site")

app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
