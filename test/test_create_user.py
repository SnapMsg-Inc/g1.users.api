import pytest
import json

from fastapi.testclient import TestClient 
from sqlmodel import Session
from pydantic import ValidationError
from src.models import User, UserCreate

#from .fixtures import db, client
from src.crud import create_user



sample_user = UserCreate(
    fullname="John", 
    email="john@example.com", 
    birthdate="1990-01-01",
    nick="eljuancho", 
    alias="Juan Bostero", 
    zone={"latitude":10.00, "longitude":0.00},  
    interests=["music", "movies"],
    pic="someurl"	
)


def test_create_user_happy_path(db: Session, client: TestClient):
    # Arrange
    uid = "unique_id"
    test_user = sample_user.copy()

    # Act
    res = client.post(f"/users/{uid}", json=test_user.model_dump())

    # Assert
    db_user = db.get(User, uid)
    assert db_user is not None

    db_user = UserCreate.from_orm(db_user)

    assert res.status_code == 201
    assert db_user == test_user
    

def test_create_uid_already_exists(client: TestClient):
    # Arrange
    uid = "unique_id"
    test_user = sample_user.copy()
    res = client.post(f"/users/{uid}", json=test_user.model_dump())
    assert res.status_code == 201
    # change nick and email
    test_user.nick = "pedro"
    test_user.email= "pedro@pedro.com"
 
    # Act
    res = client.post(f"/users/{uid}", json=test_user.model_dump())

    # Assert
    assert res.status_code == 409


def test_create_email_already_exists(client: TestClient):
    # Arrange
    uid = "unique_id_0"
    test_user = sample_user.copy()
    client.post(f"/users/{uid}", json=test_user.model_dump())

    # change uid and nick
    uid = "unique_id_1"
    test_user.nick = "juan"
 
    # Act
    res = client.post(f"/users/{uid}", json=test_user.model_dump())

    # Assert
    assert res.status_code == 409


def test_create_nick_already_exists(client: TestClient):
    # Arrange
    uid = "unique_id_0"
    test_user = sample_user.copy()
    client.post(f"/users/{uid}", json=test_user.model_dump())

    # change uid and nick
    uid = "unique_id_1"
    test_user.email = "juancho@example.com"
 
    # Act
    res = client.post(f"/users/{uid}", json=test_user.model_dump())

    # Assert
    assert res.status_code == 409

    
