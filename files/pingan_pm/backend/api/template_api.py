"""模板管理API"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class TemplateCreate(BaseModel):
    name: str
    project_type: str
    description: Optional[str] = None

@router.get("/")
async def list_templates():
    """获取模板列表"""
    from services.jdy_client import JDYClient
    from services.field_mapper import FieldMapper
    entry_id = FieldMapper.get_entry_id("template")
    data = await JDYClient.list_data("APP_ID", entry_id)
    return [FieldMapper.from_jdy_format("template", d) for d in data]

@router.post("/")
async def create_template(req: TemplateCreate):
    """创建模板"""
    from services.jdy_client import JDYClient
    from services.field_mapper import FieldMapper
    entry_id = FieldMapper.get_entry_id("template")
    jdy_data = FieldMapper.to_jdy_format("template", req.dict())
    return await JDYClient.create_data("APP_ID", entry_id, jdy_data)

@router.post("/{template_id}/import-to-project/{project_id}")
async def import_template_to_project(template_id: str, project_id: str):
    """从模板批量导入任务到项目 (F006)"""
    from services.template_importer import TemplateImporter
    return await TemplateImporter.import_to_project(template_id, project_id)
