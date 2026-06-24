"""执行监控API"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/warnings")
async def list_warnings(project_id: str = None, level: str = None):
    """获取预警列表"""
    from services.jdy_client import JDYClient
    from services.field_mapper import FieldMapper
    entry_id = FieldMapper.get_entry_id("warning")
    filter_dict = {}
    if project_id:
        filter_dict["project_id"] = project_id
    if level:
        filter_dict["level"] = level
    data = await JDYClient.list_data("APP_ID", entry_id, filter=filter_dict)
    return [FieldMapper.from_jdy_format("warning", d) for d in data]

@router.get("/action-items")
async def list_action_items(project_id: str = None):
    """获取行动项列表"""
    from services.jdy_client import JDYClient
    from services.field_mapper import FieldMapper
    entry_id = FieldMapper.get_entry_id("action_item")
    filter_dict = {}
    if project_id:
        filter_dict["project_id"] = project_id
    data = await JDYClient.list_data("APP_ID", entry_id, filter=filter_dict)
    return [FieldMapper.from_jdy_format("action_item", d) for d in data]
