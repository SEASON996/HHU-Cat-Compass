from sqlalchemy.orm import Session
from app import models, schemas

def get_user_by_student_id(db: Session, student_id: str):
    return db.query(models.User).filter(models.User.student_id == student_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user