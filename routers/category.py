from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, Field

import models
from database import get_db
from routers.base import BaseAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/category", tags=["category"])

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=25)

class CategoryResponse(CategoryCreate):
    id: int

@cbv(router)
class CategoryAPI(BaseAPI):
    db: Session = Depends(get_db)

    @router.get("/", response_model=list[CategoryResponse])
    def get_all_categories(self):
        return self.db.query(models.DBCategory).all()

    @router.get("/{category_id}", response_model=CategoryResponse)
    def get_category_by_id(self, id:int):
        return self.get_or_404(self.db, models.DBCategory, id)

    @router.post("/")
    def create_category(self, category:CategoryCreate):
        db_category = models.DBCategory(name=category.name)
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    @router.delete("/{category_id}")
    def delete_category(self, category_id: int):
        db_category = self.get_or_404(self.db, models.DBCategory, category_id)
        self.db.delete(db_category)
        self.db.commit()