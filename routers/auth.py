import jwt
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from utils.auth_util import (
    verify_password,
    encrypt_password,
    decode_token,
    generate_token
)

from models import token as token_model
from models import user as user_model
from database import engine, oauth2_scheme

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/signup", response_model=user_model.UserPublic)
async def create_user(
    user: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    try:
        with Session(engine) as db:
            existing_user = (
                db.query(user_model.User)
                .filter(user_model.User.username == user.username)
                .first()
            )
            if not existing_user:
                user.password = encrypt_password(user.password)
                db_user = user_model.User.model_validate(user)
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                return db_user
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",

        ) from e
    raise HTTPException(
        status_code=409,
        detail="User already exists"
    )

@router.post("/token", response_model=token_model.Token)
async def login_for_token(
    token: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    with Session(engine) as db:
        db_user = (
            db.query(user_model.User)
            .filter(user_model.User.username == token.username)
            .first()
        )
        if not db_user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(token.password, db_user.password):
            raise HTTPException(
                status_code=404,
                detail="Incorrect password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        access_token = generate_token(username=token.username)
        return token_model.Token(access_token=access_token, token_type="bearer")
        
@router.get("/me")
async def read_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        token_data = token_model.TokenData(username=username)
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=404,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    with Session(engine) as db:
        db_user = (
            db.query(user_model.User)
            .filter(user_model.User.username == token_data.username)
            .first()
        )
        if db_user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )
        return db_user