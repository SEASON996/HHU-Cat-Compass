from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict
import os
import uuid
import shutil
from datetime import datetime

router = APIRouter(prefix="/upload", tags=["文件上传"])

# 配置上传目录
UPLOAD_DIR = "uploads"
# 确保目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 允许的图片格式
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
# 最大文件大小 5MB
MAX_FILE_SIZE = 5 * 1024 * 1024

@router.post("/")
async def upload_image(file: UploadFile = File(...)) -> Dict:
    """上传图片接口"""
    
    # 1. 验证文件类型
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"不支持的图片格式，仅支持: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # 2. 验证文件大小
    file.file.seek(0, 2)  # 移动到文件末尾
    file_size = file.file.tell()  # 获取文件大小
    file.file.seek(0)  # 重置到开头
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"图片大小不能超过 5MB，当前: {file_size / 1024 / 1024:.2f}MB"
        )
    
    # 3. 生成唯一文件名（避免重名）
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # 4. 保存文件
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")
    
    # 5. 返回可访问的 URL
    return {
        "url": f"/uploads/{unique_filename}",
        "filename": unique_filename,
        "original_name": file.filename,
        "size": file_size,
        "upload_time": datetime.now().isoformat()
    }