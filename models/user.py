from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    username: str

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password: str

class UserPublic(UserBase):
    id: int

class UserCreate(UserBase):
    password: str