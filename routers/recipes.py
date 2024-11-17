from typing import Annotated
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, Query
from database import SessionDep, oauth2_scheme

from models import (
    recipe as recipe_model,
    tag as tag_model
)

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)


###########
# RECIPES #
###########
@router.post("/create/", response_model=recipe_model.RecipePublic)
def create_recipe(token: Annotated[str, Depends(oauth2_scheme)], recipe: recipe_model.RecipeCreate, session: SessionDep):
    db_recipe = recipe_model.Recipe.model_validate(recipe)
    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)
    return db_recipe

@router.get("/all/", response_model=list[recipe_model.RecipePublicWithTag])
def read_recipes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    recipes = session.exec(select(recipe_model.Recipe).offset(offset).limit(limit)).all()
    return recipes

@router.get("/{recipe_id}", response_model=recipe_model.RecipePublic)
def read_recipe(recipe_id: int, session: SessionDep):
    recipe = session.get(recipe_model.Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.patch("/{recipe_id}", response_model=recipe_model.RecipePublic)
def update_recipe(token: Annotated[str, Depends(oauth2_scheme)], recipe_id: int, recipe: recipe_model.RecipeUpdate, session: SessionDep):
    recipe_db = session.get(recipe_model.Recipe, recipe_id)
    if not recipe_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    recipe_data = recipe.model_dump(exclude_unset=True)
    recipe_db.sqlmodel_update(recipe_data)
    session.add(recipe_db)
    session.commit()
    session.refresh(recipe_db)
    return recipe_db

@router.delete("/{recipe_id}")
def delete_recipe(token: Annotated[str, Depends(oauth2_scheme)], recipe_id: int, session: SessionDep):
    recipe = session.get(recipe_model.Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    session.delete(recipe)
    session.commit()
    return {"ok": True}


########
# TAGS #
########
@router.post("/tag", response_model=tag_model.TagPublic)
def create_tag(token: Annotated[str, Depends(oauth2_scheme)], tag: tag_model.TagCreate, session: SessionDep):
    db_tag = tag_model.Tag.model_validate(tag)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag

@router.post("/tags/", response_model=list[tag_model.TagPublic])
def read_tags(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    tags = session.exec(select(tag_model.Tag).offset(offset).limit(limit)).all()
    return tags
