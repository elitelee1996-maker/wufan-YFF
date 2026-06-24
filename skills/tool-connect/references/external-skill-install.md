# 从外部源批量安装技能

当接入一个完整生态（如飞书 CLI、钉钉 CLI）时，这些项目通常自带配套技能（SKILL.md 文件），提供各功能域的使用指南。本文档指导如何将这些外部技能安装到悟帆中。

## 从 GitHub 仓库安装

### 步骤 1：发现技能

浏览仓库，查找 `skills/` 目录下的技能文件：

```bash
# 通过 GitHub API 列出目录
bash("curl -s 'https://api.github.com/repos/{owner}/{repo}/contents/skills' | python3 -c 'import json,sys; [print(d[\"name\"]) for d in json.loads(sys.stdin.read()) if d[\"type\"]==\"dir\"]'")
```

或通过 `web_fetch` 浏览仓库页面识别技能列表。

### 步骤 2：评估兼容性

检查每个 SKILL.md 的 frontmatter 格式是否兼容：

- 必须有 `name` 和 `description` 字段
- 允许的 frontmatter 属性：`name`、`description`、`license`、`allowed-tools`、`metadata`
- `metadata` 下可以有任意嵌套字段（如 `metadata.requires.bins`），不影响兼容性

通常开源 CLI 项目的 Skill 格式与悟帆高度兼容（都遵循相同的 SKILL.md 规范）。

### 步骤 3：下载并安装

逐技能下载 SKILL.md 及其 references/ 子目录：

```python
# 伪代码 — 通过 GitHub raw URL 下载
for skill_name in skill_list:
    # 下载 SKILL.md
    content = web_fetch(f"https://raw.githubusercontent.com/{owner}/{repo}/main/skills/{skill_name}/SKILL.md")
    write(f"skills/{skill_name}/SKILL.md", content)

    # 下载 references/ 子目录中的文件
    for ref_file in ref_files:
        ref_content = web_fetch(f"https://raw.githubusercontent.com/{owner}/{repo}/main/skills/{skill_name}/references/{ref_file}")
        write(f"skills/{skill_name}/references/{ref_file}", ref_content)
```

实际操作中用 `web_fetch` 获取内容、`write` 写入文件。每个 `write("skills/xxx/SKILL.md", ...)` 会自动触发技能绑定到当前 Agent。

### 步骤 4：验证

安装后确认技能已生效：

```bash
ls skills/  # 查看已安装的技能列表
```

读取某个技能验证内容完整性：

```
read("skills/lark-calendar/SKILL.md")
```

## 步骤 5：注入工具使用引导（关键）

外部技能中的命令示例（如 `lark-cli calendar +agenda`）假设用户直接在终端执行。但在悟帆中，这些命令必须通过中转器工具执行，而不是直接在 bash 中调用。

**原因**：
- 中转器工具自动注入凭证(通过 `ctx.connections.get(slug).field(key)`)
- 中转器工具构造隔离的环境变量（多租户安全）
- 中转器工具自动解析 JSON 输出
- 直接在 bash 中调用 CLI 拿不到凭证（环境变量安全过滤会屏蔽 TOKEN/SECRET 等）

**安装外部技能时，必须在每个 SKILL.md 的正文开头（frontmatter 之后的第一行）插入工具使用引导**：

```markdown
> **重要**：本技能中所有 {cli_name} 命令通过 `{connector_tool_name}` 工具执行，
> 不要直接在 bash 中调用。
> 用法：{connector_tool_name}(command="命令内容，不含 {cli_name} 前缀")
```

例如，对飞书 CLI 的技能，插入：

```markdown
> **重要**：本技能中所有 lark-cli 命令通过 `lark_cli` 工具执行，
> 不要直接在 bash 中调用。
> 用法：lark_cli(command="calendar +agenda --format json")
```

这确保 Agent 在 Level 2 加载技能时第一眼就看到正确的调用方式。

## 从 ZIP 包安装

如果用户提供了 ZIP 或 .skill 文件：

```bash
cd skills && python3 -c "
import zipfile, sys
with zipfile.ZipFile(sys.argv[1]) as z:
    z.extractall()
" /path/to/skills.zip
```

## 注意事项

- 技能目录名必须是小写字母、数字和连字符（如 `lark-calendar`）
- `skills/` 路径自动路由到团队技能目录，同团队 Agent 共享
- 禁止在内核路径（`/app/core/skills/builtin`）下安装外部技能
- 安装后立即生效，无需重启
- 批量安装大量技能时（如 20 个），每个 `write` 调用都会触发自动绑定
