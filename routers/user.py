from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import DBUser
from pydantic import BaseModel

router = APIRouter(prefix="/user", tags=["user"])

class UserCreate(BaseModel):
    name: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    isAdmin: bool

    class Config:
        from_attributes = True

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(DBUser).filter(DBUser.name == user.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Username already taken")
    is_admin = user.name.lower() == "admin"
    db_user = DBUser(name=user.name, password=user.password, isAdmin=is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=UserResponse)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(
        DBUser.name == user.name,
        DBUser.password == user.password
    ).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return db_user