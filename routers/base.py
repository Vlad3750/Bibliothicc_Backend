from fastapi import HTTPException
from sqlalchemy.orm import Session

class BaseAPI:
    def get_or_404(self, db: Session, model, item_id: int):
        # Primärschlüssel dynamisch ermitteln
        pk = model.__mapper__.primary_key[0].name
        item = db.query(model).filter(getattr(model, pk) == item_id).first()
        if not item:
            raise HTTPException(
                status_code=404,
                detail=f"Eintrag in '{model.__tablename__}' mit ID {item_id} nicht gefunden"
            )
        return item
