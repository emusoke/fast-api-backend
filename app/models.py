#This script will host our SQL Alchemy Models
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, Date, TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base
# from database import Base
import psycopg2
from psycopg2.extras import RealDictCursor
import sys
sys.setrecursionlimit(10000)

followers = Table(
    "user_follower",
    Base.metadata,
    Column("follower_id",Integer,ForeignKey("users.id"),primary_key=True),
    Column("following_id",Integer,ForeignKey("users.id"),primary_key=True),
)

class Like(Base):
    __tablename__ = "likes"
    user_id = Column("user_id", Integer,ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
    post_id = Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"),primary_key=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    bio = Column(String)
    is_active = Column(Boolean, default=True)
    posts = relationship("Post", back_populates="author")
    following = relationship(
        "User",
        secondary = followers,
        primaryjoin=id == followers.c.follower_id,
        secondaryjoin=id == followers.c.following_id,
        lazy='dynamic',
        backref="followers"
    )
    likes = relationship("Like")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    post = Column(String, index = True)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    author = relationship("User", back_populates="posts")
    
    