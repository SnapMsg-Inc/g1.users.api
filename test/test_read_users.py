import pytest

from fastapi import TestClient 
from pydantic import ValidationError
from src.models import User, UserCreate

from .fixtures import db, client
from src.crud import create_user


sample_user = User(
    uid="1",
    fullname="John",
    email="john@example.com",
    birthdate="1990-01-01",
    nick="eljuancho",
    alias="Juan Bostero",
    zone={"latitude":1.00000, "longitude":0.54},
    interests=["music", "movies"],
)


'''
    TEST GET /users/{uid}
'''

def test_read_user_uid_in_path(db, client):
    # Arrange 
    test_user = sample_user.copy()
    db.add(test_user)
    db.commit()

    user_public = UserPublic.from_orm(test_user)
    
    # Act
    res = client.get(f"/users/{test_user.uid}").json()
    
    # Assert
    assert res.status_code == 200
    assert users == user_public


def test_read_user_uid_in_path_twice(db, client):
    # Arrange 
    test_user = sample_user.copy()
    db.add(test_user)
    db.commit()

    user_public = UserPublic.from_orm(test_user)
    
    res = client.get(f"/users/{test_user.uid}").json()
    
    assert res.status_code == 200
    assert users == user_public

    res = client.get(f"/users/{test_user.uid}").json()
    
    assert res.status_code == 200
    assert users == user_public



def test_read_user_uid_in_path_not_found(db, client):
    # Act
    res = client.get(f"/users/some_uid").json()
    
    # Assert
    assert res.status_code == 404 
    assert res.detail == "user not found" 


'''
    TEST GET /users
'''

def test_read_users_filter_by_uid(db, client):
    # Arrange 
    test_user = sample_user.copy()
    db.add(test_user)
    db.commit()

    user_public = UserPublic.from_orm(test_user)
    
    # Act
    res = client.get(f"/users?uid={test_user.uid}").json()
    
    # Assert
    assert res.status_code == 200
    assert res.body[0] == user_public


def test_read_users_filter_by_email(db, client):
    # Arrange 
    test_user = sample_user.copy()
    db.add(test_user)
    db.commit()

    user_public = UserPublic.from_orm(test_user)
    
    # Act
    res = client.get(f"/users?email={test_user.email}").json()
    
    # Assert
    assert res.status_code == 200
    assert res.body[0] == user_public


def test_read_users_filter_by_nick(db, client):
    # Arrange 
    test_user = sample_user.copy()
    db.add(test_user)
    db.commit()

    user_public = UserPublic.from_orm(test_user)
    
    # Act
    res = client.get(f"/users?nick={test_user.nick}").json()
    
    # Assert
    assert res.status_code == 200
    assert res.body[0] == user_public


def test_read_users_filter_by_alias(db, client):
    # Arrange 
    test_user = sample_user.copy()
    db.add(test_user)
    db.commit()

    user_public = UserPublic.from_orm(test_user)
    
    # Act
    res = client.get(f"/users?alias={test_user.alias}").json()
    
    # Assert
    assert res.status_code == 200
    assert res.body[0] == user_public


