from sqlalchemy import Column, String, Float, DateTime, Integer, Text, ForeignKey, Enum as SQLEnum, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

# ---- 枚举定义（便于代码维护）----
class Gender(str, enum.Enum):
    MALE = "公"
    FEMALE = "母"
    UNKNOWN = "未知"

class AgeStage(str, enum.Enum):
    KITTEN = "幼年"
    YOUNG = "青年"
    ADULT = "成年"
    SENIOR = "老年"

class HealthStatus(str, enum.Enum):
    HEALTHY = "正常"
    NEED_HELP = "需救助"
    NEUTERED = "已绝育"

class Campus(str, enum.Enum):
    JIANGNING = "江宁"
    XIXILU = "西康路"
    JINTAN = "金坛"

class CurrentStatus(str, enum.Enum):
    NORMAL = "正常"
    NEED_HELP = "需救助"
    ADOPTED = "已领养"
    MISSING = "失踪"

class EventType(str, enum.Enum):
    SIGHTING = "偶遇打卡"
    FEEDING = "投喂打卡"

class Role(str, enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"

# ---- 表定义 ----
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String, unique=True, index=True, nullable=False)  # 学号/工号，唯一
    username = Column(String, nullable=False)
    role = Column(SQLEnum(Role), default=Role.STUDENT)

    records = relationship("Record", back_populates="user")


class Cat(Base):
    __tablename__ = "cats"

    id = Column(String(20), primary_key=True, index=True)  # 业务主键，如 "C001"
    name = Column(String, default="未命名")
    gender = Column(SQLEnum(Gender), nullable=False)
    age_stage = Column(SQLEnum(AgeStage), nullable=False)
    coat_color = Column(String, nullable=False)
    health_status = Column(SQLEnum(HealthStatus), nullable=False)

    campus = Column(SQLEnum(Campus), nullable=False)
    location_desc = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    photo_url = Column(String, nullable=False)
    current_status = Column(SQLEnum(CurrentStatus), default=CurrentStatus.NORMAL)
    remark = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    records = relationship("Record", back_populates="cat")


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cat_id = Column(String(20), ForeignKey("cats.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # 关联 users.id

    event_type = Column(SQLEnum(EventType), nullable=False)
    image_url = Column(String, nullable=True)
    food_type = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    cat = relationship("Cat", back_populates="records")
    user = relationship("User", back_populates="records")