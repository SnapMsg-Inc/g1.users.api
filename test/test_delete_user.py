from pydantic import ValidationError
import pytest
from fastapi import HTTPException
from src.models import User, UserCreate
from test.test_main import db_fixture as db
from src.crud import create_user, delete_user

@pytest.fixture
def testUser1():
    return UserCreate(
        fullname="John",
        email="john@example.com",
        birthdate="1990-01-01",
        nick="eljuancho",
        zone={"latitude":1.00000, "longitude":0.54},
        interests=["music", "movies"],
    )

def test_delete_user_happy_path(db, testUser1):

    # Arrange
    create_user(db, "unique_id_1", testUser1)

    # Act
    assert db.get(User, "unique_id_1") != None

    delete_user(db, "unique_id_1")
    
    # Assert
    assert db.get(User, "unique_id_1") == None
    
def test_delete_user_not_exist(db):
    
    # Arrange
    uid = "unique_id_1"

    with pytest.raises(HTTPException) as excinfo:
        delete_user(db, uid)
        assert str(excinfo.value.detail) == "user not found"

    
       



