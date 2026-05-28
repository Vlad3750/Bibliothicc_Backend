from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class DBUser(Base):
    __tablename__ = 'user'

    userID = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    isAdmin = Column(Boolean, index=True)