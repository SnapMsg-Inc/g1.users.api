from fastapi.testclient import TestClient 
from sqlmodel import Session

from .conftest import sample_user
from src.models import User, UserPublic
from src.crud import create_user

'''
    TEST GET /users/{uid}
'''

def test_read_user_uid_in_path(db: Session, client: TestClient):
    # Arrange 
    test_user = sample_user() 
    db.add(test_user)
    db.commit()

    # Act
    res = client.get("/users/unique_uid/")
    user_response = res.json()

    # Assert
    assert res.status_code == 200
    assert user_response == test_user.model_dump()


def test_read_user_uid_in_path_twice(db, client):
    # Arrange 
    test_user = sample_user()
    db.add(test_user)
    db.commit()

    res = client.get(f"/users/{test_user.uid}")
    user_response = res.json()
    
    assert res.status_code == 200
    assert user_response == test_user.model_dump()

    res = client.get(f"/users/{test_user.uid}")
    
    assert res.status_code == 200
    assert user_response == test_user.model_dump()



def test_read_user_uid_in_path_not_found(db, client):
    # Act
    res = client.get(f"/users/some_uid")
    
    # Assert
    assert res.status_code == 404 


'''
    TEST GET /users
'''

def test_read_users_filter_by_uid(db, client):
    # Arrange 
    test_user = sample_user()
    db.add(test_user)
    db.commit()

    user_public = UserPublic.from_orm(test_user)
    
    # Act
    res = client.get(f"/users?uid={test_user.uid}")
    users = res.json()
    
    # Assert
    assert res.status_code == 200
    assert users[0] == user_public


def test_read_users_filter_by_email(db, client):
    # Arrange 
    test_user = sample_user()
    db.add(test_user)
    db.commit()

    user_public = UserPublic.from_orm(test_user)
    
    # Act
    res = client.get(f"/users?email={test_user.email}")    
    users = res.json()

    # Assert
    assert res.status_code == 200
    assert users[0] == user_public


def test_read_users_filter_by_nick(db, client):
    # Arrange 
    test_user = sample_user()
    db.add(test_user)
    db.commit()

    user_public = UserPublic.from_orm(test_user)
    
    # Act
    res = client.get(f"/users?nick={test_user.nick}")
    users = res.json()
    
    # Assert
    assert res.status_code == 200
    assert users[0] == user_public


def test_read_users_filter_by_alias(db, client):
    # Arrange 
    test_user = sample_user()
    db.add(test_user)
    db.commit()

    user_public = UserPublic.from_orm(test_user)
    
    # Act
    res = client.get(f"/users?alias={test_user.alias}")
    users = res.json()
    
    # Assert
    assert res.status_code == 200
    assert users[0] == user_public


