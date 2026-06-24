"""模板导入服务 (F006) - 从模板批量导入任务到项目"""
from services.jdy_client import JDYClient
from services.field_mapper import FieldMapper
from services.wbs_calculator import WBSCalculator

class TemplateImporter:
    @staticmethod
    async def import_to_project(template_id: str, project_id: str) -> dict:
        """从模板导入任务清单和依赖关系到项目"""
        # 1. 读取模板任务清单
        std_entry = FieldMapper.get_entry_id("std_task")
        std_tasks = await JDYClient.list_data("APP_ID", std_entry, 
                                               filter={"template_id": template_id})
        
        # 2. 读取模板依赖关系
        dep_entry = FieldMapper.get_entry_id("template_dep")
        template_deps = await JDYClient.list_data("APP_ID", dep_entry,
                                                   filter={"template_id": template_id})
        
        # 3. 批量创建WBS节点
        wbs_entry = FieldMapper.get_entry_id("wbs_node")
        id_mapping = {}  # std_task_id → wbs_node_id
        
        wbs_data_list = []
        for task in std_tasks:
            task_data = FieldMapper.from_jdy_format("std_task", task)
            wbs_data = FieldMapper.to_jdy_format("wbs_node", {
                "project_id": project_id,
                "name": task_data.get("name"),
                "level": task_data.get("level", 1),
                "node_type": task_data.get("node_type", "task"),
                "duration": task_data.get("duration", 1),
                "constraint_type": task_data.get("constraint_type", "ASAP"),
            })
            wbs_data_list.append(wbs_data)
        
        result = await JDYClient.batch_create("APP_ID", wbs_entry, wbs_data_list)
        
        # 4. 建立ID映射
        for i, item in enumerate(result.get("data", [])):
            std_id = std_tasks[i].get("_id")
            wbs_id = item.get("_id")
            id_mapping[std_id] = wbs_id
        
        # 5. 导入依赖关系（替换ID）
        dep_data_list = []
        for dep in template_deps:
            dep_data = FieldMapper.from_jdy_format("template_dep", dep)
            from_id = id_mapping.get(dep_data.get("from_id"))
            to_id = id_mapping.get(dep_data.get("to_id"))
            if from_id and to_id:
                jdy_dep = FieldMapper.to_jdy_format("dependency", {
                    "project_id": project_id,
                    "from_id": from_id,
                    "to_id": to_id,
                    "dep_type": dep_data.get("dep_type", "FS"),
                    "lag": dep_data.get("lag", 0),
                })
                dep_data_list.append(jdy_dep)
        
        if dep_data_list:
            dep_entry_id = FieldMapper.get_entry_id("dependency")
            await JDYClient.batch_create("APP_ID", dep_entry_id, dep_data_list)
        
        # 6. 计算WBS编码
        await WBSCalculator.recalculate_all(project_id)
        
        return {
            "imported_tasks": len(wbs_data_list),
            "imported_deps": len(dep_data_list),
            "status": "success"
        }
