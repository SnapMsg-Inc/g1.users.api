from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

USERS_DB_URL = "postgresql://okteto:okteto@localhost:5432/users-db"

engine = create_engine(USERS_DB_URL)
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

