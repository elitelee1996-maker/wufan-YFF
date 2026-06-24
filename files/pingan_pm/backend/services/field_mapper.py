"""字段映射服务 - 将简道云字段ID映射为语义化名称"""
import json
from typing import Dict, Any
from pathlib import Path

class FieldMapper:
    _instance = None
    _mappings: Dict[str, Dict[str, str]] = {}
    
    @classmethod
    def initialize(cls, mapping_file: str = "config/field_mapping.json"):
        """加载字段映射配置"""
        if cls._instance is None:
            cls._instance = cls()
            path = Path(mapping_file)
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    cls._mappings = json.load(f)
        return cls._instance
    
    @classmethod
    def get_entry_id(cls, table_name: str) -> str:
        """获取表单entry_id"""
        if table_name not in cls._mappings:
            raise ValueError(f"Unknown table: {table_name}")
        return cls._mappings[table_name].get("entry_id", "")
    
    @classmethod
    def get_field_id(cls, table_name: str, field_name: str) -> str:
        """获取字段widget_id"""
        if table_name not in cls._mappings:
            raise ValueError(f"Unknown table: {table_name}")
        fields = cls._mappings[table_name].get("fields", {})
        if field_name not in fields:
            raise ValueError(f"Unknown field: {field_name} in {table_name}")
        return fields[field_name]
    
    @classmethod
    def to_jdy_format(cls, table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """将语义化数据转换为简道云格式"""
        if table_name not in cls._mappings:
            raise ValueError(f"Unknown table: {table_name}")
        
        fields = cls._mappings[table_name].get("fields", {})
        jdy_data = {}
        
        for field_name, value in data.items():
            if field_name in fields:
                widget_id = fields[field_name]
                jdy_data[widget_id] = value
            else:
                # 保留未映射的字段
                jdy_data[field_name] = value
        
        return jdy_data
    
    @classmethod
    def from_jdy_format(cls, table_name: str, jdy_data: Dict[str, Any]) -> Dict[str, Any]:
        """将简道云格式数据转换为语义化格式"""
        if table_name not in cls._mappings:
            raise ValueError(f"Unknown table: {table_name}")
        
        fields = cls._mappings[table_name].get("fields", {})
        # 反向映射: widget_id -> field_name
        reverse_map = {v: k for k, v in fields.items()}
        
        data = {}
        for widget_id, value in jdy_data.items():
            if widget_id in reverse_map:
                field_name = reverse_map[widget_id]
                data[field_name] = value
            else:
                # 保留未映射的字段
                data[widget_id] = value
        
        return data
