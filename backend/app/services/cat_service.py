from sqlalchemy.orm import Session
from app import models, schemas

def get_cat(db: Session, cat_id: str):
    return db.query(models.Cat).filter(models.Cat.id == cat_id).first()

def get_cats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cat).offset(skip).limit(limit).all()

def create_cat(db: Session, cat: schemas.CatCreate):
    db_cat = models.Cat(**cat.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def update_cat(db: Session, cat_id: str, cat_update: schemas.CatUpdate):
    db_cat = get_cat(db, cat_id)
    if not db_cat:
        return None
    for key, value in cat_update.model_dump(exclude_unset=True).items():
        setattr(db_cat, key, value)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def delete_cat(db: Session, cat_id: str):
    db_cat = get_cat(db, cat_id)
    if not db_cat:
        return False
    db.delete(db_cat)
    db.commit()
    return True