from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, Field
from typing import Optional

import models
from database import get_db
from routers.base import BaseAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users/{user_id}/categories", tags=["category"])

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=25)

class CategoryUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=25)

class CategoryResponse(BaseModel):
    categoryID: int
    name: str
    user_id: int

    class Config:
        from_attributes = True

@cbv(router)
class CategoryAPI(BaseAPI):
    db: Session = Depends(get_db)

    @router.get("/", response_model=list[CategoryResponse])
    def get_categories_of_user(self, user_id: int):
        self.get_or_404(self.db, models.DBUser, user_id)
        return self.db.query(models.DBCategory).filter(
            models.DBCategory.user_id == user_id
        ).all()

    @router.get("/{category_id}", response_model=CategoryResponse)
    def get_category_by_id(self, user_id: int, category_id: int):
        self.get_or_404(self.db, models.DBUser, user_id)
        return self.get_or_404(self.db, models.DBCategory, category_id)

    @router.post("/", response_model=CategoryResponse, status_code=201)
    def create_category(self, user_id: int, category: CategoryCreate):
        self.get_or_404(self.db, models.DBUser, user_id)
        # Doppelten Namen vermeiden
        existing = self.db.query(models.DBCategory).filter(
            models.DBCategory.user_id == user_id,
            models.DBCategory.name == category.name
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="Kategorie mit diesem Namen existiert bereits")
        db_category = models.DBCategory(name=category.name, user_id=user_id)
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    @router.put("/{category_id}", response_model=CategoryResponse)
    def rename_category(self, user_id: int, category_id: int, category: CategoryUpdate):
        self.get_or_404(self.db, models.DBUser, user_id)
        db_category = self.get_or_404(self.db, models.DBCategory, category_id)
        db_category.name = category.name
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    @router.delete("/{category_id}", status_code=204)
    def delete_category(self, user_id: int, category_id: int):
        self.get_or_404(self.db, models.DBUser, user_id)
        db_category = self.get_or_404(self.db, models.DBCategory, category_id)
        # Alle Zuordnungen dieser Kategorie auch löschen
        self.db.query(models.DBCategoryPerMedia).filter(
            models.DBCategoryPerMedia.category_id == category_id
        ).delete()
        self.db.delete(db_category)
        self.db.commit()
