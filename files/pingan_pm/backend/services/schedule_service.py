"""进度排程服务 - 整合CPM引擎和JDY数据"""
from services.cpm_engine import CPMEngine
from services.jdy_client import JDYClient
from services.field_mapper import FieldMapper

class ScheduleService:
    @staticmethod
    async def run_full_schedule(project_id: str) -> dict:
        """执行CPM全量计算"""
        # 1. 加载WBS节点
        wbs_entry = FieldMapper.get_entry_id("wbs_node")
        nodes = await JDYClient.list_data("APP_ID", wbs_entry,
                                          filter={"project_id": project_id})
        nodes = [FieldMapper.from_jdy_format("wbs_node", n) for n in nodes]
        
        # 2. 加载依赖关系
        dep_entry = FieldMapper.get_entry_id("dependency")
        deps = await JDYClient.list_data("APP_ID", dep_entry,
                                         filter={"project_id": project_id})
        deps = [FieldMapper.from_jdy_format("dependency", d) for d in deps]
        
        # 3. 构建CPM输入
        tasks = {}
        for n in nodes:
            tasks[n["_id"]] = {
                "duration": n.get("duration", 1),
                "constraint_type": n.get("constraint_type", "ASAP"),
                "constraint_date": n.get("constraint_date"),
            }
        
        dep_list = [{"from_id": d["from_id"], "to_id": d["to_id"],
                     "type": d.get("dep_type", "FS"), "lag": d.get("lag", 0)}
                    for d in deps]
        
        # 4. 执行CPM计算
        forward = CPMEngine.forward_pass(tasks, dep_list)
        backward = CPMEngine.backward_pass(tasks, dep_list, forward)
        result = CPMEngine.calculate_float(forward, backward)
        
        # 5. 回写计算结果到简道云
        update_ids = []
        update_data = {}
        for tid, calc in result.items():
            jdy_data = FieldMapper.to_jdy_format("wbs_node", {
                "es": calc["ES"], "ef": calc["EF"],
                "ls": calc["LS"], "lf": calc["LF"],
                "tf": calc["TF"], "ff": calc["FF"],
                "is_critical": calc["is_critical"],
                "has_conflict": calc["has_conflict"],
            })
            await JDYClient.update_data("APP_ID", wbs_entry, tid, jdy_data)
        
        critical_count = sum(1 for r in result.values() if r["is_critical"])
        conflict_count = sum(1 for r in result.values() if r["has_conflict"])
        
        return {
            "status": "success",
            "total_tasks": len(tasks),
            "critical_path_count": critical_count,
            "conflict_count": conflict_count,
            "project_duration": max(r["EF"] for r in result.values()) if result else 0,
        }
    
    @staticmethod
    async def ripple_update(project_id: str, changed_node_id: str) -> dict:
        """级联更新 - 仅重算受影响分支"""
        # 简化实现：当前直接全量重算
        # TODO: 实现脏标记 + 局部重算优化
        return await ScheduleService.run_full_schedule(project_id)
