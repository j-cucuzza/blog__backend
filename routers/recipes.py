from typing import Annotated
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from database import SessionDep, oauth2_scheme

from utils import (
    generate_html as gen_html,
    auth_util as auth_util
)

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
def create_recipe(token: Annotated[str, Depends(oauth2_scheme)],
    recipe: recipe_model.RecipeCreate,
    session: SessionDep,
    claims: dict = Depends(auth_util.verify_token)):
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
def update_recipe(token: Annotated[str, Depends(oauth2_scheme)],
    recipe_id: int,
    recipe: recipe_model.RecipeUpdate,
    session: SessionDep,
    claims: dict = Depends(auth_util.verify_token)):
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
def delete_recipe(token: Annotated[str, Depends(oauth2_scheme)],
    recipe_id: int,
    session: SessionDep,
    claims: dict = Depends(auth_util.verify_token)):
    recipe = session.get(recipe_model.Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    session.delete(recipe)
    session.commit()
    return {"ok": True}

#  response_model=list[recipe_model.RecipePublicWithTag]
@router.get("/all/html", response_class=HTMLResponse)
def get_recipes_html(session: SessionDep, tag: str = "all"):
    if tag == "all":
        statement = select(recipe_model.Recipe)
    else:
        statement = select(recipe_model.Recipe).where(recipe_model.Recipe.tag_id == int(tag))
    results = session.exec(statement).all()
    
    if not results:
        return ""

    html = gen_html.generate_recipes(results)

    return html

@router.get("/one/html", response_class=HTMLResponse)
def get_recipe_html(session: SessionDep, id: int = 0):
    statement = select(recipe_model.Recipe).where(recipe_model.Recipe.id == int(id))
    recipe = session.exec(statement).all()[0]

    html = ""
    
    if not recipe:
        html = gen_html.generate_error_html()
        return html
    
    html = gen_html.generate_recipe(recipe)

    response = HTMLResponse(content=html)
    response.headers["X-Page-Title"] = recipe.name
    response.headers["X-Page-Description"] = f"{recipe.servings} servings, {recipe.calories} calories, {recipe.protein}g protein"
    return response

########
# TAGS #
########
@router.post("/tag", response_model=tag_model.TagPublic)
def create_tag(token: Annotated[str, Depends(oauth2_scheme)],
    tag: tag_model.TagCreate,
    session: SessionDep,
    claims: dict = Depends(auth_util.verify_token)):
    db_tag = tag_model.Tag.model_validate(tag)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag

@router.get("/tags/", response_model=list[tag_model.TagPublic])
def read_tags(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    tags = session.exec(select(tag_model.Tag).offset(offset).limit(limit)).all()
    return tags

@router.delete("/tag/{tag_id}")
def delete_tag(token: Annotated[str, Depends(oauth2_scheme)],
    tag_id: int, session: SessionDep,
    claims: dict = Depends(auth_util.verify_token)):
    tag = session.get(tag_model.Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    session.delete(tag)
    session.commit()
    return {"ok": True}

@router.get("/tags/html", response_class=HTMLResponse)
def get_tags_html(session: SessionDep):
    tags = session.exec(select(tag_model.Tag))
    html = gen_html.generate_tags(tags)

    return html