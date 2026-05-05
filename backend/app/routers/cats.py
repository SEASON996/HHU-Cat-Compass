# app/routers/cats.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas, models
from app.services import cat_service
from app.database import get_db

router = APIRouter(prefix="/cats", tags=["猫咪管理"])

@router.post("/", response_model=schemas.CatResponse, status_code=201)
def create_cat(
    cat: schemas.CatCreate, 
    db: Session = Depends(get_db)
):
    """创建新猫咪档案"""
    # 检查猫咪ID是否已存在
    existing = cat_service.get_cat(db, cat.id)
    if existing:
        raise HTTPException(status_code=400, detail=f"猫咪ID '{cat.id}' 已存在")
    
    return cat_service.create_cat(db, cat)


@router.get("/", response_model=List[schemas.CatResponse])
def get_cats(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=200, description="返回记录数"),
    campus: Optional[schemas.Campus] = Query(None, description="按校区筛选"),
    status: Optional[schemas.CurrentStatus] = Query(None, description="按状态筛选"),
    db: Session = Depends(get_db)
):
    """获取猫咪列表（支持分页和筛选）"""
    # 如果提供了筛选条件，需要自定义查询
    if campus or status:
        query = db.query(models.Cat)
        if campus:
            query = query.filter(models.Cat.campus == campus)
        if status:
            query = query.filter(models.Cat.current_status == status)
        cats = query.offset(skip).limit(limit).all()
        return cats
    
    # 无筛选条件，直接调用 service
    return cat_service.get_cats(db, skip, limit)


@router.get("/{cat_id}", response_model=schemas.CatResponse)
def get_cat(
    cat_id: str, 
    db: Session = Depends(get_db)
):
    """根据ID获取猫咪详情"""
    cat = cat_service.get_cat(db, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="猫咪不存在")
    return cat


@router.put("/{cat_id}", response_model=schemas.CatResponse)
def update_cat(
    cat_id: str,
    cat_update: schemas.CatUpdate,
    db: Session = Depends(get_db)
):
    """更新猫咪信息"""
    cat = cat_service.update_cat(db, cat_id, cat_update)
    if not cat:
        raise HTTPException(status_code=404, detail="猫咪不存在")
    return cat


@router.delete("/{cat_id}", status_code=204)
def delete_cat(
    cat_id: str,
    db: Session = Depends(get_db)
):
    """删除猫咪档案"""
    success = cat_service.delete_cat(db, cat_id)
    if not success:
        raise HTTPException(status_code=404, detail="猫咪不存在")
    return None  # 204 No Content 响应


@router.get("/campus/{campus}", response_model=List[schemas.CatResponse])
def get_cats_by_campus(
    campus: schemas.Campus,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """按校区获取猫咪列表"""
    query = db.query(models.Cat).filter(models.Cat.campus == campus)
    cats = query.offset(skip).limit(limit).all()
    return cats