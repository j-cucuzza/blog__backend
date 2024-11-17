from sqlmodel import Field, SQLModel, Relationship
from models import tag as tag_model

class RecipeBase(SQLModel):
    name: str = Field(index=True)
    servings: int | None = Field(default=None, index=True)
    calories: int | None = Field(default=None, index=True)
    protein: int | None = Field(default=None, index=True)
    ingredients: str | None = Field(default=None)
    instructions: str | None = Field(default=None)

class Recipe(RecipeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id")
    tag: tag_model.Tag | None = Relationship()

class RecipePublic(RecipeBase):
    id: int

class RecipeCreate(RecipeBase):
    tag_id: int

class RecipeUpdate(RecipeBase):
    name: str | None = None
    servings: int | None = None
    calories: int | None = None
    protein: int | None = None
    tag_id: int | None = None
    ingredients: str | None = None
    instructions: str | None = None

class RecipePublicWithTag(RecipePublic):
    tag: tag_model.TagPublic | None = None