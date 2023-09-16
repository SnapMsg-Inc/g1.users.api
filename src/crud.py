from fastapi import HTTPException
from sqlmodel import Session, select, column
from .models import User, UserCreate, UserRead, UserUpdate, Follow
from .database import engine


def create_user(uid: str, user: UserCreate):
	with Session(engine) as db:
		db_user = db.get(User, uid)
		if db_user:
			raise HTTPException(status_code=400, detail="user already exists")

		db_user = User.from_orm(user, {"uid" : uid})
		db.add(db_user)
		db.commit()
		db.refresh(db_user)


def read_user(db: Session, uid: str):
	db_user = db.get(User, uid)
	if not db_user:
		raise HTTPException(status_code=404, detail="user not found")
	return db_user


def read_users(user: UserRead, limit: int, page: int):
	#TODO: add followers and followings params
	user_query = user.dict(exclude_none=True)

	with Session(engine) as db:
		query = select(User).offset(page * limit).limit(limit)
		# match the query params case insensitive
		for k, v in user_query.items():
			query = query.where(getattr(User, k).regexp_match(v, "i"))
		return db.exec(query).all()


def update_user(uid: str, user: UserUpdate):
	with Session(engine) as db:
		db_user = db.get(User, uid)
		
		if not db_user:
			raise HTTPException(status_code=404, detail="user not found")
		user_data = user.dict(exclude_none=True)
		
		for k, v in user_data.items():
			setattr(db_user, k, v)
		db.add(db_user)
		db.commit()
		db.refresh(db_user)


def delete_user(uid: str):
	with Session(engine) as db:
		db_user = db.get(User, uid)
		if not db_user:
			raise HTTPException(status_code=404, detail="user not found")
		
		db.delete(db_user)
		db.commit()


def get_recommended(uid: str):
	return []


def follow_user(uid: str, otheruid: str):
	with Session(engine) as db:
		# verify that both users exist
		read_user(db, uid)
		read_user(db, otheruid)
		
		# verify that the follow does not exist
		query = select(Follow).where(Follow.uid==uid).where(Follow.followed_uid==otheruid)
		db_follow = db.exec(query).first()
		if db_follow:
			raise HTTPException(status_code=400, detail="follow already exists")

		db.add(Follow(uid=uid, followed_uid=otheruid))
		db.commit()


def unfollow_user(uid: str, otheruid: str):
	with Session(engine) as db:
		# verify that both users exist
		read_user(db, uid)
		read_user(db, otheruid)

		# verify that the follow exists
		query = select(Follow).where(Follow.uid==uid).where(Follow.followed_uid==otheruid)
		db_follow = db.exec(query).first()
		if not db_follow:
			raise HTTPException(status_code=404, detail="follow not found")

		db.delete(db_follow)
		db.commit()


