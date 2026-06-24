"""基线管理服务 (F026/F027)"""
import json
from datetime import datetime
from typing import Optional
from services.jdy_client import JDYClient
from services.field_mapper import FieldMapper

class BaselineManager:
    @staticmethod
    async def save_baseline(project_id: str) -> dict:
        """保存基线快照"""
        # 获取当前WBS数据
        wbs_entry = FieldMapper.get_entry_id("wbs_node")
        nodes = await JDYClient.list_data("APP_ID", wbs_entry,
                                          filter={"project_id": project_id})
        nodes = [FieldMapper.from_jdy_format("wbs_node", n) for n in nodes]
        
        # 获取依赖关系
        dep_entry = FieldMapper.get_entry_id("dependency")
        deps = await JDYClient.list_data("APP_ID", dep_entry,
                                         filter={"project_id": project_id})
        deps = [FieldMapper.from_jdy_format("dependency", d) for d in deps]
        
        # 构建快照
        snapshot = {
            "project_id": project_id,
            "created_at": datetime.now().isoformat(),
            "nodes": nodes,
            "dependencies": deps,
        }
        
        # 保存快照
        snap_entry = FieldMapper.get_entry_id("version_snapshot")
        jdy_data = FieldMapper.to_jdy_format("version_snapshot", {
            "project_id": project_id,
            "version": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "snapshot_data": json.dumps(snapshot, ensure_ascii=False),
        })
        result = await JDYClient.create_data("APP_ID", snap_entry, jdy_data)
        
        return {"status": "success", "version": snapshot["created_at"], "node_count": len(nodes)}
    
    @staticmethod
    async def compare_versions(project_id: str, v1: Optional[str] = None, v2: Optional[str] = None) -> dict:
        """版本对比"""
        snap_entry = FieldMapper.get_entry_id("version_snapshot")
        snapshots = await JDYClient.list_data("APP_ID", snap_entry,
                                              filter={"project_id": project_id})
        
        if len(snapshots) < 2:
            return {"status": "insufficient_data", "message": "需要至少2个基线版本"}
        
        # 取最新两个版本
        snapshots = sorted(snapshots, key=lambda x: x.get("created_at", ""), reverse=True)
        baseline = FieldMapper.from_jdy_format("version_snapshot", snapshots[1])
        current = FieldMapper.from_jdy_format("version_snapshot", snapshots[0])
        
        baseline_nodes = json.loads(baseline.get("snapshot_data", "{}")).get("nodes", [])
        current_nodes = json.loads(current.get("snapshot_data", "{}")).get("nodes", [])
        
        # 对比偏差
        baseline_map = {n["_id"]: n for n in baseline_nodes}
        deviations = []
        
        for node in current_nodes:
            nid = node["_id"]
            if nid in baseline_map:
                b = baseline_map[nid]
                es_diff = node.get("es", 0) - b.get("es", 0)
                ef_diff = node.get("ef", 0) - b.get("ef", 0)
                if es_diff != 0 or ef_diff != 0:
                    deviations.append({
                        "node_id": nid,
                        "name": node.get("name"),
                        "es_deviation": es_diff,
                        "ef_deviation": ef_diff,
                        "status": "delayed" if ef_diff > 0 else "ahead",
                    })
        
        return {
            "baseline_version": baseline.get("version"),
            "current_version": current.get("version"),
            "total_nodes": len(current_nodes),
            "deviations": deviations,
            "deviation_count": len(deviations),
        }
