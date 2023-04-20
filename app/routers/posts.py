from fastapi import APIRouter
from .. import crud, models, schemas
from sqlalchemy.orm import Session
from typing import Union, List
from fastapi import Depends
from ..database import get_db
from ..dependencies import oauth2_scheme, get_current_user
from fastapi import Depends, HTTPException

router = APIRouter(
    prefix="/posts",
    tags = ['posts']
)


@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_posts = crud.get_posts(db=db)
    return db_posts

@router.get("/timeline", response_model = List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    current_user_id = current_user.id
    return crud.get_timeline(db=db,follower_id=current_user_id)

@router.get("/{email}", response_model = List[schemas.PostOut])
def read_users_posts(email: str, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme),):
    db_user = crud.get_user_by_email(db=db, email=email)
    if db_user is None:
        raise HTTPException(status_code=400, detail = "This user does not exist")
    return crud.get_posts_by_username(db=db,email=db_user.email)

@router.post("/", response_model = schemas.Post)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    db_user = crud.get_user(db=db,user_id=current_user.id)
    if db_user is None:
        raise HTTPException(status_code = 400, detail = "This user does not exist")
    return crud.create_user_post(db=db,post=post,user_id=current_user.id)
    

@router.put("/", response_model = schemas.Post)
def edit_post(post: schemas.PostEdit, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    post_detail = crud.get_post_by_id(db=db,id=post.id)

    if post_detail.author_id != current_user.id:
        raise HTTPException(status_code = 400, detail = "Forbidden Request")
    # y = crud.update_user_post(db=db,post=post)
    # print(y)
    return crud.update_user_post(db=db,post=post)

# @router.get("/test", response_model = List[schemas.PostOutTest])
# def get_post_likes(db: Session = Depends(get_db)):
#     return crud.get_post_likes(db=db)

@router.delete("/")
def delete_post(post_id: int,db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    post = crud.get_post_by_id(db=db, id = post_id)
    if post is None:
        raise HTTPException(status_code = 400, detail = "Post does not exist")
    if post.author_id != current_user.id:
        raise HTTPException(status_code = 400, detail = "Forbidden Request")
    response = crud.delete_post(db=db, post_id=post_id)
    return {"Message": response}