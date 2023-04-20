from sqlalchemy.orm import Session
from sqlalchemy.sql import func
# import models
# import schemas
from . import models,schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_users_posts(db: Session, user_id: int, skip=0,limit=100):
    return db.query(models.User.posts).filter(models.User.id == user_id)


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email = user.email, hashed_password = user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_bio(db: Session, email: str, new_bio: str):
    user = db.query(models.User).filter(models.User.email == email)#.first()
    user.update({"email": email,"bio": new_bio},synchronize_session=False)
    db.commit()
    return user.first()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    sub_query = (db.query(models.Like.post_id, func.count("*").label("like_count")).group_by(models.Like.post_id).subquery())
    return db.query(models.Post,sub_query.c.like_count).outerjoin(sub_query,models.Post.id==sub_query.c.post_id).all()

def get_posts_by_username(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    sub_query = (db.query(models.Like.post_id, func.count("*").label("like_count")).group_by(models.Like.post_id).subquery())
    return db.query(models.Post,sub_query.c.like_count).filter(models.Post.author_id==user.id).outerjoin(sub_query,models.Post.id==sub_query.c.post_id).all() 


def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), author_id = user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: schemas.PostID):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    post.delete(synchronize_session=False)
    db.commit()
    return "Post Deleted"

def update_user_post(db: Session, post: schemas.PostEdit):
    db_post = db.query(models.Post).filter(models.Post.id == post.id)
    db_post.update(post.dict(),synchronize_session=False)
    db.commit()
    return db_post.first()

def get_post_by_id(db: Session, id: int):
    return db.query(models.Post).filter(models.Post.id == id).first()
    

def is_following(db: Session, follower_id: int, followed_id: int):
    follower = get_user(db = db, user_id=follower_id)
    return follower.following.filter(models.followers.c.following_id == followed_id).count() > 0

def follow_user(db: Session, follower_id: int, followed_email: str):
    follower = get_user(db = db, user_id=follower_id)
    followed = get_user_by_email(db = db, email=followed_email)
    if not is_following(db=db,follower_id=follower_id,followed_id=followed.id):
        follower.following.append(followed)
        db.add(follower)
        db.commit()

def unfollow_user(db: Session, follower_id: int, followed_email: str):
    follower = get_user(db = db, user_id=follower_id)
    followed = get_user_by_email(db = db, email=followed_email)
    if is_following(db=db,follower_id=follower_id,followed_id=followed.id):
        follower.following.remove(followed)
        db.add(follower)
        db.commit()

# def get_timeline(db: Session, follower_id: int):
#     followed_posts = db.query(models.Post).join(
#         models.followers, models.followers.c.following_id == models.Post.author_id
#         ).filter(models.followers.c.follower_id == follower_id)
    
#     user_posts = db.query(models.Post).filter(models.Post.author_id == follower_id)
#     timeline = user_posts.union(followed_posts).order_by(models.Post.created_date.desc())

    
#     return db.query(timeline,sub_query.c.like_count).outerjoin(sub_query,models.Post.id==sub_query.c.post_id).all() 


    # return own.union(followed).order_by(models.Post.created_date.desc()).all()

def get_timeline(db: Session, follower_id: int):
    sub_query = (db.query(models.Like.post_id, func.count("*").label("like_count")).group_by(models.Like.post_id).subquery())
    followed_posts = db.query(models.Post,
                sub_query.c.like_count).join(
                models.followers, models.followers.c.following_id == models.Post.author_id
                ).filter(models.followers.c.follower_id == follower_id).outerjoin(sub_query,models.Post.id==sub_query.c.post_id)

    user_posts = db.query(models.Post,sub_query.c.like_count).filter(
                models.Post.author_id == follower_id
                ).outerjoin(sub_query,models.Post.id==sub_query.c.post_id)


    return followed_posts.union(user_posts).order_by(models.Post.created_date.desc()).all()

def like_post(db: Session, post_id: int, user_id: int):
    like = models.Like(post_id=post_id, user_id=user_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

def unlike_post(db: Session, post_id: int, user_id: int):
    like = db.query(models.Like).filter(models.Like.post_id == post_id, models.Like.user_id == user_id)
    like.delete(synchronize_session=False)
    db.commit()
    return like

def get_like(db: Session, post_id, user_id):
    return db.query(models.Like).filter(models.Like.post_id == post_id, models.Like.user_id == user_id).first()