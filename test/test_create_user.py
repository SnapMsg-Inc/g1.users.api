from fastapi.testclient import TestClient 
from sqlmodel import Session

from .conftest import sample_create_user 
from src.models import User, UserCreate


def test_create_user_happy_path(db: Session, client: TestClient):
    # Arrange
    uid = "unique_id"
    test_user = sample_create_user()

    # Act
    res = client.post(f"/users/{uid}", json=test_user.model_dump())

    # Assert
    db.refresh()
    db_user = db.get(User, uid)
    assert db_user is not None

    db_user = UserCreate.from_orm(db_user)

    assert res.status_code == 201
    assert db_user == test_user
    

def test_create_user_uid_already_exists(client: TestClient):
    # Arrange
    uid = "unique_id"
    test_user = sample_create_user()
    res = client.post(f"/users/{uid}", json=test_user.model_dump())
    assert res.status_code == 201
    # change nick and email
    test_user.nick = "pedro"
    test_user.email= "pedro@pedro.com"
 
    # Act
    res = client.post(f"/users/{uid}", json=test_user.model_dump())

    # Assert
    assert res.status_code == 409


def test_create_user_email_already_exists(client: TestClient):
    # Arrange
    uid = "unique_id_0"
    test_user = sample_create_user()
    client.post(f"/users/{uid}", json=test_user.model_dump())

    # change uid and nick
    uid = "unique_id_1"
    test_user.nick = "juan"
 
    # Act
    res = client.post(f"/users/{uid}", json=test_user.model_dump())

    # Assert
    assert res.status_code == 409


def test_create_user_nick_already_exists(client: TestClient):
    # Arrange
    uid = "unique_id_0"
    test_user = sample_create_user()
    client.post(f"/users/{uid}", json=test_user.model_dump())

    # change uid and nick
    uid = "unique_id_1"
    test_user.email = "juancho@example.com"
 
    # Act
    res = client.post(f"/users/{uid}", json=test_user.model_dump())

    # Assert
    assert res.status_code == 409

    
