"""资源管理API"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ConflictResolveRequest(BaseModel):
    conflict_id: str
    resolution: str  # "adjust_time" | "replace_resource" | "priority_sort"

@router.get("/{resource_id}/occupations")
async def get_resource_occupations(resource_id: str):
    """获取资源占用记录"""
    from services.jdy_client import JDYClient
    from services.field_mapper import FieldMapper
    entry_id = FieldMapper.get_entry_id("resource_occupy")
    data = await JDYClient.list_data("APP_ID", entry_id, filter={"resource_id": resource_id})
    return [FieldMapper.from_jdy_format("resource_occupy", d) for d in data]

@router.get("/conflicts")
async def list_conflicts(project_id: str = None):
    """获取资源冲突列表 (F020)"""
    from services.resource_scheduler import ResourceScheduler
    return await ResourceScheduler.detect_conflicts(project_id)

@router.put("/conflicts/{conflict_id}/resolve")
async def resolve_conflict(conflict_id: str, req: ConflictResolveRequest):
    """冲突决策 (F022)"""
    from services.resource_scheduler import ResourceScheduler
    return await ResourceScheduler.resolve_conflict(conflict_id, req.resolution)
