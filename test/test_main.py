import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool 
from datetime import datetime

from src.main import app, get_db
from src.models import User, UserCreate, UserRead, UserUpdate, Follow


'''
    Fixtures
'''
@pytest.fixture(name="db")
def db_fixture():
    # use in-memory database
    connect_args = {"check_same_thread": False}
    engine = create_engine("sqlite://", connect_args=connect_args, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db: 
        yield db
        db.rollback()

@pytest.fixture(name="client")
def client_fixture(db: Session):
    # override `get_db` dependecy
    def get_db_override():
        return db

    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


'''
    Users API Tests
'''

def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "users microsevice"}


#