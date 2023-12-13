from sqlmodel import Session, select, column
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from .models import User, UserCreate, UserRead, UserUpdate, Follow


class CRUDException(Exception):
    message: str = "API Error: "
    code: int

    def __init__(self, message, code=400):
        self.message += message
        self.code = code

    def __str__(self):
        return self.message


def create_user(db: Session, uid: str, user: UserCreate):
    db_user = User.from_orm(user, {"uid" : uid})

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        # 409 Conflict
        raise CRUDException(message="user already exists", code=409)


def read_user(db: Session, uid: str):
    #query = select(User).where(User.uid == uid)
    #return db.exec(query).first()
    return db.get(User, uid)

def read_users(db: Session, user: UserRead, limit: int, page: int):
    user_query = user.dict(exclude_none=True)
    query = select(User).offset(page * limit).limit(limit)
    # match the query params case insensitive
    for k, v in user_query.items():
        query = query.where(getattr(User, k).regexp_match(v, "i"))
    return db.exec(query).all()


def update_user(db: Session, uid: str, user: UserUpdate):
    db_user = db.get(User, uid)
    
    if not db_user:
        raise CRUDException(code=404, message="user not found")
    user_data = user.dict(exclude_none=True)
    
    for k, v in user_data.items():
        setattr(db_user, k, v)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def delete_user(db: Session, uid: str):
    db_user = db.get(User, uid)
    if not db_user:
        raise CRUDException(code=404, message="user not found")
    
    db.delete(db_user)
    db.commit()


def read_recommended(db: Session, uid: str):
    db_user = db.get(User, uid)
    db.engine.execute("SELECT * FROM users")
    print(select(selectable.c.uid))
    #db_recommended = db.exec(query)
    return []


def read_follow(db: Session, uid: str, followed: str):
    query = select(Follow)
    query = query.where(Follow.uid==uid)
    query = query.where(Follow.followed==followed)
    return db.exec(query).first()


def read_follows(db: Session, uid: str, limit: int, page: int):
    
    if not db.get(User, uid):
        raise CRUDException(code=404, message="user not found")
    
    follows = []
    query = select(Follow).offset(page * limit).limit(limit)
    query = query.where(Follow.uid==uid)
    db_follows = db.exec(query).all()

    for follow in db_follows:
        db_user = db.get(User, follow.followed)
        follows.append(db_user)
    return follows


def read_followers(db: Session, uid: str, limit: int, page: int):

    if not db.get(User, uid):
        raise CRUDException(code=404, message="user not found")
    
    followers = []
    query = select(Follow).offset(page * limit).limit(limit)
    query = query.where(Follow.followed==uid)
    db_follows = db.exec(query).all()

    for follower in db_follows:
        db_user = db.get(User, follower.uid)
        followers.append(db_user)
    return followers


def follow_user(db: Session, uid: str, otheruid: str):
    # verify that both users exist
    
    if uid == otheruid:
        raise CRUDException(message="follow operations are available for different users")
    
    db_user = db.get(User, uid)
    db_other_user = db.get(User, otheruid)

    if not db_user or not db_other_user:
        raise CRUDException(code=404, message="user not found")
    
    # verify that the follow doesn't exist
    query = select(Follow).where(Follow.uid==uid).where(Follow.followed==otheruid)
    db_follow = db.exec(query).first()
    if db_follow:
        raise CRUDException(message="follow already exists")
    
    # create the follow row
    db_follow = Follow(uid=uid, followed=otheruid)
    db.add(db_follow)
    setattr(db_user, "follows", db_user.follows + 1)
    setattr(db_other_user, "followers", db_other_user.followers + 1)
    db.add(db_user)
    db.add(db_other_user)
    db.commit()
    db.refresh(db_user)
    db.refresh(db_other_user)


def unfollow_user(db: Session, uid: str, otheruid: str):
    # verify that both users exist
    if uid == otheruid:
        raise CRUDException(message="follow operations are available for different users")
    
    db_user = db.get(User, uid)
    db_other_user = db.get(User, otheruid)

    if not db_user or not db_other_user:
        raise CRUDException(code=404, message="user not found")

    # verify that the follow exists
    query = select(Follow).where(Follow.uid==uid).where(Follow.followed==otheruid)
    db_follow = db.exec(query).first()
    if not db_follow:
        raise CRUDException(code=404, message="follow not found")

    db.delete(db_follow)
    setattr(db_user, "follows", db_user.follows - 1)
    setattr(db_other_user, "followers", db_other_user.followers - 1)
    db.add(db_user)
    db.add(db_other_user)
    db.commit()
    db.refresh(db_user)
    db.refresh(db_other_user)

