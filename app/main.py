from typing import Union, List
from datetime import datetime, timedelta
import uvicorn

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from .routers import users, posts, token, votes

from . import crud, models, schemas
from .database import SessionLocal, engine

# Line below creates tables using SQL Alchemy instead of alembic
models.Base.metadata.create_all(bind=engine)



#Origin of our front end application
origins = [
    'http://localhost:4200'
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(posts.router)
app.include_router(token.router)
app.include_router(votes.router)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)