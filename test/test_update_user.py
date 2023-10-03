from pydantic import ValidationError
import pytest
from fastapi import HTTPException
from src.crud import update_user
from src.models import User, UserCreate, UserRead, UserUpdate
from test.test_main import db_fixture as db
from src.crud import read_users, create_user

FIRST_USER = 0

@pytest.fixture
def testUser1():
    return UserCreate(
        fullname="John",
        email="john@example.com",
        birthdate="1990-01-01",
        nick="eljuancho",
        zone={"latitude" : 0, "longitude" : 1},
        interests=["music", "movies"],
        ocupation="student",
    )


def test_update_user_nick(db, testUser1):
    # Arrange
    uid = "unique_id_1"
    create_user(db, uid, testUser1)

    
    # Act
    db_user = db.get(User, uid)
    
    userUpdate = UserUpdate(fullname = testUser1.fullname, 
                            nick = "updateNick",
                            zone = testUser1.zone,
                            email = testUser1.email,
                            interests = testUser1.interests,
                            ocupation = testUser1.ocupation,
                            )
    
    update_user(db, uid, userUpdate)


    # Assert
    assert db_user.nick == "updateNick"

def test_update_user_missing_field(db, testUser1):

    #with pytest.raises(ValidationError) as excinfo:

        # Arrange
    uid = "unique_id_1"
    create_user(db, uid, testUser1)

        # Act
    db_user = db.get(User, uid)
    userUpdate = UserUpdate(
		fullname = testUser1.fullname, 
        zone = testUser1.zone,
        email = testUser1.email,
        interests = testUser1.interests,
        ocupation = testUser1.ocupation,
    )
    update_user(db, uid, userUpdate)
    #assert "nick" in str(excinfo.value)

def test_update_user_not_exist(db, testUser1):
    # Arrange
    uid = "unique_id_1"
    with pytest.raises(HTTPException) as excinfo:
        # Act
        update_user(db, uid, testUser1)

        assert str(excinfo.value.detail) == "user not found"

