from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Boolean, Integer, Column

Base = declarative_base()

class User(Base):  # for request serialization
	__tablename__="users"

	id = Column(String(100), primary_key=True)
	email = Column(String(254), nullable=False)
	fullname = Column(String(50), nullable=False)
	nick = Column(String(30), nullable=False)
	interests = Column(String(209), nullable=False)
	followers = Column(Integer, default=0, nullable=False) 
	followings = Column(Integer, default=0, nullable=False) 
	zone = Column(String(200), nullable=False)
	isadmin = Column(Boolean, nullable=False, default=False)

	

