from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class UserModel(BaseModel):
    email: str
    is_active: bool
    profile_id: int
    registered_at: datetime
    updated_at: datetime
    username: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
