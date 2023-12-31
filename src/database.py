from sqlmodel import SQLModel, create_engine
from . import models 

USERS_DB_URL = "postgresql://snapmsg:1234@users-db:5432/usersdb"

# USERS_DB_URL = "sqlite:////usr/snapmsg-users/db/users.db"
engine = create_engine(USERS_DB_URL, echo=True)

def init_tables():
	SQLModel.metadata.create_all(engine)
