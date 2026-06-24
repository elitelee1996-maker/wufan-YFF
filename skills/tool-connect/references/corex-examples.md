# CoreX 工具完整示例集

## 1. 企业数据搜索（API + LLM 摘要）

tool.json:
```json
{
  "name": "enterprise_search",
  "description": "Search enterprise data, clean results, and generate summary. Returns summary text and saves clean data file.",
  "display_name": "企业数据搜索",
  "timeout": 180,
  "retry": 1,
  "dependencies": ["httpx"],
  "params": {
    "query": { "type": "string", "description": "Search keywords" },
    "save_raw": { "type": "boolean", "description": "Whether to also save raw data", "default": false }
  },
  "requires_connections": [
    { "category": "enterprise_data", "fields": ["api_key"], "required": true }
  ]
}
```

main.py:
```python
import json

async def execute(ctx, query="", save_raw=False, **_kw):
    api_key = ctx.connections.get("enterprise_data").field("api_key")

    await ctx.report_progress("正在查询数据...", 10)
    resp = await ctx.http.get(
        "https://data-vendor.com/api/search",
        params={"q": query, "limit": 100},
        headers={"Authorization": f"Bearer {api_key}"},
    )
    resp.raise_for_status()
    raw = resp.json()

    await ctx.report_progress("正在处理数据...", 50)
    if save_raw:
        ctx.save_file(f"raw_{query}.json", json.dumps(raw, ensure_ascii=False, indent=2))

    clean = [{"name": r["name"], "value": r["metric"]} for r in raw.get("results", [])]
    path = ctx.save_file(f"clean_{query}.json", json.dumps(clean, ensure_ascii=False, indent=2))

    await ctx.report_progress("正在生成摘要...", 80)
    summary = await ctx.call_llm(
        f"用中文概括以下查询结果的核心发现，不超过 300 字:\n{json.dumps(clean[:20], ensure_ascii=False)}"
    )

    return f"{summary}\n\n共 {len(clean)} 条结果，精简数据已保存: {path}"
```

## 2. 企业周报（确定性流程 + Agent 节点辅助趋势分析）

tool.json:
```json
{
  "name": "weekly_report",
  "description": "Generate weekly business report from data API. Fetches metrics, analyzes trends with context, and produces formatted report.",
  "display_name": "企业周报",
  "timeout": 300,
  "params": {
    "department": { "type": "string", "description": "Department name (e.g. sales, marketing)" },
    "week": { "type": "string", "description": "Week identifier (e.g. 2026-W11)", "default": "" }
  },
  "requires_connections": [
    { "category": "data_platform", "fields": ["api_key"], "required": true }
  ]
}
```

main.py:
```python
import json

async def execute(ctx, department="", week="", **_kw):
    api_key = ctx.connections.get("data_platform").field("api_key")

    await ctx.report_progress("正在拉取业务数据...", 10)
    resp = await ctx.http.get(
        f"https://data.company.com/api/metrics/{department}",
        params={"week": week, "compare": "wow"},
        headers={"Authorization": f"Bearer {api_key}"},
    )
    resp.raise_for_status()
    metrics = resp.json()

    await ctx.report_progress("正在处理数据...", 30)
    lines = []
    for m in metrics.get("items", []):
        change = f"+{m['wow_change']}%" if m.get("wow_change", 0) >= 0 else f"{m['wow_change']}%"
        lines.append(f"- {m['name']}: {m['value']} ({change})")
    summary_table = "\n".join(lines)

    await ctx.report_progress("正在分析业务趋势...", 50)
    analysis = await ctx.create_agent(
        f"以下是{department}部门{week}的核心指标及环比变化:\n{summary_table}\n"
        f"请搜索本周相关的行业动态和公司事件，结合数据趋势给出业务解读和建议。",
        tools=["web_search", "grep", "read"],
        max_iterations=8,
    )

    report = f"# {department}部门周报 ({week})\n\n## 核心指标\n{summary_table}\n\n## 趋势分析\n{analysis}"
    path = ctx.save_file(f"weekly_report_{department}_{week}.md", report)
    return f"周报已生成: {path}\n\n{report[:1000]}"
```

## 3. 库存异常处理（API 数据处理 + Agent 节点调查根因）

tool.json:
```json
{
  "name": "inventory_alert_handler",
  "description": "Process inventory anomaly alerts: fetch alert details from ERP, investigate root cause, and generate action plan.",
  "display_name": "库存异常处理",
  "timeout": 240,
  "params": {
    "alert_id": { "type": "string", "description": "Inventory alert ID from ERP system" }
  },
  "requires_connections": [
    { "category": "erp_platform", "fields": ["api_key"], "required": true }
  ]
}
```

main.py:
```python
import json

async def execute(ctx, alert_id="", **_kw):
    api_key = ctx.connections.get("erp_platform").field("api_key")

    resp = await ctx.http.get(
        f"https://erp.company.com/api/alerts/{alert_id}",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    resp.raise_for_status()
    alert = resp.json()

    sku = alert["sku"]
    logistics = await ctx.http.get(f"https://erp.company.com/api/logistics/{sku}/recent")
    orders = await ctx.http.get(f"https://erp.company.com/api/orders/{sku}/recent")
    context_data = (
        f"告警: {json.dumps(alert, ensure_ascii=False)}\n"
        f"物流: {logistics.text[:2000]}\n订单: {orders.text[:2000]}"
    )

    await ctx.report_progress("正在调查异常原因...", 50)
    investigation = await ctx.create_agent(
        f"库存异常调查:\n{context_data}\n"
        f"请定位根本原因并提出应对方案。可搜索 files/ 下的历史记录。",
        tools=["grep", "read", "web_search"],
        max_iterations=6,
    )

    report = f"# 库存异常报告\n\n**告警ID**: {alert_id}\n**SKU**: {sku}\n\n## 调查结果\n{investigation}"
    path = ctx.save_file(f"alert_{alert_id}_report.md", report)
    return f"报告已生成: {path}\n\n{investigation[:800]}"
```

## 4. REST API 薄壳连接器（如 Confluence / Jira）

核心理念：不限定固定的 API 路径和参数，封装认证和基础连接能力，由 Agent 动态决定具体调用。

tool.json:
```json
{
  "name": "confluence_api",
  "description": "Execute any Confluence REST API call. Agent decides the method, path, and parameters. Returns JSON response.",
  "display_name": "Confluence API",
  "description_zh": "Confluence REST API 通用调用",
  "timeout": 60,
  "params": {
    "method": { "type": "string", "description": "HTTP method: GET, POST, PUT, DELETE", "default": "GET" },
    "path": { "type": "string", "description": "REST API path, e.g. /rest/api/content/12345" },
    "query": { "type": "object", "description": "Query parameters as key-value pairs", "default": {} },
    "body": { "type": "object", "description": "Request body for POST/PUT", "default": {} }
  },
  "requires_connections": [
    { "category": "confluence", "fields": ["base_url", "api_token"], "required": true }
  ]
}
```

main.py:
```python
import json

async def execute(ctx, method="GET", path="", query=None, body=None, **_kw):
    base_url = ctx.connections.get("confluence").field("base_url").rstrip("/")
    token = ctx.connections.get("confluence").field("api_token")

    url = f"{base_url}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    if method.upper() in ("GET", "DELETE"):
        resp = await ctx.http.request(method.upper(), url, params=query or {}, headers=headers)
    else:
        resp = await ctx.http.request(method.upper(), url, params=query or {}, json=body or {}, headers=headers)

    if resp.status_code >= 400:
        return f"API Error {resp.status_code}: {resp.text[:1000]}"

    try:
        data = resp.json()
        return json.dumps(data, ensure_ascii=False, indent=2)[:ctx._max_result or 25000]
    except Exception:
        return resp.text[:5000]
```

Agent 使用时自由决定调用路径：
```
confluence_api(method="GET", path="/rest/api/content/12345", query={"expand": "body.storage"})
confluence_api(method="GET", path="/rest/api/search", query={"cql": "space=DEV AND type=page"})
confluence_api(method="POST", path="/rest/api/content", body={"type": "page", "title": "...", ...})
```

## 5. CLI 薄壳连接器（如飞书 CLI / 钉钉 CLI）

核心理念：封装 CLI 二进制 + 凭证注入 + 环境隔离，Agent 动态决定命令内容。

tool.json:
```json
{
  "name": "lark_cli",
  "description": "Execute any lark-cli command with proper credential injection. Agent decides the command. Returns JSON output.",
  "display_name": "飞书 CLI",
  "description_zh": "飞书 CLI 命令执行",
  "timeout": 120,
  "params": {
    "command": { "type": "string", "description": "lark-cli command without the 'lark-cli' prefix, e.g. 'calendar +agenda --format json'" }
  },
  "requires_connections": [
    { "category": "lark", "fields": ["app_id", "app_secret", "user_token"], "required": true }
  ]
}
```

main.py:
```python
import asyncio
import json
import os

async def execute(ctx, command="", **_kw):
    # 持久化 HOME：per-user 隔离，lark-cli 的配置和 auth 状态跨调用保留
    tool_home = ctx.get_tool_home()

    # 首次使用时初始化 lark-cli 配置
    _ensure_lark_config(tool_home, ctx.connections.get("lark"))

    env = {
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "HOME": str(tool_home),
        "LANG": "en_US.UTF-8",
    }

    full_cmd = f"lark-cli {command}"
    if "--format" not in command:
        full_cmd += " --format json"

    proc = await asyncio.create_subprocess_shell(
        full_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=env,
    )
    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=100)

    if proc.returncode != 0:
        err = stderr.decode("utf-8", errors="replace")
        if "not found" in err.lower() or "command not found" in err.lower():
            return "错误: lark-cli 未安装。请先执行 bash('npm install -g @larksuite/cli') 安装。"
        return f"命令执行失败 (exit {proc.returncode}):\n{err[:2000]}"

    output = stdout.decode("utf-8", errors="replace")
    try:
        data = json.loads(output)
        return json.dumps(data, ensure_ascii=False, indent=2)[:25000]
    except json.JSONDecodeError:
        return output[:5000]


def _ensure_lark_config(tool_home, conn):
    """首次使用时用 lark-cli config init 写入配置。已存在则跳过。"""
    import subprocess
    config_dir = tool_home / ".lark-cli"
    if (config_dir / "config.json").exists():
        return
    app_id = conn.field("app_id", default="")
    app_secret = conn.field("app_secret", default="")
    if not app_id or not app_secret:
        return
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": str(tool_home), "LANG": "en_US.UTF-8"}
    proc = subprocess.run(
        f'echo "{app_secret}" | lark-cli config init --app-id "{app_id}" --app-secret-stdin --brand feishu',
        shell=True, env=env, capture_output=True, timeout=15,
    )
```

Agent 使用时自由决定命令内容：
```
lark_cli(command="calendar +agenda")
lark_cli(command="im +messages-send --chat-id oc_xxx --text '会议改到下午3点'")
lark_cli(command="docs +create --title '周报' --markdown '# 本周进展\n- 完成X功能'")
```

## 6. 复杂工具编排（工具互调）

```python
import json

async def execute(ctx, topic="", **_kw):
    await ctx.report_progress("搜索相关文件...")

    search_result = await ctx.call_tool("grep", pattern=topic, path="files/")

    if "No matches" in search_result:
        web_data = await ctx.http.get(f"https://api.example.com/search?q={topic}")
        raw = web_data.json()
        ctx.save_file(f"{topic}_research.json", json.dumps(raw, ensure_ascii=False))

    await ctx.report_progress("生成分析报告...", 60)
    report = await ctx.call_llm(
        f"基于以下数据生成分析报告:\n{search_result[:3000]}",
        json_mode=True
    )

    path = ctx.save_file(f"{topic}_report.md", report)
    return f"报告已生成: {path}"
```
