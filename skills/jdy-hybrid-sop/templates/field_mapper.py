"""FieldMapper - 配置驱动的字段映射访问器 (v2.0)

兼容两种 JSON 格式：
1. jdy_gen_field_mapping 工具自动生成格式（key = widget_id）
2. 手动语义化格式（key = 业务语义名，字段内含 widget_id）
"""
import json
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class FieldMapper:
    """从 field_mapping.json 加载映射配置，提供语义化字段访问。

    JSON 结构示例 (jdy_gen_field_mapping 自动生成格式)::

        {
          "app_id": "app_abc123def456",
          "version": "1.0.0",
          "generated_at": "2026-06-13T10:30:00",
          "forms": {
            "6a221e50149908216c2d30a6": {
              "form_name": "pur_采购订单",
              "entry_id": "6a221e50149908216c2d30a6",
              "fields": {
                "_widget_1780620881780": {
                  "widget": "_widget_1780620881780",
                  "type": "text",
                  "label": "采购单号"
                },
                "_widget_1780620881781": {
                  "widget": "_widget_1780620881781",
                  "type": "number",
                  "label": "订单金额"
                }
              }
            }
          }
        }

    JSON 结构示例 (手动语义化格式，向后兼容)::

        {
          "app_id": "app_abc123def456",
          "version": "1.0.0",
          "forms": {
            "order": {
              "form_name": "pur_采购订单",
              "entry_id": "6a221e50149908216c2d30a6",
              "fields": {
                "order_no": {
                  "widget_id": "_widget_1780620881780",
                  "type": "text",
                  "label": "采购单号"
                },
                "amount": {
                  "widget_id": "_widget_1780620881781",
                  "type": "number",
                  "label": "订单金额"
                }
              }
            }
          }
        }
    """

    def __init__(self, mapping_path: str) -> None:
        """加载字段映射配置。

        Args:
            mapping_path: field_mapping.json 文件路径
        """
        self.mapping_path = mapping_path
        with open(mapping_path, "r", encoding="utf-8") as f:
            self._config: Dict[str, Any] = json.load(f)
        self._forms: Dict[str, Any] = self._config.get("forms", {})
        self._app_id: str = self._config.get("app_id", "")
        self._version: str = self._config.get("version", "1.0.0")
        logger.info("FieldMapper loaded %d forms from %s", len(self._forms), mapping_path)

    # ------------------------------------------------------------------
    # 核心访问方法
    # ------------------------------------------------------------------
    def widget_id(self, form_key: str, field_key: str) -> str:
        """获取字段的 widget_id（即 _widget_xxx，用于 API 调用）。

        自动适配两种格式：
        - 自动生成格式：key 本身就是 widget_id，字段中 widget 也是 widget_id
        - 语义化格式：字段中有 widget_id 属性

        Args:
            form_key: 表单键（entry_id 或语义键如 "order"）
            field_key: 字段键（widget_id 或语义键如 "customer"）

        Returns:
            widget_id 字符串（如 "_widget_1780620881780"）

        Raises:
            KeyError: 表单或字段不存在
        """
        field_entry = self._forms[form_key]["fields"][field_key]
        # 优先取显式 widget_id，否则取 widget（自动生成格式中 widget = widget_id）
        return field_entry.get("widget_id") or field_entry.get("widget", "")

    def field_type(self, form_key: str, field_key: str) -> str:
        """获取字段的控件类型。

        Args:
            form_key: 表单键
            field_key: 字段键

        Returns:
            控件类型字符串（如 "text", "number", "datetime"）

        Raises:
            KeyError: 表单或字段不存在
        """
        field_entry = self._forms[form_key]["fields"][field_key]
        return field_entry.get("type", field_entry.get("widget", "unknown"))

    def entry_id(self, form_key: str) -> str:
        """获取表单的 entry_id（简道云表单唯一标识）。

        Args:
            form_key: 表单键

        Returns:
            entry_id 字符串

        Raises:
            KeyError: 表单不存在
        """
        form = self._forms[form_key]
        return form.get("entry_id", form.get("form_id", ""))

    def form_name(self, form_key: str) -> str:
        """获取表单的中文显示名称。

        Args:
            form_key: 表单键

        Returns:
            表单中文名称

        Raises:
            KeyError: 表单不存在
        """
        return self._forms[form_key]["form_name"]

    def field_label(self, form_key: str, field_key: str) -> str:
        """获取字段的中文标签。

        Args:
            form_key: 表单键
            field_key: 字段键

        Returns:
            字段中文标签

        Raises:
            KeyError: 表单或字段不存在
        """
        return self._forms[form_key]["fields"][field_key]["label"]

    def app_id(self) -> str:
        """获取应用 ID。"""
        return self._app_id

    # ------------------------------------------------------------------
    # 子表单支持
    # ------------------------------------------------------------------
    def subform_items(self, form_key: str, field_key: str) -> Dict[str, Any]:
        """获取子表单的子字段映射。

        Args:
            form_key: 表单键
            field_key: 子表单字段键

        Returns:
            子字段字典

        Raises:
            KeyError: 表单或字段不存在
            ValueError: 字段不是子表单类型
        """
        field_entry = self._forms[form_key]["fields"][field_key]
        if field_entry.get("type") != "subform":
            raise ValueError(f"Field '{field_key}' is not a subform")
        return field_entry.get("items", {})

    # ------------------------------------------------------------------
    # 批量查询
    # ------------------------------------------------------------------
    def list_forms(self) -> List[str]:
        """列出所有表单键。"""
        return list(self._forms.keys())

    def list_fields(self, form_key: str) -> List[str]:
        """列出指定表单的所有字段键。"""
        return list(self._forms[form_key]["fields"].keys())

    def get_all_widget_ids(self, form_key: str) -> Dict[str, str]:
        """获取指定表单所有字段的 widget_id 映射。

        Returns:
            {field_key: widget_id} 字典
        """
        result = {}
        for fk in self._forms[form_key]["fields"]:
            result[fk] = self.widget_id(form_key, fk)
        return result

    # ------------------------------------------------------------------
    # 向后兼容（v1.0 方法别名）
    # ------------------------------------------------------------------
    def widget(self, form_key: str, field_key: str) -> str:
        """[已弃用] 获取字段控件类型。请使用 field_type()。"""
        return self.field_type(form_key, field_key)

    def form_id(self, form_key: str) -> str:
        """[已弃用] 获取表单 ID。请使用 entry_id()。"""
        return self.entry_id(form_key)

    # ------------------------------------------------------------------
    # 验证
    # ------------------------------------------------------------------
    def validate(self) -> bool:
        """验证映射配置的完整性。

        检查每个表单是否包含必要字段：form_name, entry_id, fields。
        检查每个字段是否包含 label 和 widget/widget_id。

        Returns:
            True 表示验证通过

        Raises:
            ValueError: 配置不完整时抛出，附带具体缺失信息
        """
        errors: list = []
        required_form_keys = {"form_name", "fields"}
        # entry_id 或 form_id 至少有一个
        form_id_keys = {"entry_id", "form_id"}
        # widget_id 或 widget 至少有一个
        field_id_keys = {"widget_id", "widget"}

        for fk, form_cfg in self._forms.items():
            # 检查表单级必要字段
            missing = required_form_keys - set(form_cfg.keys())
            if missing:
                errors.append(f"Form '{fk}' missing keys: {missing}")
                continue

            # 检查 entry_id 存在
            if not form_cfg.get("entry_id") and not form_cfg.get("form_id"):
                errors.append(f"Form '{fk}' missing entry_id or form_id")

            # 检查字段级
            for field_k, field_cfg in form_cfg["fields"].items():
                if "label" not in field_cfg:
                    errors.append(f"Form '{fk}' field '{field_k}' missing: label")
                if not (field_cfg.get("widget_id") or field_cfg.get("widget")):
                    errors.append(f"Form '{fk}' field '{field_k}' missing: widget_id or widget")

                # 子表单检查 items
                if field_cfg.get("type") == "subform" and "items" not in field_cfg:
                    errors.append(f"Form '{fk}' subform '{field_k}' missing: items")

        if errors:
            msg = "Field mapping validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            raise ValueError(msg)

        logger.info("Field mapping validation passed (%d forms, %d total fields)",
                     len(self._forms),
                     sum(len(f["fields"]) for f in self._forms.values()))
        return True
