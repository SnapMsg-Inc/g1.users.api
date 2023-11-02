from fastapi.testclient import TestClient
from sqlmodel import Session

from src.models import User, UserCreate
from .conftest import sample_user 


def test_delete_user(db: Session, client: TestClient):
    # Arrange
    test_user = sample_user()
    db.add(test_user)
    db.commit()

    # Act
    res = client.delete(f"/users/{test_user.uid}")    

    # Assert
    assert res.status_code == 200
    assert db.get(User, test_user.uid) is None

    
def test_delete_user_does_not_exist(db: Session, client: TestClient):
    # Act
    res = client.delete(f"/users/some_uid")    

    # Assert
    assert res.status_code == 404


def test_delete_user_does_not_delete_other_user(db: Session, client: TestClient):
    # Arrange
    test_user_0 = sample_user()
    db.add(test_user_0)

    # uid, nick and email are unique
    test_user_1 = sample_user()
    test_user_1.uid = "different_uid"
    test_user_1.nick = "different_nick"
    test_user_1.email = "different_email"
    db.add(test_user_1)

    db.commit()

    # Act
    res = client.delete(f"/users/{test_user_0.uid}")    

    # Assert
    assert res.status_code == 200
    assert db.get(User, test_user_1.uid) == test_user_1



