# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.services import user_service
from app.database import get_db
from app import models

router = APIRouter(prefix="/users", tags=["用户管理"])

@router.post("/", response_model=schemas.UserResponse, status_code=201)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """注册新用户"""
    # 检查学号是否已存在
    existing = user_service.get_user_by_student_id(db, user.student_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"学号 '{user.student_id}' 已注册"
        )
    
    return user_service.create_user(db, user)


@router.get("/{student_id}", response_model=schemas.UserResponse)
def get_user(
    student_id: str,
    db: Session = Depends(get_db)
):
    """根据学号获取用户信息"""
    user = user_service.get_user_by_student_id(db, student_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.get("/{user_id}/records", response_model=List[schemas.RecordResponse])
def get_user_records(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """获取用户的打卡记录"""
    # 先检查用户是否存在
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    from app.services import record_service
    records = record_service.get_user_records(db, user_id, skip, limit)
    return records