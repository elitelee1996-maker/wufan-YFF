---
name: MCP 服务安装
description: 安装和配置 MCP(Model Context Protocol)服务。当用户想要接入外部 MCP 服务、配置 MCP 连接参数、或管理 MCP 所需的外部服务凭据时使用此技能。
---

# MCP 服务安装指南

## 什么是 MCP

MCP(Model Context Protocol)是一种标准协议,让 Agent 能够连接外部工具和数据源。
每个 MCP Server 提供一组工具(如查火车票、操作 GitHub、查地图等),安装后 Agent 可以按需激活使用。

## 安装步骤

### 1. 创建配置文件

在 `mcp_servers/{name}/mcp.json` 中写入配置。`{name}` 是服务的唯一标识(英文、小写、用短横线分隔)。

```bash
# 示例:创建 12306 火车票查询服务
write(path="mcp_servers/12306-mcp/mcp.json", content=...)
```

### 2. mcp.json 格式规范

#### STDIO 模式(通过子进程通信,适用于 npm 包)

```json
{
  "name": "12306-mcp",
  "display_name": "12306 车票查询",
  "description": "查询12306火车票余票、车次、站点信息",
  "transport": "stdio",
  "command": "npx",
  "args": ["-y", "12306-mcp"],
  "env": {},
  "enabled": true
}
```

#### SSE 模式(通过 HTTP 长连接,适用于远程服务)

```json
{
  "name": "amap-maps",
  "display_name": "高德地图",
  "description": "地理编码、路径规划、天气查询等地图服务",
  "transport": "sse",
  "url": "https://mcp.amap.com/sse",
  "headers": {},
  "env": {
    "AMAP_MAPS_API_KEY": "${conn:amap.api_key}"
  },
  "requires_connections": [
    { "category": "amap", "fields": ["api_key"], "required": true }
  ],
  "enabled": true
}
```

#### HTTP 模式(Streamable HTTP)

```json
{
  "name": "github",
  "display_name": "GitHub",
  "description": "GitHub API 操作:仓库、Issue、PR 管理",
  "transport": "http",
  "url": "https://api.github.com/mcp",
  "headers": {
    "Authorization": "Bearer ${conn:github.personal_access_token}"
  },
  "requires_connections": [
    { "category": "github", "fields": ["personal_access_token"], "required": true }
  ],
  "enabled": true
}
```

### 3. 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 唯一标识,英文小写+短横线 |
| `display_name` | 否 | Agent 看到的显示名称 |
| `description` | 强烈建议 | Agent 根据描述判断何时使用此服务 |
| `transport` | 是 | `stdio` / `sse` / `http` / `ws` |
| `command` | stdio 必填 | 启动命令(如 `npx`、`python`) |
| `args` | stdio 可选 | 命令参数数组 |
| `env` | 可选 | 环境变量(支持 `${conn:<slug>.<field>}` 占位符) |
| `url` | SSE/HTTP/WS 必填 | 服务器 URL |
| `headers` | 可选 | 请求头(支持 `${conn:<slug>.<field>}` 占位符) |
| `requires_connections` | 可选 | 此 MCP 依赖的外部连接器声明 |
| `enabled` | 否 | 默认 true |

## 外部服务凭据(重要)

### 绝不将明文 API Key 写入配置文件

错误做法:
```json
"env": {"API_KEY": "sk-abc123def456"}
```

正确做法 — 声明连接器 + 用占位符:
```json
"env": {"API_KEY": "${conn:my_service.api_key}"},
"requires_connections": [
  { "category": "my_service", "fields": ["api_key"], "required": true }
]
```

### 连接器占位符格式

`${conn:<slug>.<field>}` — 运行时自动从连接中心读取字段值。

### 声明连接器

如果 MCP 需要的服务还没有连接器,先通过 `connection_credential` 工具声明:

```
connection_credential(action="list")   # 先看空间现有哪些
connection_credential(
  action="declare",
  display_name="高德地图",
  slug="amap",
  fields=[
    {"key": "api_key", "label": "API Key", "type": "secret",
     "owner_level": "team", "required": true,
     "hint": "在高德开放平台申请"}
  ]
)
```

- 若 slug 已在内置 Registry(github / notion / slack / feishu 等)→ 直接复用,不需再 declare
- 常用的 amap / baidu-maps / tencent-maps / 12306 等第三方服务多半需要自定义

### 字段所有权

- `owner_level: "team"` — 团队共享一个(如公司统一申请的地图 API Key)
- `owner_level: "user"` — 每个成员各自填(如个人 GitHub Personal Token)

不确定时问用户:
> 这个 key 是团队共享一个,还是每个人各自有?

### 引导用户连接

MCP 安装完成后,告知用户:
> 请前往「设置 → 连接中心」,找到刚才声明的连接器,点击「+ 连接」填入 API Key。

或者直接调 `connection_credential(action="request", slug="amap")` 在 Chat 里弹连接卡。

**永远不要在对话中要求用户明文发送 API Key。**

## 安装后操作

1. **绑定到 Agent**:用户需要在 Agent 详情页的 MCP tab 中启用此服务
2. **验证连通**:在资产面板的 MCP 列表中点击「测试」验证连接
3. **Agent 使用**:绑定后,Agent 通过 `load_mcp(server_name)` 激活服务的工具

## 从用户提供的 JSON 配置安装

用户可能直接提供 MCP 官方的配置 JSON,格式如:

```json
{"name":"pencil","transport":"stdio","command":"/path/to/binary","args":["--app","desktop"],"env":{}}
```

或 Claude Desktop 格式:

```json
{"mcpServers":{"github":{"command":"npx","args":["-y","@modelcontextprotocol/server-github"],"env":{"GITHUB_TOKEN":"xxx"}}}}
```

处理步骤:
1. 解析 JSON,提取 name/transport/command/args/env/url 等字段
2. 检查 env / headers 中是否有疑似凭据(命名含 KEY/TOKEN/SECRET/PASSWORD)
3. 如有凭据:
   a. 用 `connection_credential(action="list")` 先查是否已有对应连接器
   b. 没有就 `action="declare"` 声明一个
   c. 把 env / headers 中的字面量替换为 `${conn:<slug>.<field>}` 占位符
   d. 添加 `requires_connections` 声明
4. 补充 `display_name` 和 `description`(如果用户未提供,根据名称推断)
5. 写入 `mcp_servers/{name}/mcp.json`
6. `action="request"` 让用户填字段

## 常见 MCP Server 模板

### 12306 火车票查询(无需凭据)
```json
{
  "name": "12306-mcp",
  "display_name": "12306 车票查询",
  "description": "查询12306火车票余票、车次、经停站信息",
  "transport": "stdio",
  "command": "npx",
  "args": ["-y", "12306-mcp"],
  "enabled": true
}
```

### 高德地图(需要 API Key)
```json
{
  "name": "amap-maps",
  "display_name": "高德地图",
  "description": "地理编码、逆地理编码、路径规划、天气查询、IP定位等地图服务",
  "transport": "stdio",
  "command": "npx",
  "args": ["-y", "@amap/amap-maps-mcp-server"],
  "env": {"AMAP_MAPS_API_KEY": "${conn:amap.api_key}"},
  "requires_connections": [
    { "category": "amap", "fields": ["api_key"], "required": true }
  ],
  "enabled": true
}
```
