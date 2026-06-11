from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, Field

import models
from database import get_db
from routers.base import BaseAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=["user"])

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=25)
    password: str = Field(..., min_length=8, max_length=25)

class UserResponse(BaseModel):
    name: str
    id: int

@cbv(router)
class UserAPI(BaseAPI):
    db: Session = Depends(get_db)

    @router.get("/", response_model=list[UserResponse])
    def get_all_user(self):
        return self.db.query(models.DBUser).all()

    @router.get("/{user_id}", response_model=UserResponse)
    def get_user_by_id(self, id:int):
        return self.get_or_404(self.db, models.DBUser, id)

    @router.post("/")
    def create_user(self, user:UserCreate):
        db_user = models.DBUser(name=user.name, password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    @router.delete("/{user_id}")
    def delete_item(self, user_id: int):
        db_user = self.get_or_404(self.db, models.DBUser, user_id)
        self.db.delete(db_user)
        self.db.commit()