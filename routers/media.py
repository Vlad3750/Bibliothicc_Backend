from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, Field

import models
from database import get_db
from routers.base import BaseAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/media", tags=["media"])

class MediaCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=25)

class MediaResponse(MediaCreate):
    id: int

@cbv(router)
class MediaAPI(BaseAPI):
    db: Session = Depends(get_db)

    @router.get("/", response_model=list[MediaResponse])
    def get_all_media(self):
        return self.db.query(models.DBMedia).all()

    @router.get("/{media_id}", response_model=MediaResponse)
    def get_media_by_id(self, id:int):
        return self.get_or_404(self.db, models.DBMedia, id)

    @router.post("/")
    def create_media(self, media:MediaCreate):
        db_media = models.DBMedia(name=media.name)
        self.db.add(db_media)
        self.db.commit()
        self.db.refresh(db_media)
        return db_media

    @router.delete("/{media_id}")
    def delete_media(self, media_id: int):
        db_media = self.get_or_404(self.db, models.DBMedia, media_id)
        self.db.delete(db_media)
        self.db.commit()