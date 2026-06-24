"""资源调度服务 - 冲突检测与决策"""
from typing import List, Optional
from services.jdy_client import JDYClient
from services.field_mapper import FieldMapper

class ResourceScheduler:
    @staticmethod
    async def detect_conflicts(project_id: Optional[str] = None) -> List[dict]:
        """检测资源冲突 (F020) - 时间区间重叠"""
        entry_id = FieldMapper.get_entry_id("resource_occupy")
        filter_dict = {}
        if project_id:
            filter_dict["project_id"] = project_id
        
        occupations = await JDYClient.list_data("APP_ID", entry_id, filter=filter_dict)
        occupations = [FieldMapper.from_jdy_format("resource_occupy", o) for o in occupations]
        
        # 按资源分组
        by_resource = {}
        for occ in occupations:
            rid = occ.get("resource_id")
            if rid not in by_resource:
                by_resource[rid] = []
            by_resource[rid].append(occ)
        
        # 检测时间区间重叠
        conflicts = []
        for rid, occs in by_resource.items():
            sorted_occs = sorted(occs, key=lambda x: x.get("start_date", ""))
            for i in range(len(sorted_occs)):
                for j in range(i + 1, len(sorted_occs)):
                    a = sorted_occs[i]
                    b = sorted_occs[j]
                    # 区间重叠: a.start < b.end and b.start < a.end
                    if a.get("start_date") < b.get("end_date") and \
                       b.get("start_date") < a.get("end_date"):
                        conflicts.append({
                            "resource_id": rid,
                            "task_a": a.get("task_id"),
                            "task_b": b.get("task_id"),
                            "overlap_start": max(a.get("start_date"), b.get("start_date")),
                            "overlap_end": min(a.get("end_date"), b.get("end_date")),
                        })
        
        return conflicts
    
    @staticmethod
    async def resolve_conflict(conflict_id: str, resolution: str) -> dict:
        """冲突决策 (F022)"""
        # TODO: 根据resolution类型执行不同策略
        return {"status": "resolved", "resolution": resolution}
