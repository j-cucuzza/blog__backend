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
    review as review_model,
    cuisine as cuisine_model
    )

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

    
###########
# REVIEWS #
###########
@router.post("/create/", response_model=review_model.ReviewPublic)
def create_review(token: Annotated[str, Depends(oauth2_scheme)],
    review: review_model.ReviewCreate,
    session: SessionDep,
    claims: dict = Depends(auth_util.verify_token)):
    db_review = review_model.Review.model_validate(review)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

@router.get("/all/", response_model=list[review_model.ReviewPublicWithCuisine])
def read_reviews(session: SessionDep):
    reviews = session.exec(
        select(review_model.Review).order_by(review_model.Review.visited.desc(), 
            review_model.Review.rating.desc(), review_model.Review.name)
    )
    return reviews

@router.get("/{review_id}", response_model=review_model.ReviewPublic)
def read_review(review_id: int, session: SessionDep):
    review = session.get(review_model.Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.patch("/{review_id}", response_model=review_model.ReviewPublic)
def update_review(token: Annotated[str, Depends(oauth2_scheme)],
    review_id: int,
    review: review_model.ReviewUpdate,
    session: SessionDep,
    claims: dict = Depends(auth_util.verify_token)):
    review_db = session.get(review_model.Review, review_id)
    if not review_db:
        raise HTTPException(status_code=404, detail="Review not found")
    review_data = review.model_dump(exclude_unset=True)
    review_db.sqlmodel_update(review_data)
    session.add(review_db)
    session.commit()
    session.refresh(review_db)
    return review_db

@router.delete("/{review_id}")
def delete_review(token: Annotated[str, Depends(oauth2_scheme)],
    review_id: int,
    session: SessionDep,
    claims: dict = Depends(auth_util.verify_token)):
    review = session.get(review_model.Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    session.delete(review)
    session.commit()
    return {"ok": True}

@router.get("/all/html", response_class=HTMLResponse)
def get_recipes_html(session: SessionDep, cuisine: str = "all"):
    if cuisine == "all":
        statement = select(review_model.Review).order_by(review_model.Review.visited.desc(),
            review_model.Review.rating.desc(), review_model.Review.name)
    else:
        statement = select(review_model.Review).where(review_model.Review.cuisine_id == int(cuisine)).order_by(review_model.Review.visited.desc(), 
            review_model.Review.rating.desc(), review_model.Review.name)
    results = session.exec(statement).all()
    
    if not results:
        return ""

    html = gen_html.generate_reviews(results)

    return html

    
############
# CUISINES #
############
@router.post("/cuisine", response_model=cuisine_model.CuisinePublic)
def create_Cuisine(token: Annotated[str, Depends(oauth2_scheme)],
    cuisine: cuisine_model.CuisineCreate,
    session: SessionDep,
    claims: dict = Depends(auth_util.verify_token)):
    db_cuisine = cuisine_model.Cuisine.model_validate(cuisine)
    session.add(db_cuisine)
    session.commit()
    session.refresh(db_cuisine)
    return db_cuisine

@router.get("/cuisines/", response_model=list[cuisine_model.CuisinePublic])
def read_Cuisines(
    session: SessionDep,
):
    cuisines = session.exec(select(cuisine_model.Cuisine).order_by(cuisine_model.Cuisine.name)).all()
    return cuisines


@router.delete("/cuisine/{cuisine_id}")
def delete_cuisine(token: Annotated[str, Depends(oauth2_scheme)],
    cuisine_id: int,
    session: SessionDep,
    claims: dict = Depends(auth_util.verify_token)):
    cuisine = session.get(cuisine_model.Cuisine, cuisine_id)
    if not cuisine:
        raise HTTPException(status_code=404, detail="Cuisine not found")
    session.delete(cuisine)
    session.commit()
    return {"ok": True}

@router.get("/cuisines/html", response_class=HTMLResponse)
def get_tags_html(session: SessionDep):
    cuisines = session.exec(select(cuisine_model.Cuisine).order_by(cuisine_model.Cuisine.name))
    html = gen_html.generate_tags(cuisines)

    return html