from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, Field
from typing import Optional

import models
from database import get_db
from routers.base import BaseAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/library", tags=["library"])

class LibraryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    fileType: str = Field(..., description="Video, Movie, Text, Image oder Audio")
    isPublic: bool = False

class LibraryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    isPublic: Optional[bool] = None

class LibraryResponse(BaseModel):
    libID: int
    name: str
    fileType: str
    isPublic: bool

    class Config:
        from_attributes = True

@cbv(router)
class LibraryAPI(BaseAPI):
    db: Session = Depends(get_db)

    @router.get("/", response_model=list[LibraryResponse])
    def get_all_libraries(self):
        return self.db.query(models.DBLibrary).all()

    @router.get("/public", response_model=list[LibraryResponse])
    def get_public_libraries(self):
        return self.db.query(models.DBLibrary).filter(models.DBLibrary.isPublic == True).all()

    @router.get("/{library_id}", response_model=LibraryResponse)
    def get_library_by_id(self, library_id: int):
        return self.get_or_404(self.db, models.DBLibrary, library_id)

    @router.post("/", response_model=LibraryResponse, status_code=201)
    def create_library(self, library: LibraryCreate):
        valid_types = ["Video", "Movie", "Text", "Image", "Audio"]
        if library.fileType not in valid_types:
            raise HTTPException(status_code=400, detail=f"fileType muss einer von {valid_types} sein")
        db_library = models.DBLibrary(name=library.name, fileType=library.fileType, isPublic=library.isPublic)
        self.db.add(db_library)
        self.db.commit()
        self.db.refresh(db_library)
        return db_library

    @router.put("/{library_id}", response_model=LibraryResponse)
    def update_library(self, library_id: int, library: LibraryUpdate):
        db_library = self.get_or_404(self.db, models.DBLibrary, library_id)
        if library.name is not None:
            db_library.name = library.name
        if library.isPublic is not None:
            db_library.isPublic = library.isPublic
        self.db.commit()
        self.db.refresh(db_library)
        return db_library

    @router.delete("/{library_id}", status_code=204)
    def delete_library(self, library_id: int):
        db_library = self.get_or_404(self.db, models.DBLibrary, library_id)
        self.db.query(models.DBMedia).filter(models.DBMedia.lib_id == library_id).delete()
        self.db.delete(db_library)
        self.db.commit()