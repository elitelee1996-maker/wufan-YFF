"""进度排程API"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class ScheduleRequest(BaseModel):
    project_id: str

class RippleRequest(BaseModel):
    project_id: str
    changed_node_id: str

@router.post("/{project_id}/schedule")
async def run_schedule(project_id: str):
    """执行CPM全量计算 (F012/F013)"""
    from services.schedule_service import ScheduleService
    return await ScheduleService.run_full_schedule(project_id)

@router.post("/{project_id}/schedule/ripple")
async def ripple_update(project_id: str, req: RippleRequest):
    """级联更新 (F014) - 仅重算受影响分支"""
    from services.schedule_service import ScheduleService
    return await ScheduleService.ripple_update(project_id, req.changed_node_id)

@router.post("/{project_id}/baseline")
async def save_baseline(project_id: str):
    """保存基线快照 (F026)"""
    from services.baseline_manager import BaselineManager
    return await BaselineManager.save_baseline(project_id)

@router.get("/{project_id}/baseline/compare")
async def compare_baselines(project_id: str, v1: Optional[str] = None, v2: Optional[str] = None):
    """版本对比 (F027)"""
    from services.baseline_manager import BaselineManager
    return await BaselineManager.compare_versions(project_id, v1, v2)
