#This will hold our pydantic models
from typing import List, Union, Optional
from pydantic import BaseModel
from datetime import datetime

class FollowUser(BaseModel):
    followed_email: str

class PostID(BaseModel):
    post_id: int

class PostBase(BaseModel):
    post: str

class Like(BaseModel):
    post_id: int

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass

class PostEdit(PostBase):
    id: int

class UserBase(BaseModel):
    email: str
    
    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    # author_id: int
    author: UserBase
    created_date: datetime
    
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    like_count: Optional[int] = 0

    
    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    bio: str

class User(UserBase):
    # bio: Optional[str] = None
    # posts: List[Post]
    bio: Optional[str] = None
    likes: List[Like]

    class Config:
        orm_mode = True

class UserOut(UserBase):
    # posts: List[PostOut]
    likes: List[Like]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None