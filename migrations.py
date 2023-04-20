import app.models
from app.database import engine
import os

# app.models.Base.metadata.create_all(bind=engine)

# print("I am a migrations script")

from alembic.config import Config
from alembic import command

alembic_cfg = Config("alembic.ini")
command.stamp(alembic_cfg, "head")
# command.upgrade(alembic_cfg, "head")
