from sqlalchemy.orm import Session
from app import models, schemas

def create_record(db: Session, record: schemas.RecordCreate):
    db_record = models.Record(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_cat_records(db: Session, cat_id: str, skip: int = 0, limit: int = 50):
    return db.query(models.Record).filter(models.Record.cat_id == cat_id).offset(skip).limit(limit).all()