from pydantic import ValidationError
import pytest
from fastapi import HTTPException
from src.models import User, UserCreate
from test.test_main import db_fixture as db
from src.crud import create_user, read_follows, read_followers, follow_user, unfollow_user
from src.models import UserCreate

FIRST = 0

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
@pytest.fixture
def testUser2():
    return UserCreate(
        fullname="Charles",
        email="charles@example.com",
        birthdate="1992-01-01",
        nick="charles",
        zone={"latitude":1.00000, "longitude":0.54},
        interests=["music", "movies"],
    )

def test_user_unfollow_happy_path(db, testUser1, testUser2):
    # Arrange
    uid1 = "unique_id_1"
    uid2 = "unique_id_2"

    create_user(db, uid1, testUser1)
    create_user(db, uid2, testUser2)

    follow_user(db, uid1, uid2)

    # Act
    unfollow_user(db, uid1, uid2)

    db_user1 = db.get(User, uid1)
    db_user2 = db.get(User, uid2)

    # Assert
    assert read_follows(db, uid1,100, 0) == []
    assert read_followers(db, uid2,100, 0) == []

def test_user_unfollow_not_following(db, testUser1, testUser2):
    # Arrange
    uid1 = "unique_id_1"
    uid2 = "unique_id_2"

    create_user(db, uid1, testUser1)
    create_user(db, uid2, testUser2)

    # Act
    with pytest.raises(HTTPException) as excinfo:
        unfollow_user(db, uid1, uid2)
        assert str(excinfo.value.detail) == "follow not found"
    
def test_user_not_exist(db, testUser1, testUser2):
    # Arrange
    uid1 = "unique_id_1"
    uid2 = "unique_id_2"


    create_user(db, uid1, testUser1)

    # Act
    with pytest.raises(HTTPException) as excinfo:
        unfollow_user(db, uid1, uid2)
        assert str(excinfo.value.detail) == "user not found"

