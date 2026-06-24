"""
平安快运 · 项目计划与进度管控系统 — FastAPI 后端入口
Standard 模式：FastAPI + React + PostgreSQL
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.settings import settings
from api.template_api import router as template_router
from api.wbs_api import router as wbs_router
from api.schedule_api import router as schedule_router
from api.resource_api import router as resource_router
from api.monitoring_api import router as monitoring_router
from api.auth_api import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from services.jdy_client import JDYClient
    JDYClient.initialize(settings.JDY_API_KEY, settings.JDY_API_URL)
    yield


app = FastAPI(
    title="平安快运 · 项目计划与进度管控系统",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["认证"])
app.include_router(template_router, prefix="/api/templates", tags=["模板管理"])
app.include_router(wbs_router, prefix="/api/projects", tags=["WBS编制"])
app.include_router(schedule_router, prefix="/api/projects", tags=["进度排程"])
app.include_router(resource_router, prefix="/api/resources", tags=["资源管理"])
app.include_router(monitoring_router, prefix="/api/monitoring", tags=["执行监控"])


@app.get("/api/health")
async def health_check():
    from services.jdy_client import JDYClient
    jdy_ok = JDYClient.is_configured()
    return {
        "status": "ok" if jdy_ok else "degraded",
        "jdy_configured": jdy_ok,
        "version": "1.0.0",
        "mode": "standard",
    }
