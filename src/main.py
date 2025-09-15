from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(root_path="/frontend-api")

user_router = APIRouter(prefix="", tags=['users'])


@user_router.get("/users/me")
def get_user_info():
    return {
        "email": "example@example.com",
        "isActive": True,
        "profileId": "1",
        "registeredAt": "2025-06-15T18:29:56+00:00",
        "updatedAt": "2025-06-15T18:29:56+00:00",
        "username": "user123",
    }


app.include_router(user_router)

app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

app.mount("/", StaticFiles(directory="frontend", html=True), name="site")
