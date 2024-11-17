from sqlmodel import Field, SQLModel

class CuisineBase(SQLModel):
    name: str = Field(index=True)

class Cuisine(CuisineBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class CuisinePublic(CuisineBase):
    id: int

class CuisineCreate(CuisineBase):
    pass

class CuisineUpdate(CuisineBase):
    name: str | None = None