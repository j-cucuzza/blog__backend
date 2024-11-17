import jwt
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine
from fastapi import FastAPI
from routers import auth, recipes, reviews
from database import create_db_and_tables

app = FastAPI()
routers = [
    auth.router,
    recipes.router,
    reviews.router,
]
for router in routers:
    app.include_router(router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
