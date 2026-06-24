---
name: 工具与连接
description: 工具创建与外部服务连接的完整指南。当用户想要接入外部服务、连接 API 或 CLI、创建自定义工具、管理外部服务凭据(API Key / Token / OAuth / 账号),或提到任何需要外部服务授权的场景时使用。凭据统一通过 `connection_credential` 工具和连接中心管理。涵盖从简单 API 转发到复杂生态接入的全谱系。
---

# 工具与连接

本技能指导你创建自定义工具和接入外部服务——将 HTTP API、CLI 工具或任何外部能力封装为 Agent 可调用的工具。

## 两种实现模式

- **声明式**：仅 `tool.json`，配置 HTTP 请求，零代码。适合直接转发外部 API。
- **脚本式（CoreX）**：`tool.json` + `main.py`，可编程。适合需要数据处理、多步编排、调 CLI、生成内容等场景。

判断原则：只需发一个 HTTP 请求并原样返回 → 声明式。其他一切 → 脚本式。

## ⚠️ 【最高优先级】读取凭据的三种上下文(别搞错)

悟帆里读连接中心的凭据,**上下文不同写法完全不同**。搞错了会连续报错浪费 token:

| 你在哪写代码 | 怎么读凭据 | 为什么 |
|---|---|---|
| **自定义工具 `tools/<name>/main.py`** 的 `execute(ctx, ...)` 里 | `ctx.connections.get("<slug>").field("<key>")` | `ctx` 是工具的入参,只在这里存在 |
| **execute_python / execute_code / bash**(无需建工具,临时跑脚本) | 用环境变量 `$CVO_CONN_<SLUG_UPPER>_<FIELD_UPPER>` | 这些是独立子进程,**没有 `ctx` 变量** |
| **tool.json 声明式 API 工具**(url / headers / query) | `${conn:<slug>.<field>}` 占位符 | 平台运行时自动替换 |

**一次性示例**(对 `openweather` 的 `api_key`):

```bash
# ✓ 【推荐】一次性查询优先用 bash + curl(系统自带,零依赖):
curl "https://api.openweathermap.org/data/2.5/weather?q=Hangzhou&appid=$CVO_CONN_OPENWEATHER_API_KEY&units=metric"
```

```python
# ✓ 需要复杂数据处理时用 execute_python:
import os, httpx   # 用 httpx,不要用 requests(子进程未必装)
key = os.environ["CVO_CONN_OPENWEATHER_API_KEY"]
r = httpx.get("https://api.openweathermap.org/data/2.5/weather",
              params={"q": "Hangzhou", "appid": key, "units": "metric"})
print(r.json())
```

**常见错误**(浪费你 token):
- ✗ 在 execute_python / execute_code / bash 里用 `ctx.connections` → `NameError: name 'ctx' is not defined`
  (ctx 只在自定义工具 main.py 里存在)
- ✗ 在 execute_python 里 `import requests` → `ModuleNotFoundError`
  (子进程不一定装 requests,请用 `httpx` / `urllib`)
- ✗ 在 bash 里 `python3 << EOF` 启动的又是系统 python3,依赖也不全。
  **宁可直接 `curl`,或用 `execute_python`(走 venv + httpx)**

判断规则: **"我要不要沉淀成长期可复用的工具?"**
- 要 → 建 `tools/<name>/main.py`,用 `ctx.connections`
- 不要(一次性查询)→ 直接在 bash + curl / execute_python + httpx,读 `$CVO_CONN_*`

## 核心约束（强制）

1. **外部服务凭据**:涉及任何外部服务凭据(API Key / Token / 账号等)时,
   使用 `connection_credential` 工具管理 —— 参见本文下方"**外部服务凭据**"章节。
   **读凭据的三种写法见上方表格**,按上下文选对。
2. **验证交付**：工具创建后必须至少执行一次验证调用，确认功能正常。
3. **路径规范**：工具写入 `tools/{name}/` 目录。目录名必须与 `tool.json` 中 `name` 字段一致。

## 步骤 1：判断意图

用户要做什么？

### A. 做一个独立功能

每日名言、数据计算、文本处理等——不涉及外部服务连接。直接进入步骤 2。

### B. 接通一个外部服务

Confluence、天气 API、企业内部系统、GitHub API 等——核心是封装认证和连接能力。

- 理解服务的 API 文档或认证方式
- 阅读 `references/service-connector.md` 获取服务连接器的设计模式和模板
- 进入步骤 2

### C. 接入一个完整生态

飞书 CLI、钉钉 CLI 等——不仅要建工具，还要安装配套技能。

- 分析外部仓库/文档，识别有哪些配套技能
- 阅读 `references/external-skill-install.md` 了解如何批量安装外部技能
- 阅读 `references/service-connector.md` 获取连接器模板
- 进入步骤 2

## 步骤 2：选择实现方式

问自己：核心逻辑是什么？

**声明式**——纯粹转发一个 HTTP API（输入 → 请求 → 原样返回，无自定义逻辑）：

- 只需 `tool.json`，无需 `main.py`
- 阅读 `references/tool-json-spec.md` 获取完整字段规范和示例

**脚本式**——需要自定义逻辑，包括但不限于：

- 调 HTTP API + 数据后处理（如 Confluence 知识库封装）
- 调 CLI 二进制 + 解析输出（如飞书/钉钉 CLI 中转）
- 多步编排、LLM 调用、生成内容、写文件
- `tool.json` + `main.py`
- 阅读 `references/tool-json-spec.md` 获取 tool.json 规范
- 阅读 `references/corex-api.md` 获取 ToolContext 完整 API
- 复杂工具可阅读 `references/corex-examples.md` 获取完整示例
- 需要拆分子模块时阅读 `references/lib-pattern.md`

## 步骤 3:外部服务凭据

如果工具需要任何外部服务凭据(API Key / Token / OAuth / 实例地址 等),
通过 `connection_credential` 工具的两步法建立连接器:

**第一步:声明连接器**

```
connection_credential(
  action="declare",
  display_name="OpenWeather",          # 必填,用户看到的名字
  slug="openweather",                   # 可选,不传则从 display_name 自动派生
  description="调用 OpenWeather API 查天气",
  fields=[
    {
      "key": "api_key",                  # 代码里 conn.field("api_key")
      "label": "API Key",
      "type": "secret",                  # secret / text / url / email
      "owner_level": "user",             # team(管理员配,全员共享) / user(每人各填)
      "required": true,
      "hint": "在 openweathermap.org/api_keys 获取"
    }
  ]
)
```

- 若 slug 已在内置 Registry(feishu / github / notion / slack / atlassian 等)
  或团队已有自定义连接器 → 自动复用,此时不需传 fields
- 新的连接器才需提供 fields 定义

**第二步:在 tool.json 中声明依赖**

```json
"requires_connections": [
  { "category": "<slug>", "fields": ["api_key", ...], "required": true }
]
```

**第三步:代码中使用凭据**

```python
# main.py
async def execute(ctx, **params):
    conn = ctx.connections.get("openweather")
    api_key = conn.field("api_key")
    ...
```

**第四步:在合适时机让用户填写**

```
connection_credential(action="request", slug="openweather",
                      reason="需要 OpenWeather 才能查天气")
```

前端会弹出连接卡,用户点击后打开连接面板填字段 —— 不需要你在对话中询问明文。

**字段所有权判断**:
- `team` — 空间管理员配一次全员共享(公共 API key / 企业账号 / 实例 URL)
- `user` — 每个成员各自填(个人 Access Token / 权限相关凭据)

不确定时,询问用户:"这个 key 是团队共享一个,还是每个人各自有?"

### 另外一种使用方式:直接在 bash / execute_python 里拿

如果你要临时写脚本验证一下凭据是否工作,或者帮用户跑一次性查询(不沉淀为工具),
可以直接通过**环境变量**读取已接入的连接器字段:

变量命名规则:`CVO_CONN_<SLUG_UPPER>_<FIELD_UPPER>`

```bash
# 在 bash 里:
curl "https://api.openweathermap.org/data/2.5/weather?q=Beijing&appid=$CVO_CONN_OPENWEATHER_API_KEY"
```

```python
# 在 execute_python 里:
import os, httpx
api_key = os.environ["CVO_CONN_OPENWEATHER_API_KEY"]
r = httpx.get("https://api.openweathermap.org/data/2.5/weather",
              params={"q": "Beijing", "appid": api_key, "units": "metric"})
print(r.json())
```

这样即使不走工具路径,你也能用用户连接中心里的凭证,替用户完成一次任务。

## 步骤 4：验证

工具创建后必须至少执行一次验证调用。验证失败时阅读 `references/troubleshooting.md` 排查。

## 工具结构速查

```
tools/
├── weather_query/
│   └── tool.json              # 声明式
├── confluence_api/
│   ├── tool.json              # 脚本式
│   └── main.py
├── company_overview/
│   ├── tool.json              # 脚本式 + 子模块
│   ├── main.py
│   └── lib/
│       ├── __init__.py
│       ├── api_client.py
│       └── formatter.py
└── jiandaoyun/                # 工具包
    ├── pack.json
    ├── search_data/
    │   └── tool.json
    └── write_data/
        ├── tool.json
        └── main.py
```

## tool.json 核心字段

```json
{
  "name": "tool_name",
  "description": "English description for Agent — what it does, what it returns",
  "params": {
    "param_name": {
      "type": "string",
      "description": "Parameter description"
    }
  }
}
```

- `name` — 英文 snake_case 标识符
- `description` — 英文，给 Agent 阅读，说明功能和返回内容
- `params` — 参数定义，无 `default` 字段的参数自动设为必填
- `display_name` — 可选，给用户看的中文名
- `description_zh` — 可选，给用户看的中文简介
- `api` — API 工具的 HTTP 配置（仅声明式）
- `requires_connections` — 工具依赖的外部连接器声明(见"步骤 3")

高级字段（`timeout`、`retry`、`max_result_size`、`dependencies`）详见 `references/tool-json-spec.md`。

## 声明式工具速览

通过 `tool.json` 的 `api` 字段声明 HTTP 请求：

```json
{
  "name": "weather_query",
  "description": "Query current weather for a city. Returns temperature, humidity, wind.",
  "display_name": "查天气",
  "params": {
    "city": { "type": "string", "description": "City name" }
  },
  "requires_connections": [
    { "category": "openweather", "fields": ["api_key"], "required": true }
  ]
}
```

对于需要连接器的 API 工具,推荐用**脚本式**(`main.py`)以便通过
`ctx.connections.get("openweather").field("api_key")` 显式注入 key 到 headers/query。
纯 `auth` 字段暂不支持按连接器引用凭据(未来版本)。

```json
// 纯声明式 · 无须凭据的服务(例如公共接口,或凭据在 URL 模板中通过 {conn:...} 占位):
{
  "name": "weather_query",
  "description": "...",
  "params": { "city": { "type": "string" } },
  "api": {
    "url": "https://api.openweathermap.org/data/2.5/weather?appid={conn:openweather.api_key}",
    "method": "GET",
    "params_mapping": { "city": "q" }
  },
  "requires_connections": [
    { "category": "openweather", "fields": ["api_key"], "required": true }
  ]
}
```

完整的 `api` 字段说明和认证方式详见 `references/tool-json-spec.md`。

## 脚本式工具速览

`main.py` 定义入口：

```python
async def execute(ctx, **params):
    # ctx: ToolContext — 平台能力入口
    # params: tool.json 中声明的参数
    conn = ctx.connections.get("openweather")
    api_key = conn.field("api_key")
    resp = await ctx.http.get("https://...", headers={"Authorization": f"Bearer {api_key}"})
    data = resp.json()
    # ... 数据处理 ...
    return "result"
```

ToolContext 核心能力：

| 能力 | 用法 |
|------|------|
| 连接凭据 | `ctx.connections.get("<slug>").field("<key>")` |
| HTTP | `await ctx.http.get/post(...)` |
| 文件 | `ctx.save_file(name, content)` / `ctx.read_file(path)` |
| 持久化目录 | `ctx.get_tool_home()` — CLI 工具的 per-user 持久化 HOME |
| LLM | `await ctx.call_llm(prompt)` |
| Agent 节点 | `await ctx.create_agent(task, tools=[...])` |
| 工具互调 | `await ctx.call_tool("grep", pattern="...")` |
| 进度 | `await ctx.report_progress("处理中...", 50)` |
| 缓存 | `ctx.cache["key"] = value` |

完整 API 详见 `references/corex-api.md`，完整示例详见 `references/corex-examples.md`。

## 工具优化与诊断

当用户报告工具有问题或需要优化时：

1. 读取现有 `tools/{name}/tool.json` 和 `main.py`，理解当前实现
2. 诊断问题（参考 `references/troubleshooting.md`）
3. 修改相关文件
4. 重新验证

## 创建流程总结

1. 判断意图（独立功能 / 接通服务 / 接入生态）
2. 选择实现方式（声明式 / 脚本式）
3. 编写 tool.json（name、description、params，声明式加 api 字段）
4. 脚本式：编写 main.py，使用 `ctx` 访问平台能力
5. 如需外部服务凭据:按"步骤 3 · 外部服务凭据"走 `connection_credential` 两步法
6. 如需子模块：`lib/` 目录 + `__init__.py`（详见 `references/lib-pattern.md`）
7. 如属同一服务的多个工具：用工具包组织（详见 `references/tool-json-spec.md`）
8. 如是生态接入：先安装配套技能（详见 `references/external-skill-install.md`）
9. 验证工具可用
