#!/usr/bin/env python3
"""
工具验证脚本 - 检查工具目录结构和配置完整性

用法:
    verify_tool.py <tool_directory>

示例:
    verify_tool.py tools/weather_query
"""

import sys
import json
from pathlib import Path


REQUIRED_TOOL_JSON_FIELDS = {"name", "description", "params"}


def verify_tool(tool_path: str) -> tuple[bool, list[str]]:
    tool_dir = Path(tool_path)
    issues: list[str] = []

    tool_json = tool_dir / "tool.json"
    if not tool_json.exists():
        return False, ["未找到 tool.json"]

    try:
        config = json.loads(tool_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return False, [f"tool.json JSON 格式无效: {e}"]

    if not isinstance(config, dict):
        return False, ["tool.json 必须是 JSON 对象"]

    for field in REQUIRED_TOOL_JSON_FIELDS:
        if field not in config:
            issues.append(f"tool.json 缺少必需字段: {field}")

    name = config.get("name", "")
    if name and name != tool_dir.name:
        issues.append(f"tool.json name ({name}) 与目录名 ({tool_dir.name}) 不一致")

    if not config.get("description"):
        issues.append("description 为空，Agent 将无法理解工具用途")

    params = config.get("params", {})
    if not isinstance(params, dict):
        issues.append("params 必须是对象")
    else:
        for pname, pdef in params.items():
            if not isinstance(pdef, dict):
                issues.append(f"参数 {pname} 的定义必须是对象")
            elif "type" not in pdef:
                issues.append(f"参数 {pname} 缺少 type 字段")

    has_api = "api" in config
    has_main = (tool_dir / "main.py").exists()

    if not has_api and not has_main:
        issues.append("既无 api 配置也无 main.py — 工具没有执行逻辑")

    if has_main:
        main_content = (tool_dir / "main.py").read_text(encoding="utf-8")
        if "def execute" not in main_content:
            issues.append("main.py 未定义 execute 函数")

        lib_dir = tool_dir / "lib"
        if lib_dir.exists() and lib_dir.is_dir():
            if not (lib_dir / "__init__.py").exists():
                issues.append("lib/ 目录缺少 __init__.py")

    requires = config.get("requires_connections", [])
    if requires:
        for i, r in enumerate(requires):
            if not isinstance(r, dict):
                issues.append(f"requires_connections[{i}] 必须是对象")
                continue
            if "category" not in r:
                issues.append(f"requires_connections[{i}] 缺少 category 字段")
            fields = r.get("fields")
            if fields is not None and not isinstance(fields, list):
                issues.append(f"requires_connections[{i}].fields 必须是字符串数组")

    timeout = config.get("timeout")
    if timeout is not None:
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            issues.append("timeout 必须是正数")
        elif timeout > 600:
            issues.append("timeout 最大值为 600 秒")

    if issues:
        return False, issues
    return True, ["工具验证通过"]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python verify_tool.py <tool_directory>")
        sys.exit(1)

    valid, messages = verify_tool(sys.argv[1])
    for msg in messages:
        prefix = "✓" if valid else "✗"
        print(f"{prefix} {msg}")
    sys.exit(0 if valid else 1)
