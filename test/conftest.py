import os
import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool 
from src.main import app, get_db
from src.models import User, Follow, UserCreate



@pytest.fixture(name="db")
def db():
    TEST_DB_URL = os.environ.get("TEST_DB_URL")

    if TEST_DB_URL is None:
        TEST_DB_URL = "postgresql://test:1234@postgres/testdb"
    engine = create_engine(TEST_DB_URL)#, connect_args=connect_args)
    SQLModel.metadata.create_all(engine)

    with Session(engine, autoflush=True) as db:
        yield db
        db.rollback()
    

@pytest.fixture(name="cleanup_db")
def cleanup_db(db: Session):
    yield 
    db.rollback()
    db.execute(User.__table__.delete())
    db.execute(User.__table__.delete())
    db.commit()


@pytest.fixture(name="client")
def client(db: Session):
    def get_db_override():
        return db

    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app, raise_server_exceptions=False)
    yield client
    app.dependency_overrides.clear()


def sample_user():
    return User(
        uid="unique_uid",
        email="john@example.com",
        nick="eljuancho",
        fullname="John",
        alias="Juan Bostero",
        birthdate="1999-01-01",
        zone={"latitude":1.00000, "longitude":0.54},
        interests=["music", "movies"],
    )


def sample_create_user():
    return UserCreate(
        fullname="John", 
        email="john@example.com", 
        birthdate="1990-01-01",
        nick="eljuancho", 
        alias="Juan Bostero", 
        zone={"latitude":10.00, "longitude":0.00},  
        interests=["music", "movies"],
        pic="someurl"	
    )


