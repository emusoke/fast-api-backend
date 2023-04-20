from fastapi import APIRouter
from .. import crud, models, schemas
from sqlalchemy.orm import Session
from typing import Union, List
from fastapi import Depends, FastAPI, HTTPException, status
from ..database import get_db
from ..dependencies import get_current_active_user, oauth2_scheme, get_password_hash, get_current_user

router = APIRouter(
    prefix="/users",
    tags = ['users']
)

@router.get("/", response_model = List[schemas.User])
def read_user(skip: int = 0, limit = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db=db,skip=skip,limit=limit)
    return users

@router.post("/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # First Check of the user exists
    db_user = crud.get_user_by_email(db=db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    user.password = get_password_hash(user.password)
    crud.create_user(db=db, user=user)
    return {"detail": "Successfully Registered User"}

@router.get("/my_profile", response_model = schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

# @router.get("/{user_id}", response_model = schemas.User)
# def read_user(user_id: str, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme),):
#     db_user = crud.get_user(db=db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=400, detail = "This user does not exist")
#     return db_user

@router.get("/following", response_model = List[schemas.User])
def get_current_users_following(current_user: models.User = Depends(get_current_active_user),db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=current_user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail = "This is not a valid user")
    return db_user.following.all()

@router.get("/followers", response_model = List[schemas.User])
def get_current_users_followers(current_user: models.User = Depends(get_current_active_user),db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=current_user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail = "This is not a valid user")
    return db_user.followers

@router.get("/{email}", response_model = schemas.User)
def get_user_by_username(email: str, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme),):
    db_user = crud.get_user_by_email(db=db, email=email)
    if db_user is None:
        raise HTTPException(status_code=400, detail = "This user does not exist")
    return db_user


@router.get("/{email}/following", response_model = List[schemas.User])
def get_following(email: str, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme),):
    db_user = crud.get_user_by_email(db=db, email=email)
    if db_user is None:
        raise HTTPException(status_code=400, detail = "This is not a valid user")
    return db_user.following.all()

@router.get("/{email}/followers", response_model = List[schemas.User])
def get_users_followers(email: str, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme),):
    db_user = crud.get_user_by_email(db=db, email=email)
    if db_user is None:
        raise HTTPException(status_code=400, detail = "This is not a valid user")
    return db_user.followers



@router.post("/follow", response_model = schemas.User)
def follow_user(followed: schemas.User, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    crud.follow_user(db=db,follower_id=current_user.id,followed_email= followed.email)
    return get_user_by_username(email=followed.email,db=db)

@router.post("/unfollow", response_model = schemas.User)
def follow_user(followed: schemas.User, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    crud.unfollow_user(db=db,follower_id=current_user.id,followed_email= followed.email)
    return get_user_by_username(email=followed.email,db=db)

@router.put("/settings", response_model = schemas.User)
def update_users_profile(new_bio: schemas.UserUpdate, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_active_user)):
    return crud.update_user_bio(db=db,email=current_user.email, new_bio=new_bio.bio)
    # return {"message": "Profile Updated!"}