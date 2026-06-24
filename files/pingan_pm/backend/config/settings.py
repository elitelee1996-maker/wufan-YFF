"""配置管理"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # 简道云配置
    JDY_API_KEY: str = ""
    JDY_API_URL: str = "https://api.jiandaoyun.com/api/v5"
    JDY_APP_ID: str = ""
    
    # 数据库配置
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/pingan_pm"
    
    # JWT配置
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440  # 24小时
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # 服务配置
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
