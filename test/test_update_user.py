from fastapi.testclient import TestClient 
from sqlmodel import Session

from .conftest import sample_user
from src.models import User, UserCreate, UserRead, UserUpdate


def test_update_user_nick(db: Session, client: TestClient, cleanup_db):
     # Arrange 
    test_user = sample_user() 
    db.add(test_user)
    db.commit()

    user_update = {"nick" : "different_nick"}
    test_user.nick = "different_nick"
    res = client.patch(f"/users/{test_user.uid}/", json=user_update)

    assert res.status_code == 200
    assert db.get(User, test_user.uid) == test_user


def test_update_user_alias(db: Session, client: TestClient, cleanup_db):
    test_user = sample_user() 
    db.add(test_user)
    db.commit()

    user_update = {"alias" : "different alias"}
    test_user.alias = "different alias"
    res = client.patch(f"/users/{test_user.uid}/", json=user_update)
    
    assert res.status_code == 200
    assert db.get(User, test_user.uid) == test_user
 

def test_update_user_zone(db: Session, client: TestClient, cleanup_db):
    test_user = sample_user() 
    db.add(test_user)
    db.commit()

    user_update = {"zone": {"latitude" : 1.0000, "longitude" : 99.9999}}
    test_user.zone = {"latitude" : 1.0000, "longitude" : 99.9999}
    res = client.patch(f"/users/{test_user.uid}/", json=user_update)

    assert res.status_code == 200
    assert db.get(User, test_user.uid) == test_user
  

def test_update_user_interests(db: Session, client: TestClient, cleanup_db):
    test_user = sample_user() 
    db.add(test_user)
    db.commit()

    user_update = {"interests" : ["football", "coffee"]}
    test_user.interests = ["football", "coffee"]
    res = client.patch(f"/users/{test_user.uid}/", json=user_update)
    
    assert res.status_code == 200
    assert db.get(User, test_user.uid) == test_user
  

def test_update_user_ocupation(db: Session, client: TestClient, cleanup_db):
    test_user = sample_user() 
    db.add(test_user)
    db.commit()

    user_update = {"ocupation" : "buisness man"}
    test_user.ocupation = "buisness man"
    res = client.patch(f"/users/{test_user.uid}/", json=user_update)

    assert res.status_code == 200
    assert db.get(User, test_user.uid) == test_user
    

def test_update_user_pic(db: Session, client: TestClient, cleanup_db):
    test_user = sample_user() 
    db.add(test_user)
    db.commit()

    user_update = {"pic" : "http://pics.com/some-pic.jpg"}
    test_user.pic = "http://pics.com/some-pic.jpg"
    res = client.patch(f"/users/{test_user.uid}/", json=user_update)

    assert res.status_code == 200
    assert db.get(User, test_user.uid) == test_user


def test_update_user_all(db: Session, client: TestClient, cleanup_db):
    test_user = sample_user() 
    db.add(test_user)
    db.commit()

    user_update = {
        "nick" : "different_nick",
        "alias" : "different alias",
        "zone" : {"latitude" : 9.99999, "longitude" : 0.0000},
        "interests" : ["trips", "hiking"],
        "ocupation" : "researcher",
        "pic" : "https://secure.pics.com/some-secure-pic.jpg"
    }
    test_user.__dict__.update(user_update)
    res = client.patch(f"/users/{test_user.uid}/", json=user_update)

    assert res.status_code == 200
    assert db.get(User, test_user.uid) == test_user


def test_update_user_does_not_exist(db: Session, client: TestClient, cleanup_db):
    test_user = sample_user() 

    user_update = {
        "pic" : "https://secure.pics.com/some-secure-pic.jpg"
    }
    res = client.patch(f"/users/{test_user.uid}/", json=user_update)
    assert res.status_code == 404 

