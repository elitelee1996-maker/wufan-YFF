"""认证API - OAuth2.0 + JWT"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    jdy_token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    """简道云OAuth登录 → 签发JWT"""
    # TODO: 验证jdy_token → 获取用户信息 → 签发JWT
    raise HTTPException(status_code=501, detail="待实现: OAuth集成")

@router.get("/me")
async def get_current_user():
    """获取当前用户信息"""
    # TODO: 解析JWT → 返回用户信息
    raise HTTPException(status_code=501, detail="待实现: JWT解析")
