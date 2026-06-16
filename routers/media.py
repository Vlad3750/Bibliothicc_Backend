from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, Field
from typing import Optional

import models
from database import get_db
from routers.base import BaseAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/libraries/{library_id}/media", tags=["media"])

class MediaCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=100)
    mimeType: str = Field(..., min_length=1, max_length=20)
    mediaURL: str
    coverURL: Optional[str] = None

class MediaUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    coverURL: Optional[str] = None

class MediaResponse(BaseModel):
    mediaID: int
    name: str
    title: str
    mimeType: str
    mediaURL: str
    coverURL: Optional[str]
    lib_id: int

    class Config:
        from_attributes = True

@cbv(router)
class MediaAPI(BaseAPI):
    db: Session = Depends(get_db)

    @router.get("/", response_model=list[MediaResponse])
    def get_media_of_library(self, library_id: int):
        self.get_or_404(self.db, models.DBLibrary, library_id)
        return self.db.query(models.DBMedia).filter(
            models.DBMedia.lib_id == library_id
        ).all()

    @router.get("/{media_id}", response_model=MediaResponse)
    def get_media_by_id(self, library_id: int, media_id: int):
        self.get_or_404(self.db, models.DBLibrary, library_id)
        return self.get_or_404(self.db, models.DBMedia, media_id)

    @router.post("/", response_model=MediaResponse, status_code=201)
    def create_media(self, library_id: int, media: MediaCreate):
        self.get_or_404(self.db, models.DBLibrary, library_id)
        db_media = models.DBMedia(
            name=media.name,
            title=media.title,
            mimeType=media.mimeType,
            mediaURL=media.mediaURL,
            coverURL=media.coverURL,
            lib_id=library_id
        )
        self.db.add(db_media)
        self.db.commit()
        self.db.refresh(db_media)
        return db_media

    @router.put("/{media_id}", response_model=MediaResponse)
    def update_media(self, library_id: int, media_id: int, media: MediaUpdate):
        self.get_or_404(self.db, models.DBLibrary, library_id)
        db_media = self.get_or_404(self.db, models.DBMedia, media_id)
        if media.name is not None:
            db_media.name = media.name
        if media.title is not None:
            db_media.title = media.title
        if media.coverURL is not None:
            db_media.coverURL = media.coverURL
        self.db.commit()
        self.db.refresh(db_media)
        return db_media

    @router.delete("/{media_id}", status_code=204)
    def delete_media(self, library_id: int, media_id: int):
        self.get_or_404(self.db, models.DBLibrary, library_id)
        db_media = self.get_or_404(self.db, models.DBMedia, media_id)
        # Kategoriezuordnungen auch löschen
        self.db.query(models.DBCategoryPerMedia).filter(
            models.DBCategoryPerMedia.media_id == media_id
        ).delete()
        self.db.delete(db_media)
        self.db.commit()
