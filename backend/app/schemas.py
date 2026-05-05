# app/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models import Gender, AgeStage, HealthStatus, Campus, CurrentStatus, EventType, Role

# ========== 用户相关 ==========
class UserBase(BaseModel):
    student_id: str
    username: str
    role: Role = Role.STUDENT

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

# ========== 猫咪相关 ==========
class CatBase(BaseModel):
    id: str = Field(..., description="业务主键，如 C001", max_length=20)
    name: str = Field(default="未命名", description="猫咪名字")
    gender: Gender
    age_stage: AgeStage
    coat_color: str = Field(..., description="毛色")
    health_status: HealthStatus
    campus: Campus
    location_desc: str = Field(..., description="具体位置描述")
    latitude: float = Field(..., ge=-90, le=90, description="纬度")
    longitude: float = Field(..., ge=-180, le=180, description="经度")
    photo_url: str = Field(..., description="照片URL")
    current_status: CurrentStatus = Field(default=CurrentStatus.NORMAL, description="当前状态")
    remark: Optional[str] = Field(None, description="备注")

class CatCreate(CatBase):
    pass

class CatUpdate(BaseModel):
    """猫咪更新模型（所有字段可选）"""
    name: Optional[str] = Field(None, description="猫咪名字")
    health_status: Optional[HealthStatus] = Field(None, description="健康状况")
    current_status: Optional[CurrentStatus] = Field(None, description="当前状态")
    location_desc: Optional[str] = Field(None, description="具体位置描述")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="纬度")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="经度")
    photo_url: Optional[str] = Field(None, description="照片URL")
    remark: Optional[str] = Field(None, description="备注")

class CatResponse(CatBase):
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ========== 打卡记录相关 ==========
class RecordBase(BaseModel):
    cat_id: str = Field(..., description="猫咪ID")
    event_type: EventType
    image_url: Optional[str] = Field(None, description="打卡图片URL")
    food_type: Optional[str] = Field(None, max_length=100, description="食物类型（投喂时填写）")

class RecordCreate(RecordBase):
    user_id: int = Field(..., description="用户ID")

class RecordResponse(RecordBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True