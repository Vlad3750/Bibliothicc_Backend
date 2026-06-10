from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, Field, field_validator

import models
from database import get_db
from routers.base import BaseAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=["user"])

class UserCreate(BaseModel):
    name:str = Field(..., min_length=3, max_length=25)
    password:str = Field(..., min_length=8, max_length=25)

class UserResponse(BaseModel):
    name: str
    id: int

@cbv(router)
class UserAPI(BaseAPI):
    db: Session = Depends(get_db())

    @router.get("/", response_model=list[UserResponse])
    def get_all_user(self):
        return self.db.query(models.DBUser).all()