from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    name: str
    full_name: str | None = None
    password: str
