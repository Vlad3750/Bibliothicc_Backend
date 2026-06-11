from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_restful.cbv import cbv
from pydantic import BaseModel, Field

import models
from database import get_db
from routers.base import BaseAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/libraryCollection", tags=["libraryCollection"])

class LibraryCollection(BaseModel):
    name: str = Field(..., min_length=3, max_length=30)

@cbv(router)
class LibraryCollectionAPI(BaseAPI):
    db: Session = Depends(get_db)

    @router.get("/", response_model=list[LibraryCollection])
    def get_all_libraryCollection(self):
        return self.db.query(models.DBLibraryCollection).all()

