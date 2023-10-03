from pydantic import ValidationError
import pytest
from fastapi import HTTPException
from src.models import User, UserCreate
from test.test_main import db_fixture as db
from src.crud import create_user


def test_create_user_happy_path(db):

    # Arrange
    uid = "unique_id_1"
    new_user = UserCreate(
		fullname="John", 
        email="john@example.com", 
        birthdate="1990-01-01",
        nick="eljuancho", 
        zone={"latitude":10.00, "longitude":0.00},  
        interests=["music", "movies"],
		pic="someurl"	
    )
    # Act
    create_user(db, uid, new_user)

    db_user = db.get(User, uid)


    # Assert
    assert db_user.uid == uid
    assert db_user.fullname == new_user.fullname
    assert db_user.email == new_user.email
    assert db_user.birthdate == new_user.birthdate
    assert db_user.nick == new_user.nick
    assert db_user.zone == new_user.zone
    assert db_user.interests == new_user.interests
    


def test_create_user_already_exists(db):
    
    # Arrange
    uid = "unique_id"
    user_data = UserCreate(fullname="John",
                           email="john@example.com",
                           birthdate="1990-01-01",
                           nick="eljuancho",
                           zone="Bogotá",
                           interests=["music", "movies"])

    # Act
    create_user(db, uid, user_data)

    with pytest.raises(HTTPException) as excinfo:
        create_user(db, uid, user_data)
    
    # Assert
    assert str(excinfo.value.detail) == "user already exists"

def test_create_user_missing_fields():
    
    with pytest.raises(ValidationError) as excinfo:
        # Arrange
        user_data = UserCreate(fullname="John",
                               email="john@gmail.com",
                               zone="Bogotá",
                               interests=["music", "movies"],
                               nick="eljuancho")
        
    # Assert 
    assert "birthdate" in str(excinfo.value)
    assert "field required" in str(excinfo.value)


    
