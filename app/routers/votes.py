from fastapi import APIRouter
from .. import crud, models, schemas
from sqlalchemy.orm import Session
from typing import Union, List
from fastapi import Depends, FastAPI, HTTPException, status
from ..database import get_db
from ..dependencies import get_current_active_user, oauth2_scheme, get_password_hash, get_current_user

router = APIRouter(
    prefix="/vote",
    tags = ['votes']
)

@router.post("/like")
def like_a_post(post_id: schemas.Like,db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    post = crud.get_post_by_id(db=db,id=post_id.post_id)
    if post is None:
        raise HTTPException(status_code = 400, detail = "This post does not exist")
    like = crud.get_like(db=db,user_id=current_user.id,post_id=post_id.post_id)
    if like:
        raise HTTPException(status_code = 400, detail = "Already liked this post")
    return crud.like_post(db=db, post_id=post_id.post_id,user_id=current_user.id)

@router.post("/unlike")
def unlike_a_post(post_id: schemas.Like,db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    post = crud.get_post_by_id(db=db,id=post_id.post_id)
    if post is None:
        raise HTTPException(status_code = 400, detail = "This post does not exist")
    like = crud.get_like(db=db,user_id=current_user.id,post_id=post_id.post_id)
    if like is None:
        raise HTTPException(status_code = 400, detail = "User did not previously like post")
    return crud.unlike_post(db=db, post_id=post_id.post_id,user_id=current_user.id)