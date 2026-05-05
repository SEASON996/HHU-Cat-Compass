import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 1. 数据库连接配置（从环境变量获取）
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("未设置 DATABASE_URL 环境变量")

# 2. 创建引擎（显式配置连接池，合理设置池大小）
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,           # 连接池中保持的连接数
    max_overflow=20,        # 池满时允许溢出的连接数
    pool_pre_ping=True,     # 自动重连失效连接
    echo=False              # 生产环境设为 False
)

# 3. 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 基类
Base = declarative_base()

# 5. 依赖注入：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()