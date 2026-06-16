from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
import models
import os
import shutil
import uuid
from database import get_db

router = APIRouter(tags=["upload"])

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    path = f"data/uploads/{filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"url": f"/files/{filename}"}

@router.delete("/media/{media_id}", status_code=204)
def delete_media_global(media_id: int, db: Session = Depends(get_db)):
    db_media = db.query(models.DBMedia).filter(models.DBMedia.mediaID == media_id).first()
    if not db_media:
        raise HTTPException(status_code=404, detail="Media not found")
    db.query(models.DBCategoryPerMedia).filter(
        models.DBCategoryPerMedia.media_id == media_id
    ).delete()
    db.delete(db_media)
    db.commit()