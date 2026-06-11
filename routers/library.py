from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, Field

import models
from database import get_db
from routers.base import BaseAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/library", tags=["library"])

class LibraryCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=25)

class LibraryResponse(LibraryCreate):
    id: int

@cbv(router)
class LibraryAPI(BaseAPI):
    db: Session = Depends(get_db)

    @router.get("/", response_model=list[LibraryResponse])
    def get_all_libraries(self):
        return self.db.query(models.DBLibrary).all()

    @router.get("/{library_id}", response_model=LibraryResponse)
    def get_library_by_id(self, id:int):
        return self.get_or_404(self.db, models.DBLibrary, id)

    @router.post("/")
    def create_library(self, library:LibraryCreate):
        db_library = models.DBLibrary(name=library.name)
        self.db.add(db_library)
        self.db.commit()
        self.db.refresh(db_library)
        return db_library

    @router.delete("/{library_id}")
    def delete_library(self, library_id: int):
        db_library = self.get_or_404(self.db, models.DBLibrary, library_id)
        self.db.delete(db_library)
        self.db.commit()