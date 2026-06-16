from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from pydantic import BaseModel

import models
from database import get_db
from routers.base import BaseAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users/{user_id}/libraries", tags=["library_collection"])

class LibraryCollectionResponse(BaseModel):
    libcolID: int
    user_id: int
    lib_id: int

    class Config:
        from_attributes = True

@cbv(router)
class LibraryCollectionAPI(BaseAPI):
    db: Session = Depends(get_db)

    @router.get("/", response_model=list[LibraryCollectionResponse])
    def get_libraries_of_user(self, user_id: int):
        # Prüfen ob User existiert
        self.get_or_404(self.db, models.DBUser, user_id)
        return self.db.query(models.DBLibraryCollection).filter(
            models.DBLibraryCollection.user_id == user_id
        ).all()

    @router.post("/{library_id}", response_model=LibraryCollectionResponse, status_code=201)
    def add_library_to_user(self, user_id: int, library_id: int):
        # Prüfen ob User und Library existieren
        self.get_or_404(self.db, models.DBUser, user_id)
        self.get_or_404(self.db, models.DBLibrary, library_id)

        # Prüfen ob Verbindung schon existiert
        existing = self.db.query(models.DBLibraryCollection).filter(
            models.DBLibraryCollection.user_id == user_id,
            models.DBLibraryCollection.lib_id == library_id
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="Library bereits beim User vorhanden")

        db_libcol = models.DBLibraryCollection(user_id=user_id, lib_id=library_id)
        self.db.add(db_libcol)
        self.db.commit()
        self.db.refresh(db_libcol)
        return db_libcol

    @router.delete("/{library_id}", status_code=204)
    def remove_library_from_user(self, user_id: int, library_id: int):
        entry = self.db.query(models.DBLibraryCollection).filter(
            models.DBLibraryCollection.user_id == user_id,
            models.DBLibraryCollection.lib_id == library_id
        ).first()
        if not entry:
            raise HTTPException(status_code=404, detail="Verbindung nicht gefunden")
        self.db.delete(entry)
        self.db.commit()
