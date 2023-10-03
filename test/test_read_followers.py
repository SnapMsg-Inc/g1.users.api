from pydantic import ValidationError
import pytest
from fastapi import HTTPException
from src.models import User, UserCreate, UserRead
from test.test_main import db_fixture as db
from src.crud import read_users, create_user, read_followers, follow_user, delete_user

FIRST_USER = 0

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

@pytest.fixture
def testUser3():
    return UserCreate(
        fullname="Tom",
        email="tom@example.com",
        birthdate="1991-01-01",
        nick="Tom",
        zone={"latitude":1.00000, "longitude":0.54},
        interests=["music", "movies"],
    )

def test_read_followers_happy_path(db, testUser1):
    # Arrange
    uid1 = "unique_id_1"
    uid2 = "unique_id_2"
    uid3 = "unique_id_3"
    
    # Act
    create_user(db, uid1, testUser1)
    create_user(db, uid2, testUser1)
    create_user(db, uid3, testUser1)
    db_user = db.get(User, uid1)

    follow_user(db, uid2, uid1)
    follow_user(db, uid3, uid1)

    followers = read_followers(db, uid1, 100, 0)
    
    # Assert
    assert len(followers) == 2