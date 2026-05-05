# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 
from app.routers import cats, users, records, upload
import os

app = FastAPI(
    title="河海猫咪地图 API",
    description="HHU Cat Compass Backend API",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(cats.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(upload.router) 

# 挂载静态文件目录（让上传的图片可以被访问）
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/")
def root():
    return {"message": "河海猫咪地图 API 服务运行中"}