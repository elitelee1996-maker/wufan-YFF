#!/usr/bin/env python3
"""
工具初始化器 - 从模板创建新工具

用法:
    init_tool.py <tool-name> [--corex]

示例:
    init_tool.py weather_query          # 声明式 API 工具
    init_tool.py enterprise_search --corex  # 脚本式 CoreX 工具
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def _write_asset_meta(asset_dir: Path, *, default_author_type: str = "human_agent") -> None:
    """创建资产后同步写入 meta.json,记录"谁、何时、经由哪个 Agent"

    环境变量 CVO_USER_ID / CVO_AGENT_ID 由 bash.py 注入。
    """
    try:
        meta_file = asset_dir / "meta.json"
        if meta_file.exists():
            return
        user_id = os.environ.get("CVO_USER_ID", "").strip()
        agent_id = os.environ.get("CVO_AGENT_ID", "").strip()
        if agent_id:
            author_type = "human_agent"
        elif user_id:
            author_type = "human"
        else:
            author_type = default_author_type
        payload = {
            "author_type": author_type,
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        if user_id:
            payload["created_by"] = user_id
        if agent_id:
            payload["created_by_agent_id"] = agent_id
        meta_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


API_TOOL_JSON = """{
  "name": "{tool_name}",
  "description": "[TODO: English description — what it does, what it returns]",
  "display_name": "[TODO: 中文显示名]",
  "description_zh": "[TODO: 中文简介]",
  "params": {
    "query": {
      "type": "string",
      "description": "[TODO: Parameter description]"
    }
  },
  "api": {
    "url": "[TODO: API endpoint URL — 支持 {conn:<slug>.<field>} 占位符注入凭据]",
    "method": "GET",
    "params_mapping": {}
  },
  "requires_connections": [
    { "category": "[TODO: connection slug]", "fields": ["api_key"], "required": true }
  ]
}"""

COREX_TOOL_JSON = """{
  "name": "{tool_name}",
  "description": "[TODO: English description — what it does, what it returns]",
  "display_name": "[TODO: 中文显示名]",
  "description_zh": "[TODO: 中文简介]",
  "timeout": 120,
  "params": {
    "query": {
      "type": "string",
      "description": "[TODO: Parameter description]"
    }
  },
  "requires_connections": [
    { "category": "[TODO: connection slug]", "fields": ["api_key"], "required": true }
  ]
}"""

COREX_MAIN_PY = '''async def execute(ctx, query="", **_kw):
    # 替换 "your_service" 为实际连接器 slug(通过 connection_credential 工具声明)
    conn = ctx.connections.get("your_service")
    api_key = conn.field("api_key")

    await ctx.report_progress("正在处理...", 10)

    resp = await ctx.http.get(
        "[TODO: API URL]",
        params={"q": query},
        headers={"Authorization": f"Bearer {api_key}"},
    )
    resp.raise_for_status()
    data = resp.json()

    # [TODO: 数据处理逻辑]

    return str(data)
'''


KERNEL_MARKERS = ("core/skills/builtin", "core/subagents/builtin", "core/tools/builtin")


def init_tool(tool_name: str, corex: bool = False):
    tool_dir = Path("tools") / tool_name

    resolved_str = str(tool_dir.resolve())
    for marker in KERNEL_MARKERS:
        if marker in resolved_str:
            print(f"错误: 禁止在内核目录创建工具: {tool_dir}")
            return None

    if tool_dir.exists():
        print(f"错误: 工具目录已存在: {tool_dir}")
        return None

    try:
        tool_dir.mkdir(parents=True, exist_ok=False)
        print(f"已创建工具目录: {tool_dir}")
    except Exception as e:
        print(f"创建目录错误: {e}")
        return None

    template = COREX_TOOL_JSON if corex else API_TOOL_JSON
    tool_json_content = template.replace("{tool_name}", tool_name)

    tool_json_path = tool_dir / "tool.json"
    try:
        tool_json_path.write_text(tool_json_content, encoding="utf-8")
        print("已创建 tool.json")
    except Exception as e:
        print(f"创建 tool.json 错误: {e}")
        return None

    if corex:
        main_py_path = tool_dir / "main.py"
        try:
            main_py_path.write_text(COREX_MAIN_PY, encoding="utf-8")
            print("已创建 main.py")
        except Exception as e:
            print(f"创建 main.py 错误: {e}")
            return None

    # 写入 meta.json — 记录资产来源(Agent/人类/共创)
    _write_asset_meta(tool_dir, default_author_type="human_agent")

    mode = "CoreX（脚本式）" if corex else "API（声明式）"
    print(f"\n工具 '{tool_name}' 初始化成功（{mode}）: {tool_dir}")
    print("\n后续步骤:")
    print("1. 编辑 tool.json 完成 [TODO] 项")
    if corex:
        print("2. 编辑 main.py 实现业务逻辑")
    print(f"{'3' if corex else '2'}. 配置密钥（如需要）")
    print(f"{'4' if corex else '3'}. 验证工具可用性")

    return tool_dir


def main():
    if len(sys.argv) < 2:
        print("用法: init_tool.py <tool-name> [--corex]")
        print("\n示例:")
        print("  init_tool.py weather_query          # 声明式 API 工具")
        print("  init_tool.py enterprise_search --corex  # 脚本式 CoreX 工具")
        sys.exit(1)

    tool_name = sys.argv[1]
    corex = "--corex" in sys.argv

    print(f"正在初始化工具: {tool_name}")
    print()

    result = init_tool(tool_name, corex=corex)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
