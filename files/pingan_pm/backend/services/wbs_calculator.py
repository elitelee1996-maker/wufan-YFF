"""WBS编码计算服务"""
from typing import Optional, List, Dict
from collections import defaultdict
from services.jdy_client import JDYClient
from services.field_mapper import FieldMapper

class WBSCalculator:
    @staticmethod
    async def get_tree(project_id: str) -> dict:
        """获取项目WBS树结构"""
        entry_id = FieldMapper.get_entry_id("wbs_node")
        nodes = await JDYClient.list_data("APP_ID", entry_id, 
                                          filter={"project_id": project_id})
        
        flat_nodes = [FieldMapper.from_jdy_format("wbs_node", n) for n in nodes]
        
        # 构建树
        node_map = {n["_id"]: n for n in flat_nodes}
        children = defaultdict(list)
        roots = []
        
        for n in flat_nodes:
            parent = n.get("parent_id")
            if parent and parent in node_map:
                children[parent].append(n)
            else:
                roots.append(n)
        
        def build_tree(node):
            node["children"] = [build_tree(c) for c in children.get(node["_id"], [])]
            return node
        
        return {"tree": [build_tree(r) for r in roots], "total": len(flat_nodes)}
    
    @staticmethod
    async def recalculate_all(project_id: str):
        """全量重算WBS编码"""
        tree = await WBSCalculator.get_tree(project_id)
        
        entry_id = FieldMapper.get_entry_id("wbs_node")
        updates = []
        
        def assign_codes(nodes, prefix=""):
            for i, node in enumerate(nodes, 1):
                code = f"{prefix}{i}" if prefix else str(i)
                updates.append({"id": node["_id"], "wbs_code": code})
                if node.get("children"):
                    assign_codes(node["children"], f"{code}.")
        
        assign_codes(tree["tree"])
        
        # 批量更新
        for update in updates:
            jdy_data = FieldMapper.to_jdy_format("wbs_node", {"wbs_code": update["wbs_code"]})
            await JDYClient.update_data("APP_ID", entry_id, update["id"], jdy_data)
    
    @staticmethod
    async def reorder(project_id: str, node_id: str, 
                     new_parent_id: Optional[str], new_order: int):
        """拖拽排序后重算编码"""
        entry_id = FieldMapper.get_entry_id("wbs_node")
        
        # 更新父节点和排序号
        update_data = {"sort_order": new_order}
        if new_parent_id:
            update_data["parent_id"] = new_parent_id
        
        jdy_data = FieldMapper.to_jdy_format("wbs_node", update_data)
        await JDYClient.update_data("APP_ID", entry_id, node_id, jdy_data)
        
        # 全量重算编码
        await WBSCalculator.recalculate_all(project_id)
