from pydantic import ValidationError
import pytest
from fastapi import HTTPException
from src.models import User, UserCreate, UserRead
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
        zone="Bogotá",
        interests=["music", "movies"],
    )

@pytest.fixture
def testUser2():
    return UserCreate(
        fullname="Charles",
        email="charles@example.com",
        birthdate="1992-01-01",
        nick="charles",
        zone="UK",
        interests=["music", "movies"],
    )

@pytest.fixture
def testUser3():
    return UserCreate(
        fullname="Tom",
        email="tom@example.com",
        birthdate="1991-01-01",
        nick="Tom",
        zone="US",
        interests=["music", "movies"],
    )

def test_read_users_happy_path(db, testUser1):
    # Arrange
    uid = "unique_id_1"
    
    # Act
    create_user(db, uid, testUser1)
    db_user = db.get(User, uid)

    userRead = UserRead(uid=uid, email=testUser1.email, nick=testUser1.nick)

    users = read_users(db, userRead, 100, 0)
    

    # Assert
    assert len(users) == 1

    assert users[FIRST_USER].fullname == testUser1.fullname
    assert users[FIRST_USER].email == testUser1.email
    assert users[FIRST_USER].birthdate == testUser1.birthdate
    assert users[FIRST_USER].nick == testUser1.nick
    assert users[FIRST_USER].zone == testUser1.zone
    assert users[FIRST_USER].interests == testUser1.interests

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