from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:magical_password@postgres:5432"

#TODO Make a config file that will connect to different environments
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:magical_password@localhost:5432"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:magical_password@database-1.czliip20htmb.af-south-1.rds.amazonaws.com:5432"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()