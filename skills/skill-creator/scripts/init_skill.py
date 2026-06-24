#!/usr/bin/env python3
"""
技能初始化器 - 从模板创建新技能

用法:
    init_skill.py <skill-name>

示例:
    init_skill.py my-new-skill
    init_skill.py data-analyzer
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def _write_asset_meta(asset_dir: Path, *, default_author_type: str = "human_agent") -> None:
    """脚本直接落盘时同步写 meta.json — 让系统能追溯到"由谁、何时、经由谁"

    身份信息通过 ExecutionContext 注入的环境变量读取:
        CVO_USER_ID / CVO_AGENT_ID

    这样无论脚本是被 Agent 调用 (CVO_AGENT_ID 非空 → human_agent) 还是
    被 CLI 用户手动调用 (只有 CVO_USER_ID → human) 都能正确打标。
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
        # 任何异常不应阻断脚本主流程
        pass


SKILL_TEMPLATE = """---
name: {skill_name}
description: [待完成: 完整且信息丰富的说明，描述技能做什么以及何时使用。包括何时使用此技能 - 触发它的具体场景、文件类型或任务。]
---

# {skill_title}

## 概述

[待完成: 1-2 句话说明此技能能做什么]

## 技能结构设计

[待完成: 选择最适合此技能目的的结构。常见模式:

**1. 基于工作流**（最适合顺序流程）
- 示例: ## 概述 → ## 工作流决策树 → ## 步骤 1 → ## 步骤 2...

**2. 基于任务**（最适合工具集合）
- 示例: ## 概述 → ## 快速开始 → ## 任务类别 1 → ## 任务类别 2...

**3. 参考/指南**（最适合标准或规范）
- 示例: ## 概述 → ## 指南 → ## 规范 → ## 用法...

**4. 基于能力**（最适合集成系统）
- 示例: ## 概述 → ## 核心能力 → ### 1. 功能 → ### 2. 功能...

完成后删除整个"技能结构设计"部分。]

## [待完成: 根据选择的结构替换为第一个主要部分]

[待完成: 在此添加内容]

## 资源

### scripts/
可直接运行以执行特定操作的可执行代码。

### references/
旨在加载到上下文中以指导 Agent 过程和思考的文档。

### assets/
用于 Agent 生成的输出的模板和素材。

---

**不需要的目录可以删除。**
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
{skill_name} 的示例辅助脚本

替换为实际实现或在不需要时删除。
"""

def main():
    print("这是 {skill_name} 的示例脚本")

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# {skill_title} 参考文档

替换为实际参考内容或在不需要时删除。
"""


def title_case_skill_name(skill_name):
    """将连字符分隔的技能名称转换为标题大小写用于显示。"""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


KERNEL_MARKERS = ("core/skills/builtin", "core/subagents/builtin")


def init_skill(skill_name):
    """
    使用模板 SKILL.md 初始化新技能目录。

    技能创建在 skills/<skill-name> 下（相对于 cwd）。
    在 SaaS 模式下，cwd 中的 skills/ 是指向团队技能目录的符号链接，
    因此技能会自动安装到正确的团队资产目录中。
    """
    skill_dir = Path("skills") / skill_name

    resolved_str = str(skill_dir.resolve())
    for marker in KERNEL_MARKERS:
        if marker in resolved_str:
            print(f"错误: 禁止在内核目录创建技能: {skill_dir}")
            print(f"   内核目录为只读，由系统维护。")
            return None

    if skill_dir.exists():
        print(f"错误: 技能目录已存在: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"已创建技能目录: {skill_dir}")
    except Exception as e:
        print(f"创建目录错误: {e}")
        return None

    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("已创建 SKILL.md")
    except Exception as e:
        print(f"创建 SKILL.md 错误: {e}")
        return None

    try:
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("已创建 scripts/example.py")

        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'guide.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("已创建 references/guide.md")

        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
    except Exception as e:
        print(f"创建资源目录错误: {e}")
        return None

    # 写入 meta.json — 记录"这个资产是 Agent 通过脚本创建的"
    # 由于脚本运行在 Agent 的 ExecutionContext 中,能通过环境变量拿到身份信息
    _write_asset_meta(skill_dir, default_author_type="human_agent")

    print(f"\n技能 '{skill_name}' 初始化成功: {skill_dir}")
    print("\n后续步骤:")
    print("1. 编辑 SKILL.md 完成待完成项并更新描述")
    print("2. 自定义或删除 scripts/、references/ 中的示例文件")
    print(f"3. 测试: python skills/{skill_name}/scripts/example.py")

    return skill_dir


def main():
    if len(sys.argv) < 2:
        print("用法: init_skill.py <skill-name>")
        print("\n技能名称要求:")
        print("  - 连字符分隔的标识符（如 'data-analyzer'）")
        print("  - 仅限小写字母、数字和连字符")
        print("  - 最多 40 个字符")
        print("\n示例:")
        print("  init_skill.py my-new-skill")
        print("  init_skill.py data-analyzer")
        sys.exit(1)

    skill_name = sys.argv[1]

    print(f"正在初始化技能: {skill_name}")
    print()

    result = init_skill(skill_name)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
