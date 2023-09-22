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


def test_get_users_one_user(db: Session, client: TestClient):
    db_user = User(
        uid=0,
        email="example@example.com",
        fullname="John Doe",
        nick="eljuancho",
        b_day=datetime (1990, 1, 1),
        
    )
    db.add(db_user)
    db.commit()

    response = client.get("/users")
    users = response.json()

    assert response.status_code == 200

    for user in users:
        #assert user == db_user # ORM magic
        assert user["uid"] == db_user.uid
        assert user["email"] == db_user.email
        assert user["fullname"] == db_user.fullname
        assert user["nick"] == db_user.nick
        assert user["b_day"] == str(db_user.b_day)


def test_create_duplicate_user(db: Session, client: TestClient):
    # Paso 1: Asegurarse de que la base de datos está en un estado conocido
    db.query(User).filter(User.uid == 0).delete()
    db.commit()

    # Paso 2: Crear un usuario usando la API (para probar el endpoint)
    user_data = {
        "email": "example@example.com",
        "fullname": "John Doe",
        "nick": "eljuancho",
        "b_day": "1990-01-01",
    }
    response = client.post("/users/0", json=user_data)
    assert response.status_code == 201  # Cambiado a 200 como en tu ejemplo

    # Paso 3: Intentar crear el mismo usuario nuevamente usando la API
    response = client.post("/users/0", json=user_data)
    assert response.status_code == 400  # Suponiendo que 400 es el código de estado para "usuario ya existe"
    assert "user already exists" in response.json().get("detail", "")
    # Paso 4: Asegurarse de que la base de datos no haya cambiado
    assert db.query(User).count() == 1

def test_create_user_whitout_field(db: Session, client: TestClient):
        user_data = {
        "email": "example@example.com",
        "fullname": "John Doe",
        "nick": "eljuancho",
    }
        response = client.post("/users/0", json=user_data)
        assert response.status_code == 422
