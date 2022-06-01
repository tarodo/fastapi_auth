from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: EmailStr = Field(index=True, sa_column_kwargs={"unique": True})
    password: str = Field(...)
    is_admin: bool = Field(default=False, nullable=False)


class UserBase(SQLModel):
    email: EmailStr = Field(...)
    is_admin: bool = Field(default=False)


class UserIn(UserBase):
    password: str = Field(...)


class UserOut(UserBase):
    id: int = Field(...)
