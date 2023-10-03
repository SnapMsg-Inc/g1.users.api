from pydantic import ValidationError
import pytest
from fastapi import HTTPException
from src.models import User, UserPublic, UserCreate, UserRead
from test.test_main import db_fixture as db
from test.test_main import client_fixture as client
from src.crud import read_users, create_user

FIRST_USER = 0

@pytest.fixture
def testUser1():
    return User(
        uid="1",
        fullname="John",
        email="john@example.com",
        birthdate="1990-01-01",
        nick="eljuancho",
        zone={"latitude":1.00000, "longitude":0.54},
        interests=["music", "movies"],
    )

@pytest.fixture
def testUser2():
    return User(
        uid="2",
        fullname="Charles",
        email="charles@example.com",
        birthdate="1992-01-01",
        nick="charles",
        zone={"latitude":1.00000, "longitude":0.54},
        interests=["music", "movies"],
    )

@pytest.fixture
def testUser3():
    return User(
        uid="3",
        fullname="Tom",
        email="tom@example.com",
        birthdate="1991-01-01",
        nick="Tom",
        zone={"latitude":1.00000, "longitude":0.54},
        interests=["music", "movies"],
    )

def test_read_users_happy_path(db, client, testUser1):
    # Arrange 
    db.add(testUser1)
    db.commit()

    user_read = UserRead.from_orm(testUser1)
    testUser1_public = UserPublic.from_orm(testUser1)
    
    # Act
	# query must be harcoded according to TestClient docs
    users = client.get("/users?uid=1").json()
    
    # Assert
    assert users[FIRST_USER] == testUser1_public

def test_read_users_no_user_found(db):

    userRead = UserRead(uid="unique_id_1")
    users = read_users(db, userRead, 100, 0)

    assert len(users) == 0
    assert users == []

def test_read_users_by_email(db, testUser1, testUser2, testUser3):
    
    # Arrange
    uid1 = "unique_id_1"
    uid2 = "unique_id_2"
    uid3 = "unique_id_3"

    
    # Act
    create_user(db, uid1, testUser1)
    create_user(db, uid2, testUser2)
    create_user(db, uid3, testUser3)

    userRead = UserRead(email=testUser1.email)
    users = read_users(db, userRead, 100, 0)

    # Assert
    assert len(users) == 1
    assert users[FIRST_USER].fullname == testUser1.fullname
    assert users[FIRST_USER].email == testUser1.email
    assert users[FIRST_USER].birthdate == testUser1.birthdate
    assert users[FIRST_USER].nick == testUser1.nick
    assert users[FIRST_USER].zone == testUser1.zone
