from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, Field

import models
from database import get_db
from routers.base import BaseAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/categoryPerMedia", tags=["categoryPerMedia"])

class CategoryPerMedia(BaseModel):
    name: str = Field(..., min_length=3, max_length=30)

@cbv(router)
class CategoryPerMediaAPI(BaseAPI):
    db: Session = Depends(get_db)

    @router.get("/", response_model=list[CategoryPerMedia])
    def get_all_CategoryPerMedia(self):
        return self.db.query(models.DBCategoryPerMedia).all()

