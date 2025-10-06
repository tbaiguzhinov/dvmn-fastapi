from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class UserModel(BaseModel):
    email: EmailStr
    is_active: bool
    profile_id: int
    registered_at: datetime
    updated_at: datetime
    username: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "email": "example@example.com",
                    "isActive": True,
                    "profileId": 1,
                    "registeredAt": "2025-06-15T18:29:56+00:00",
                    "updatedAt": "2025-06-15T18:29:56+00:00",
                    "username": "user123",
                },
            ],
        },
    )
