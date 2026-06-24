# tool.json 完整规范

## 核心字段

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

- `name` — 工具标识符，英文 snake_case
- `description` — 给 Agent 阅读的英文工具描述，应说明功能和返回内容
- `params` — 参数定义，每个参数含 `type`（string/integer/number/boolean/array/object）和 `description`；无 `default` 字段的参数自动设为必填
- `display_name` — 可选，给用户看的中文名
- `description_zh` — 可选，给用户看的中文简介
- `api` — API 工具的 HTTP 配置（仅声明式）
- `requires_connections` — 工具依赖的外部连接器声明(通过 `connection_credential` 工具管理)

## 高级字段

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `timeout` | integer | 120（CoreX）/ 30（API） | 执行超时秒数，最大 600 |
| `retry` | integer | 0 | 失败自动重试次数 |
| `max_result_size` | integer | 25000 | 返回结果最大字符数，超出自动截断 |
| `dependencies` | string[] | [] | CoreX 工具依赖的 Python 包名，加载时预检 |

## API 工具（声明式）

通过 `tool.json` 的 `api` 字段声明 HTTP 请求。

### api 字段说明

| 字段 | 说明 |
|------|------|
| `url` | 请求地址,支持 `{conn:<slug>.<field>}` 模板变量自动注入凭据 |
| `method` | HTTP 方法:GET / POST / PUT / PATCH / DELETE |
| `params_mapping` | Agent 参数名到 API 字段名的映射,支持点分路径(如 `"query": "filter.keyword"`) |
| `query_defaults` | 固定的默认查询参数,自动附加到每次请求 |
| `headers` | 额外请求头,值支持 `{conn:<slug>.<field>}` 模板变量 |

### URL / headers 中注入凭据

通过 `{conn:<slug>.<field>}` 占位符自动注入连接器字段的值:

```json
{
  "api": {
    "url": "https://api.openweathermap.org/data/2.5/weather?appid={conn:openweather.api_key}",
    "method": "GET"
  },
  "requires_connections": [
    { "category": "openweather", "fields": ["api_key"], "required": true }
  ]
}
```

```json
{
  "api": {
    "url": "https://{conn:confluence.base_url}/rest/api/content",
    "headers": { "Authorization": "Bearer {conn:confluence.api_token}" }
  },
  "requires_connections": [
    { "category": "confluence", "fields": ["base_url", "api_token"], "required": true }
  ]
}
```

需要更灵活的逻辑处理(如签名、多阶段调用)时,用脚本式工具,
通过 `ctx.connections.get(slug).field(key)` 显式读取。

### 完整声明式示例

```json
{
  "name": "weather_query",
  "description": "Query current weather for a city via OpenWeather API. Returns JSON with temperature, humidity, wind speed, and weather description.",
  "display_name": "查天气",
  "description_zh": "查询城市实时天气",
  "params": {
    "city": {
      "type": "string",
      "description": "City name, e.g. Beijing, London, Tokyo"
    }
  },
  "api": {
    "url": "https://api.openweathermap.org/data/2.5/weather?appid={conn:openweather.api_key}",
    "method": "GET",
    "params_mapping": { "city": "q" },
    "query_defaults": { "units": "metric", "lang": "zh_cn" }
  },
  "requires_connections": [
    { "category": "openweather", "fields": ["api_key"], "required": true }
  ]
}
```

## 工具包

当多个工具属于同一服务时（如简道云的搜索、写入、创建表单），用工具包组织。

### pack.json

```json
{
  "name": "jiandaoyun",
  "display_name": "简道云",
  "description": "简道云数据操作工具集",
  "requires_connections": [
    { "category": "jiandaoyun", "fields": ["api_key"], "required": true }
  ]
}
```

包级 `requires_connections` 由包内所有工具共享,无需在每个 tool.json 中重复声明。
工具级声明会被自动合并(取并集)。

### 工具包目录结构

```
tools/{pack_name}/
├── pack.json
├── search_data/
│   └── tool.json
└── write_data/
    ├── tool.json
    └── main.py
```

## 写入路径

通过 write 工具写入，路径以 `tools/` 开头（自动路由到团队工具资产目录）：

- 独立工具：`tools/{name}/tool.json`（+ `tools/{name}/main.py`）
- 子模块：`tools/{name}/lib/__init__.py`、`tools/{name}/lib/{module}.py`
- 工具包元信息：`tools/{pack_name}/pack.json`
- 包内工具：`tools/{pack_name}/{tool_name}/tool.json`（+ `main.py`）
