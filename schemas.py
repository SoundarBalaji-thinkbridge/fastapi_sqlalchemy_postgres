from pydantic import BaseModel, EmailStr,Field


class UserBase(BaseModel):
    email: EmailStr
    name: str


class User(UserBase):
    id: int = Field(None, alias='id')
    name: str = None
    email: str = None

    class Config:
        orm_mode = True

