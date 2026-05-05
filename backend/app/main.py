# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cats, users, records

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

@app.get("/")
def root():
    return {"message": "河海猫咪地图 API 服务运行中"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}