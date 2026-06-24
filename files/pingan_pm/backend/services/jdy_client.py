"""简道云API客户端封装"""
import httpx
from typing import Dict, List, Optional, Any
from config.settings import settings

class JDYClient:
    _instance = None
    _client: httpx.AsyncClient = None
    _api_key: str = ""
    _api_url: str = ""
    
    @classmethod
    def initialize(cls, api_key: str, api_url: str):
        cls._api_key = api_key
        cls._api_url = api_url
        cls._client = httpx.AsyncClient(
            base_url=api_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30.0
        )
    
    @classmethod
    def is_configured(cls) -> bool:
        return bool(cls._api_key and cls._client)
    
    @classmethod
    async def create_data(cls, app_id: str, entry_id: str, data: Dict) -> Dict:
        """创建单条数据"""
        response = await cls._client.post(
            f"/open/app/{app_id}/entry_data",
            json={"entry_id": entry_id, "data": data}
        )
        response.raise_for_status()
        return response.json()
    
    @classmethod
    async def list_data(cls, app_id: str, entry_id: str, 
                       filter: Optional[Dict] = None,
                       limit: int = 100, 
                       fields: Optional[List[str]] = None) -> List[Dict]:
        """查询数据列表"""
        payload = {
            "entry_id": entry_id,
            "limit": limit,
        }
        if filter:
            payload["filter"] = filter
        if fields:
            payload["fields"] = fields
        
        response = await cls._client.post(
            f"/open/app/{app_id}/entry_data/list",
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        return result.get("data", [])
    
    @classmethod
    async def get_data(cls, app_id: str, entry_id: str, data_id: str) -> Dict:
        """获取单条数据"""
        response = await cls._client.post(
            f"/open/app/{app_id}/entry_data/get",
            json={"entry_id": entry_id, "data_id": data_id}
        )
        response.raise_for_status()
        return response.json()
    
    @classmethod
    async def update_data(cls, app_id: str, entry_id: str, 
                         data_id: str, data: Dict) -> Dict:
        """更新数据"""
        response = await cls._client.post(
            f"/open/app/{app_id}/entry_data/update",
            json={"entry_id": entry_id, "data_id": data_id, "data": data}
        )
        response.raise_for_status()
        return response.json()
    
    @classmethod
    async def delete_data(cls, app_id: str, entry_id: str, data_id: str) -> Dict:
        """删除数据"""
        response = await cls._client.post(
            f"/open/app/{app_id}/entry_data/delete",
            json={"entry_id": entry_id, "data_id": data_id}
        )
        response.raise_for_status()
        return response.json()
    
    @classmethod
    async def batch_create(cls, app_id: str, entry_id: str, 
                          data_list: List[Dict]) -> Dict:
        """批量创建数据"""
        response = await cls._client.post(
            f"/open/app/{app_id}/entry_data/batch_create",
            json={"entry_id": entry_id, "data_list": data_list}
        )
        response.raise_for_status()
        return response.json()
    
    @classmethod
    async def batch_update(cls, app_id: str, entry_id: str,
                          data_ids: List[str], data: Dict) -> Dict:
        """批量更新数据"""
        response = await cls._client.post(
            f"/open/app/{app_id}/entry_data/batch_update",
            json={"entry_id": entry_id, "data_ids": data_ids, "data": data}
        )
        response.raise_for_status()
        return response.json()
