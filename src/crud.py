from sqlmodel import Session, select
from .models import User, UserCreate, UserUpdate
from .database import engine


def read_users(limit: int, page: int, uid: str, email: str, nick: str):
	# lowercase
	email = email.lower()
	nick = nick.lower()

	with Session(engine) as db:
		query = select(User).where(User.uid.contains(uid))
		query = query.where(User.email.contains(email))
		query = query.where(User.nick.contains(nick))
		query = query.offset(page * limit).limit(limit)
		return db.exec(query).all()



def create_user(uid: str, user: UserCreate):
	#db_user = User.from_orm(user, uid)
	db_user = User(**user.dict(), uid=uid)

	with Session(engine) as db:
		db.add(db_user)
		db.commit()


def update_user(uid: str, user: UserUpdate):
	pass


def delete_user(uid: str):
	pass

