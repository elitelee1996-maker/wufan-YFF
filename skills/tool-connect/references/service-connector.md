# 服务连接器设计模式

当需要接通一个外部服务（而不仅仅是做一个固定功能的工具）时，核心理念是构建一个**薄壳（thin wrapper）**——封装认证和基础连接能力，不限定固定的 API 路径或命令，由 Agent 在使用时动态决定具体调用什么。

## 选择模式

| 目标服务提供的是... | 用哪种模式 |
|------|------|
| HTTP REST API（大多数 SaaS 产品：Confluence、Jira、Notion、GitHub API 等） | 模式 A：HTTP API 封装 |
| Agent-friendly 的 CLI 工具（如飞书 CLI `--format json`、钉钉 CLI） | 模式 B：CLI 中转 |
| 两者都有 | 优先 CLI（如果 CLI 设计了结构化输出和丰富的 shortcuts） |

## 模式 A：HTTP API 封装

封装 base_url + 认证，参数为 `method` / `path` / `query` / `body`，Agent 自由组合。

### 设计要点

1. **不限定 API 路径**：参数用通用的 `path`，而不是写死 `/api/v1/users`
2. **认证统一处理**:从 `ctx.connections.get(slug)` 取凭据,在 headers 中统一注入
3. **base_url 作为密钥**：不同团队可能使用不同的实例域名，base_url 声明为 team 级 secret

### tool.json 模板

```json
{
  "name": "{service_name}_api",
  "description": "Execute any {Service Name} REST API call. Agent decides method, path, and parameters.",
  "display_name": "{Service Display Name}",
  "timeout": 60,
  "params": {
    "method": { "type": "string", "description": "HTTP method: GET, POST, PUT, DELETE", "default": "GET" },
    "path": { "type": "string", "description": "REST API path, e.g. /rest/api/content/12345" },
    "query": { "type": "object", "description": "Query parameters as key-value pairs", "default": {} },
    "body": { "type": "object", "description": "Request body for POST/PUT", "default": {} }
  },
  "requires_connections": [
    { "category": "{service}_base_url", "fields": ["value"], "required": true },
    { "category": "{service}_token", "fields": ["value"], "required": true }
  ]
}
```

### main.py 模板

```python
import json

async def execute(ctx, method="GET", path="", query=None, body=None, **_kw):
    conn = ctx.connections.get("{SERVICE}")
    base_url = conn.field("base_url").rstrip("/")
    token = conn.field("api_token")

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
        return json.dumps(data, ensure_ascii=False, indent=2)[:25000]
    except Exception:
        return resp.text[:5000]
```

### 适配不同认证方式

根据目标服务替换 headers 中的认证行：

- **Bearer Token**：`"Authorization": f"Bearer {token}"`
- **Basic Auth**：`"Authorization": f"Basic {base64.b64encode(f'{user}:{token}'.encode()).decode()}"`
- **API Key Header**：`"X-Api-Key": token`
- **Cookie**：`"Cookie": f"session={token}"`

## 模式 B：CLI 中转

封装 CLI 二进制 + 凭证注入 + 环境隔离，参数为 `command`，Agent 自由决定。

### 设计要点

1. **持久化 HOME 目录**：使用 `ctx.get_tool_home()` 获取 per-user 持久化目录，CLI 的配置、auth token、缓存跨调用保留，不用每次从零初始化
2. **凭证通过 ctx.connections 注入**:从连接器读取字段值,注入到 CLI 配置文件或环境变量
3. **JSON 输出**：自动附加 `--format json`（如果 CLI 支持），便于解析
4. **CLI 安装检查**：首次执行时检查 CLI 是否已安装，未安装则返回安装指引

### tool.json 模板

```json
{
  "name": "{service_name}_cli",
  "description": "Execute any {cli-name} command with credential injection. Agent decides the command.",
  "display_name": "{Service Display Name} CLI",
  "timeout": 120,
  "params": {
    "command": { "type": "string", "description": "{cli-name} command without the binary prefix" }
  },
  "requires_connections": [
    { "category": "{service}", "fields": ["app_id", "app_secret", "user_token"], "required": true }
  ]
}
```

### main.py 模板

```python
import asyncio
import json
import os

async def execute(ctx, command="", **_kw):
    # 持久化 HOME 目录：per-user 隔离，CLI 配置和 auth 状态跨调用保留
    tool_home = ctx.get_tool_home()

    env = {
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "HOME": str(tool_home),
        "LANG": "en_US.UTF-8",
    }

    # 首次使用时初始化 CLI 配置（后续调用自动复用）
    # 替换为对应 CLI 的初始化逻辑
    _ensure_config(tool_home, ctx.connections.get("your_service"))

    full_cmd = f"{cli_binary} {command}"
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
        if "not found" in err.lower():
            return f"错误: {cli_binary} 未安装。请先执行对应的安装命令。"
        return f"命令执行失败 (exit {proc.returncode}):\n{err[:2000]}"

    output = stdout.decode("utf-8", errors="replace")
    try:
        return json.dumps(json.loads(output), ensure_ascii=False, indent=2)[:25000]
    except json.JSONDecodeError:
        return output[:5000]


def _ensure_config(tool_home, conn):
    """首次使用时写入 CLI 配置文件。已存在则跳过。conn 是 ctx.connections.get(slug) 的结果。"""
    # 替换为具体 CLI 的配置文件写入逻辑,用 conn.field("<key>") 读凭据
    pass
```

**关键区别**：`ctx.get_tool_home()` 返回的是持久化的 per-user 目录，CLI 的 `auth login` 写入的 token 会保留。下次调用时 `_ensure_config` 检测到配置已存在就跳过，CLI 直接使用已有的 auth 状态。

### 常见 CLI 的环境变量

| CLI | 配置目录环境变量 | 凭证环境变量 |
|-----|----------------|-------------|
| 飞书 (lark-cli) | `LARKSUITE_CLI_CONFIG_DIR` | `LARK_APP_ID`, `LARK_APP_SECRET` |
| 钉钉 (dws) | `DWS_CONFIG_DIR` | `DWS_CLIENT_ID`, `DWS_CLIENT_SECRET` |
| GitHub (gh) | `GH_CONFIG_DIR` | `GH_TOKEN` |

### CLI 安装

CLI 工具通常不预装在平台中，Agent 需要在构建连接器时通过 bash 安装：

```bash
npm install -g @larksuite/cli     # 飞书
npm install -g @anthropic/cli     # 示例
pip install gh-cli                # 示例
```

在 main.py 模板中应包含安装检查逻辑，首次执行时如果 CLI 不存在则返回安装指引。
