from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from pydantic import BaseModel

import models
from database import get_db
from routers.base import BaseAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/media/{media_id}/categories", tags=["category_per_media"])

class CategoryPerMediaResponse(BaseModel):
    categoryPerMediaID: int
    category_id: int
    media_id: int

    class Config:
        from_attributes = True

@cbv(router)
class CategoryPerMediaAPI(BaseAPI):
    db: Session = Depends(get_db)

    @router.get("/", response_model=list[CategoryPerMediaResponse])
    def get_categories_of_media(self, media_id: int):
        self.get_or_404(self.db, models.DBMedia, media_id)
        return self.db.query(models.DBCategoryPerMedia).filter(
            models.DBCategoryPerMedia.media_id == media_id
        ).all()

    @router.post("/{category_id}", response_model=CategoryPerMediaResponse, status_code=201)
    def add_category_to_media(self, media_id: int, category_id: int):
        self.get_or_404(self.db, models.DBMedia, media_id)
        self.get_or_404(self.db, models.DBCategory, category_id)

        # Doppelte Zuordnung vermeiden
        existing = self.db.query(models.DBCategoryPerMedia).filter(
            models.DBCategoryPerMedia.media_id == media_id,
            models.DBCategoryPerMedia.category_id == category_id
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="Kategorie bereits bei diesem Media vorhanden")

        db_cpm = models.DBCategoryPerMedia(category_id=category_id, media_id=media_id)
        self.db.add(db_cpm)
        self.db.commit()
        self.db.refresh(db_cpm)
        return db_cpm

    @router.delete("/{category_id}", status_code=204)
    def remove_category_from_media(self, media_id: int, category_id: int):
        entry = self.db.query(models.DBCategoryPerMedia).filter(
            models.DBCategoryPerMedia.media_id == media_id,
            models.DBCategoryPerMedia.category_id == category_id
        ).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Zuordnung nicht gefunden")
        self.db.delete(entry)
        self.db.commit()
