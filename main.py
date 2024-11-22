from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, recipes, reviews
from database import create_db_and_tables

app = FastAPI()
routers = [
    auth.router,
    recipes.router,
    reviews.router,
]

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://localhost:3000",
    "https://localhost:8000",
    "https://www.dippingsauce.net",
    "https://admin.dippingsauce.net",
]

for router in routers:
    app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Page-Title", "X-Page-Description"]
)
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
