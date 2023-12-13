import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool 
from src.main import app, get_db
from src.models import User, UserCreate


@pytest.fixture(name="db")
def db():
    # use in-memory database
    print("Setting up db")
    connect_args = {"check_same_thread": False}
    engine = create_engine("sqlite://", connect_args=connect_args, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db: 
        yield db
        db.rollback()

@pytest.fixture(name="client")
def client(db: Session):
    # override `get_db` dependecy
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


