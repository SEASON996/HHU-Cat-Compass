from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.services import user_service
from app.auth import create_access_token, get_current_user
from app import schemas

router = APIRouter(prefix="/auth", tags=["认证"])

# 请求模型
class LoginRequest(BaseModel):
    student_id: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    student_id: str
    username: str
    role: str

@router.post("/login", response_model=LoginResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """学号直接登录（无密码，不存在则自动注册）"""
    
    # 查找用户
    user = user_service.get_user_by_student_id(db, login_data.student_id)
    
    if not user:
        # 用户不存在，自动注册
        user_data = schemas.UserCreate(
            student_id=login_data.student_id,
            username=f"河海猫友{login_data.student_id[-4:]}"
        )
        user = user_service.create_user(db, user_data)
    
    # 创建 JWT token
    token_data = {
        "user_id": user.id,
        "student_id": user.student_id,
        "username": user.username,
        "role": user.role.value if hasattr(user.role, 'value') else user.role
    }
    access_token = create_access_token(token_data)
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        student_id=user.student_id,
        username=user.username,
        role=user.role.value if hasattr(user.role, 'value') else user.role
    )

@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    """获取当前登录用户信息"""
    if not current_user:
        return None
    
    return {
        "id": current_user.id,
        "student_id": current_user.student_id,
        "username": current_user.username,
        "role": current_user.role.value if hasattr(current_user.role, 'value') else current_user.role
    }