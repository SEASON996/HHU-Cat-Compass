# app/routers/records.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas
from app.services import record_service, cat_service, user_service
from app import models
from app.database import get_db

router = APIRouter(prefix="/records", tags=["打卡记录"])

@router.post("/", response_model=schemas.RecordResponse, status_code=201)
def create_record(
    record: schemas.RecordCreate,
    db: Session = Depends(get_db)
):
    """创建打卡记录"""
    # 验证猫咪是否存在
    cat = cat_service.get_cat(db, record.cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail=f"猫咪 '{record.cat_id}' 不存在")
    
    # 验证用户是否存在
    user = user_service.get_user_by_student_id(db, str(record.user_id))
    if not user:
        raise HTTPException(status_code=404, detail=f"用户不存在")
    
    return record_service.create_record(db, record)


@router.get("/cat/{cat_id}", response_model=List[schemas.RecordResponse])
def get_cat_records(
    cat_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取某只猫咪的所有打卡记录"""
    # 验证猫咪是否存在
    cat = cat_service.get_cat(db, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="猫咪不存在")
    
    return record_service.get_cat_records(db, cat_id, skip, limit)


@router.get("/user/{user_id}", response_model=List[schemas.RecordResponse])
def get_user_records(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取某个用户的所有打卡记录"""
    # 验证用户是否存在
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return record_service.get_user_records(db, user_id, skip, limit)


@router.get("/stats/cat/{cat_id}")
def get_cat_stats(
    cat_id: str,
    db: Session = Depends(get_db)
):
    """获取某只猫咪的打卡统计"""
    # 验证猫咪是否存在
    cat = cat_service.get_cat(db, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="猫咪不存在")
    
    # 统计总打卡次数
    total_records = db.query(models.Record).filter(models.Record.cat_id == cat_id).count()
    
    # 统计不同类型打卡次数
    sighting_count = db.query(models.Record).filter(
        models.Record.cat_id == cat_id,
        models.Record.event_type == schemas.EventType.SIGHTING
    ).count()
    
    feeding_count = db.query(models.Record).filter(
        models.Record.cat_id == cat_id,
        models.Record.event_type == schemas.EventType.FEEDING
    ).count()
    
    return {
        "cat_id": cat_id,
        "cat_name": cat.name,
        "total_records": total_records,
        "sighting_count": sighting_count,
        "feeding_count": feeding_count
    }