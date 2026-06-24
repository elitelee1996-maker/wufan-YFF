# 子模块拆分规范（lib/）

当工具逻辑复杂（超过约 200 行，或包含 3 个以上独立关注点）时，将代码拆分到 `lib/` 子目录。`main.py` 负责编排流程，`lib/` 中的模块各自处理独立的关注点。

## 什么时候用 lib/

| 场景 | 用什么 |
|------|--------|
| 逻辑简单，一个函数搞定 | 单文件 `main.py` |
| 多个 API + 数据清洗 + LLM 处理 | `main.py` + `lib/` |
| 并行调用多个外部服务 + 结果聚合 | `main.py` + `lib/` |

## 目录规范

```
tools/{name}/
├── tool.json
├── main.py                # 入口，必须定义 execute(ctx, **params)
└── lib/                   # 固定用 lib/ 作为子模块目录名
    ├── __init__.py        # 必须有，可以为空文件
    ├── api_client.py      # 示例：封装外部 API 交互
    └── formatter.py       # 示例：数据格式化
```

## 关键约束

- 子模块目录统一命名为 `lib/`，不要用 `utils/`、`helpers/` 等其他名称
- `lib/` 内必须包含 `__init__.py`（内容可为空）
- `main.py` 必须定义 `execute(ctx, **params)` 入口函数
- 将 `ctx` 作为参数传递给 lib 模块中的函数，使其能访问平台能力
- **禁止**手动操作 `sys.path`，CoreX 引擎自动处理模块导入路径
- **禁止**通过 `os.environ.get()` 读取凭据,应使用 `ctx.connections.get(slug).field(key)`

## 完整示例：企业概况查询（多 API + LLM 消歧 + 数据聚合）

tool.json:
```json
{
  "name": "company_overview",
  "description": "Query comprehensive company profile by name. Resolves ambiguous names via LLM, fetches business registration, CRM records, and financial data in parallel.",
  "display_name": "企业概况查询",
  "timeout": 180,
  "params": {
    "name": { "type": "string", "description": "Company name to search for" }
  },
  "requires_connections": [
    { "category": "data_platform", "fields": ["api_key"], "required": true },
    { "category": "crm_platform", "fields": ["app_code"], "required": true }
  ]
}
```

main.py:
```python
import asyncio
from lib.resolver import resolve_company
from lib.data_fetcher import fetch_profile, fetch_crm
from lib.formatter import build_report

async def execute(ctx, name="", **_kw):
    await ctx.report_progress("正在匹配企业...", 10)
    company = await resolve_company(ctx, name)

    await ctx.report_progress("正在采集数据...", 40)
    profile, crm = await asyncio.gather(
        fetch_profile(ctx, company["credit_code"]),
        fetch_crm(ctx, company["credit_code"]),
    )

    report = build_report(company, profile, crm)
    path = ctx.save_file(f"{name}_overview.md", report)
    return f"报告已生成: {path}\n\n{report[:1500]}"
```

lib/\_\_init\_\_.py:
```python
```

lib/resolver.py:
```python
async def resolve_company(ctx, name: str) -> dict:
    resp = await ctx.http.get(
        "https://data-api.example.com/company/search",
        params={"keyword": name},
        headers={"Authorization": f"Bearer {ctx.connections.get("data_platform").field("api_key")}"},
    )
    resp.raise_for_status()
    candidates = resp.json().get("items", [])

    if len(candidates) == 1:
        return candidates[0]

    choice = await ctx.call_llm(
        f"用户搜索: {name}\n候选企业:\n"
        + "\n".join(f"{i+1}. {c['name']} ({c.get('credit_code','')})" for i, c in enumerate(candidates))
        + "\n\n请返回最匹配的企业序号（仅数字）。",
    )
    idx = int(choice.strip()) - 1
    return candidates[max(0, min(idx, len(candidates) - 1))]
```

lib/data_fetcher.py:
```python
async def fetch_profile(ctx, credit_code: str) -> dict:
    resp = await ctx.http.get(
        f"https://data-api.example.com/company/{credit_code}/profile",
        headers={"Authorization": f"Bearer {ctx.connections.get("data_platform").field("api_key")}"},
    )
    resp.raise_for_status()
    return resp.json()

async def fetch_crm(ctx, credit_code: str) -> dict:
    resp = await ctx.http.get(
        f"https://crm.example.com/api/customer/{credit_code}",
        headers={"AppCode": ctx.connections.get("crm_platform").field("app_code")},
    )
    if resp.status_code == 404:
        return {"found": False}
    resp.raise_for_status()
    return resp.json()
```

lib/formatter.py:
```python
def build_report(company: dict, profile: dict, crm: dict) -> str:
    lines = [
        f"# {company['name']}",
        f"统一社会信用代码: {company.get('credit_code', 'N/A')}",
        "",
        "## 工商信息",
        f"- 法定代表人: {profile.get('legal_person', 'N/A')}",
        f"- 注册资本: {profile.get('registered_capital', 'N/A')}",
        f"- 经营状态: {profile.get('status', 'N/A')}",
    ]
    if crm.get("found"):
        lines += ["", "## CRM 记录", f"- 客户等级: {crm.get('level', 'N/A')}"]
    return "\n".join(lines)
```

## 写入路径

通过 write 工具写入：

- `tools/{name}/lib/__init__.py`
- `tools/{name}/lib/{module}.py`
