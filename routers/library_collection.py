from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, Field

import models
from database import get_db
from routers.base import BaseAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/libraryCollection", tags=["libraryCollection"])

class LibraryCollectionCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=30)

class LibraryCollectionResponse(LibraryCollectionCreate):
    id: int

@cbv(router)
class LibraryCollectionAPI(BaseAPI):
    db: Session = Depends(get_db)

    @router.get("/", response_model=list[LibraryCollectionResponse])
    def get_all_libraryCollection(self):
        return self.db.query(models.DBLibraryCollection).all()

    @router.get("/{libraryCollection_id}", response_model=LibraryCollectionResponse)
    def get_libraryCollection_by_id(self, libraryCollection_id: int):
        return self.get_or_404(self.db, models.DBLibraryCollection, libraryCollection_id)

    @router.post("/")
    def create_libraryCollection(self, libraryCollection: LibraryCollectionCreate):
        db_libraryCollection = models.DBLibraryCollection(name=libraryCollection.name)
        self.db.add(db_libraryCollection)
        self.db.commit()
        self.db.refresh(db_libraryCollection)
        return db_libraryCollection

    @router.delete("/{libraryCollection_id}")
    def delete_libraryCollection(self, libraryCollection_id: int):
        db_libraryCollection = self.get_or_404(self.db, models.DBLibraryCollection, libraryCollection_id)
        self.db.delete(db_libraryCollection)
        self.db.commit()