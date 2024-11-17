from sqlmodel import Field, SQLModel

class TagBase(SQLModel):
    name: str = Field(index=True)

class Tag(TagBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class TagPublic(TagBase):
    id: int

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    name: str | None = None
