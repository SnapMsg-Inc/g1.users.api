import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool 
from src.main import app, get_db
from src.models import User, Follow, UserCreate


def get_engine():
    TEST_DB_URL = "postgresql://test:1234@postgres/testdb"
    engine = create_engine(TEST_DB_URL)#, connect_args=connect_args)
    SQLModel.metadata.create_all(engine)
    return engine
 

@pytest.fixture(name="db_no_rollback")
def db_no_rollback():
    with Session(get_engine(), autoflush=True) as db_no_rollback:
        yield db_no_rollback
    

@pytest.fixture(name="db")
def db(db_no_rollback: Session):
    yield db_no_rollback
    db_no_rollback.execute(User.__table__.delete())
    db_no_rollback.execute(Follow.__table__.delete())
    db_no_rollback.commit()
    


@pytest.fixture(name="client")
def client(db_no_rollback: Session):
    def get_db_override():
        return db_no_rollback

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


