from sqlalchemy import Column, Integer, String
from database import Base

class DBUser(Base):
    __tablename__ = 'user'

    