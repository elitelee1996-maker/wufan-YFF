"""WBS编制API"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class DependencyCreate(BaseModel):
    from_id: str
    to_id: str
    dep_type: str = "FS"
    lag: int = 0

class ReorderRequest(BaseModel):
    node_id: str
    new_parent_id: Optional[str] = None
    new_order: int

@router.get("/{project_id}/wbs")
async def get_wbs_tree(project_id: str):
    """获取项目WBS树"""
    from services.wbs_calculator import WBSCalculator
    return await WBSCalculator.get_tree(project_id)

@router.post("/{project_id}/wbs/reorder")
async def reorder_wbs(project_id: str, req: ReorderRequest):
    """拖拽排序 → 重算WBS编码 (F008)"""
    from services.wbs_calculator import WBSCalculator
    return await WBSCalculator.reorder(project_id, req.node_id, req.new_parent_id, req.new_order)

@router.get("/{project_id}/dependencies")
async def list_dependencies(project_id: str):
    """获取依赖关系列表"""
    from services.jdy_client import JDYClient
    from services.field_mapper import FieldMapper
    entry_id = FieldMapper.get_entry_id("dependency")
    data = await JDYClient.list_data("APP_ID", entry_id, filter={"project_id": project_id})
    return [FieldMapper.from_jdy_format("dependency", d) for d in data]

@router.post("/{project_id}/dependencies")
async def create_dependency(project_id: str, req: DependencyCreate):
    """添加依赖关系 + 循环检测 (F009/F010)"""
    from services.cpm_engine import CPMEngine
    from services.jdy_client import JDYClient
    from services.field_mapper import FieldMapper
    
    # 获取现有依赖
    dep_entry = FieldMapper.get_entry_id("dependency")
    existing = await JDYClient.list_data("APP_ID", dep_entry, filter={"project_id": project_id})
    
    # 构建任务列表和依赖列表
    tasks = [req.from_id, req.to_id]
    deps = [{"from_id": d.get("from_id"), "to_id": d.get("to_id")} for d in existing]
    deps.append({"from_id": req.from_id, "to_id": req.to_id})
    
    # 循环检测
    cycle = CPMEngine.detect_cycle(tasks, deps)
    if cycle:
        raise HTTPException(status_code=400, detail=f"循环依赖: {' → '.join(cycle)}")
    
    # 创建依赖
    jdy_data = FieldMapper.to_jdy_format("dependency", {
        "project_id": project_id,
        "from_id": req.from_id,
        "to_id": req.to_id,
        "dep_type": req.dep_type,
        "lag": req.lag,
    })
    return await JDYClient.create_data("APP_ID", dep_entry, jdy_data)

@router.post("/{project_id}/dependencies/validate")
async def validate_dependencies(project_id: str, req: DependencyCreate):
    """验证依赖关系（循环检测）(F010)"""
    from services.cpm_engine import CPMEngine
    from services.jdy_client import JDYClient
    from services.field_mapper import FieldMapper
    
    dep_entry = FieldMapper.get_entry_id("dependency")
    existing = await JDYClient.list_data("APP_ID", dep_entry, filter={"project_id": project_id})
    
    tasks = [req.from_id, req.to_id]
    deps = [{"from_id": d.get("from_id"), "to_id": d.get("to_id")} for d in existing]
    deps.append({"from_id": req.from_id, "to_id": req.to_id})
    
    cycle = CPMEngine.detect_cycle(tasks, deps)
    return {"valid": cycle is None, "cycle_path": cycle}
