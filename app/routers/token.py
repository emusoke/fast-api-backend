from fastapi import APIRouter
from .. import crud, models, schemas
from sqlalchemy.orm import Session
from typing import Union, List
from fastapi import Depends, FastAPI, HTTPException, status
from ..database import get_db
from ..dependencies import authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

SECRET_KEY = "7d5492df2b93a8ac7510efaa21dc6d5e972d3a4eb859b021aca2b87a3185f541"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(tags=['Authentication'])


@router.post("/token", response_model = schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(username=form_data.username,password=form_data.password,db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}