from pydantic import BaseModel


class UserUpdateRequest(BaseModel):
    fullname: str | None = None
    avatar: str | None = None

