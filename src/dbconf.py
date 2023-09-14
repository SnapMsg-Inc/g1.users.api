from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

USERS_DB_URL = "postgresql://snapmsg:1234@users-db:5432/usersdb"

engine = create_engine(USERS_DB_URL)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
conn = engine.connect()
