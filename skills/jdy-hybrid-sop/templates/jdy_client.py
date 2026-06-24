"""JDYClient - 简道云API标准客户端，含限流重试与自动分页"""
import time
import logging
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class JDYClient:
    """简道云 Open API 客户端封装"""

    def __init__(self, api_key: str, base_url: str, app_id: str) -> None:
        """初始化客户端。

        Args:
            api_key: 简道云 API Key
            base_url: API 基础地址
            app_id: 应用 ID
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.app_id = app_id
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    # ------------------------------------------------------------------
    # 内部：限流重试
    # ------------------------------------------------------------------
    def _request(self, method: str, path: str, max_retries: int = 3, **kwargs) -> Dict[str, Any]:
        """发送请求并处理限流重试。

        Args:
            method: HTTP 方法
            path: API 路径（不含 base_url）
            max_retries: 最大重试次数
            **kwargs: 传递给 requests 的额外参数

        Returns:
            响应 JSON
        """
        url = f"{self.base_url}{path}"
        for attempt in range(1, max_retries + 1):
            resp = self.session.request(method, url, **kwargs)
            if resp.status_code == 429:
                wait = min(2 ** attempt, 30)
                logger.warning("Rate limited, retry %d/%d after %ds", attempt, max_retries, wait)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError(f"Exceeded {max_retries} retries for {method} {url}")

    # ------------------------------------------------------------------
    # 数据 CRUD
    # ------------------------------------------------------------------
    def list_data(self, form_id: str, filter_cond: Optional[Dict] = None,
                  fields: Optional[List[str]] = None, limit: int = 100,
                  data_id: str = "") -> Dict[str, Any]:
        """查询表单数据列表（单页）。

        Args:
            form_id: 表单 ID
            filter_cond: 筛选条件
            fields: 返回字段列表
            limit: 每页条数 (1-100)
            data_id: 分页游标

        Returns:
            {"data": [...], "total_returned": N}
        """
        body: Dict[str, Any] = {"form_id": form_id, "limit": limit}
        if filter_cond:
            body["filter"] = filter_cond
        if fields:
            body["fields"] = fields
        if data_id:
            body["data_id"] = data_id
        return self._request("POST", "/api/v5/open/data/list", json=body)

    def get_data(self, form_id: str, data_id: str) -> Dict[str, Any]:
        """获取单条数据。

        Args:
            form_id: 表单 ID
            data_id: 数据 ID

        Returns:
            单条数据详情
        """
        body = {"form_id": form_id, "data_id": data_id}
        return self._request("POST", "/api/v5/open/data/get", json=body)

    def create_data(self, form_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建一条数据。

        Args:
            form_id: 表单 ID
            data: 字段键值对

        Returns:
            创建结果（含新数据 ID）
        """
        body = {"form_id": form_id, "data": data}
        return self._request("POST", "/api/v5/open/data/create", json=body)

    def update_data(self, form_id: str, data_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新一条数据。

        Args:
            form_id: 表单 ID
            data_id: 数据 ID
            data: 要更新的字段键值对

        Returns:
            更新结果
        """
        body = {"form_id": form_id, "data_id": data_id, "data": data}
        return self._request("POST", "/api/v5/open/data/update", json=body)

    # ------------------------------------------------------------------
    # 批量操作
    # ------------------------------------------------------------------
    def batch_create(self, form_id: str, data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量创建数据（单次上限100条）。

        Args:
            form_id: 表单 ID
            data_list: 数据列表

        Returns:
            批量创建结果
        """
        body = {"form_id": form_id, "data_list": data_list}
        return self._request("POST", "/api/v5/open/data/batch_create", json=body)

    def batch_update(self, form_id: str, updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量更新数据（单次上限100条）。

        Args:
            form_id: 表单 ID
            updates: [{"data_id": "...", "data": {...}}, ...]

        Returns:
            批量更新结果
        """
        body = {"form_id": form_id, "update_list": updates}
        return self._request("POST", "/api/v5/open/data/batch_update", json=body)

    # ------------------------------------------------------------------
    # 自动分页
    # ------------------------------------------------------------------
    def list_all(self, form_id: str, filter_cond: Optional[Dict] = None,
                 fields: Optional[List[str]] = None, max_records: int = 0) -> List[Dict[str, Any]]:
        """自动分页获取全部数据。

        Args:
            form_id: 表单 ID
            filter_cond: 筛选条件
            fields: 返回字段列表
            max_records: 最大记录数，0 表示不限制

        Returns:
            所有数据的列表
        """
        all_data: List[Dict[str, Any]] = []
        data_id = ""
        while True:
            result = self.list_data(form_id, filter_cond, fields, limit=100, data_id=data_id)
            records = result.get("data", [])
            all_data.extend(records)
            if max_records and len(all_data) >= max_records:
                return all_data[:max_records]
            if len(records) < 100:
                break
            data_id = records[-1].get("_id", "")
        return all_data

    # ------------------------------------------------------------------
    # 表单 & 通讯录
    # ------------------------------------------------------------------
    def get_widgets(self, form_id: str) -> Dict[str, Any]:
        """获取表单字段定义。

        Args:
            form_id: 表单 ID

        Returns:
            字段定义列表
        """
        return self._request("POST", "/api/v5/open/form/widgets", json={"form_id": form_id})

    def list_contacts(self, dept_id: str = "", offset: int = 0, limit: int = 100) -> Dict[str, Any]:
        """列出通讯录成员。

        Args:
            dept_id: 部门 ID（空字符串为根部门）
            offset: 偏移量
            limit: 每页条数

        Returns:
            成员列表
        """
        body: Dict[str, Any] = {"offset": offset, "limit": limit}
        if dept_id:
            body["dept_id"] = dept_id
        return self._request("POST", "/api/v5/open/contact/list", json=body)

    def search_contacts(self, keyword: str, limit: int = 50) -> List[Dict[str, Any]]:
        """搜索通讯录成员（带内存缓存）。

        Args:
            keyword: 搜索关键词
            limit: 最大返回数

        Returns:
            匹配的成员列表
        """
        cache_key = f"{keyword}:{limit}"
        if not hasattr(self, "_contact_cache"):
            self._contact_cache: Dict[str, List[Dict[str, Any]]] = {}
        if cache_key in self._contact_cache:
            return self._contact_cache[cache_key]
        result = self._request("POST", "/api/v5/open/contact/search",
                               json={"keyword": keyword, "limit": limit})
        members = result.get("members", [])
        self._contact_cache[cache_key] = members
        return members

    # ------------------------------------------------------------------
    # 静态工具方法
    # ------------------------------------------------------------------
    @staticmethod
    def safe_get(data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
        """安全地从嵌套字典中取值。

        Args:
            data: 源字典
            *keys: 逐层键名
            default: 缺失时的默认值

        Returns:
            取到的值或 default
        """
        current = data
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key, default)
            else:
                return default
        return current

    @staticmethod
    def build_filter(field: str, method: str, value: Any,
                     field_type: str = "text") -> Dict[str, Any]:
        """构建简道云筛选条件。

        Args:
            field: 字段名
            method: 筛选方法 (eq/ne/in/nin/like/range/gt/lt/empty/not_empty)
            value: 筛选值
            field_type: 字段类型

        Returns:
            可直接传入 list_data filter 参数的字典
        """
        return {
            "rel": "and",
            "cond": [{"field": field, "type": field_type, "method": method, "value": value}],
        }
