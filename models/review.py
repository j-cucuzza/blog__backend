from sqlmodel import SQLModel, Field, Relationship
from models import cuisine as cuisine_model

class ReviewBase(SQLModel):
    name: str = Field(index=True)
    address: str | None = Field(default=None, index=True)
    visited: bool = Field(default=False, index=True)
    rating: int | None = Field(default=None, index=True)
    notes: str | None = Field(default=None)

class Review(ReviewBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cuisine_id: int | None = Field(default=None, foreign_key="cuisine.id")
    cuisine: cuisine_model.Cuisine | None = Relationship()

class ReviewPublic(ReviewBase):
    id: int

class ReviewCreate(ReviewBase):
    cuisine_id: int

class ReviewUpdate(ReviewBase):
    name: str | None = None
    address: str | None = None
    visited: bool | None = None
    rating: int | None = None
    notes: str | None = None
    cuisine_id: int | None = None

class ReviewPublicWithCuisine(ReviewPublic):
    cuisine: cuisine_model.CuisinePublic | None = None

