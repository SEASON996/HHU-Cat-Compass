from sqlalchemy.orm import Session
from app import models, schemas

def get_user_by_id(db: Session, user_id: int):
    """根据 ID 获取用户"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_student_id(db: Session, student_id: str):
    """根据学号获取用户"""
    return db.query(models.User).filter(models.User.student_id == student_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    """创建用户"""
    db_user = models.User(
        student_id=user.student_id,
        username=user.username,
        role=user.role if hasattr(user, 'role') else models.Role.STUDENT
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user