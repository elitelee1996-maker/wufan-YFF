# Case JSON Schema 参考

## 完整结构

```json
{
  "schema_version": "v1",
  "artifact_type": "corevo_e2e_case",
  "case_id": "case_XXX",
  "title": "简短标题",
  "description": "详细描述",
  "environment": {
    "base_url": "https://www.wufanai.com",
    "requires_authenticated_browser_state": true,
    "auth_strategy": "reuse_or_login"
  },
  "map_ref": "agent_workspace",
  "vars": {
    "message": "你好"
  },
  "steps": [...],
  "expected": {
    "status": "passed"
  },
  "ws_expect": {
    "performance": {
      "max_ttft_ms": 10000,
      "max_duration_ms": 120000,
      "max_iterations": 10,
      "max_tool_calls": 20
    }
  }
}
```

## 字段说明

| 字段 | 类型 | 必需 | 说明 |
|---|---|---|---|
| `case_id` | string | 是 | 唯一 ID，格式 `case_NNN` |
| `title` | string | 是 | 简短标题 |
| `description` | string | 否 | 详细描述 |
| `environment.base_url` | string | 是 | 目标站点 URL |
| `environment.requires_authenticated_browser_state` | bool | 是 | 是否需要登录态 |
| `environment.auth_strategy` | string | 是 | `none` / `reuse_or_login` / `force_login` |
| `map_ref` | string | 否 | 关联的 map ID |
| `vars` | object | 否 | 模板变量，步骤中用 `{{key}}` 引用 |
| `steps` | array | 是 | 步骤数组 |
| `expected.status` | string | 否 | 期望状态，通常 `"passed"` |
| `ws_expect` | object | 否 | WebSocket 期望配置 |

## Step Action 类型

### auth — 认证

```json
{"step_id": "login", "action": "auth", "strategy": "reuse_or_login"}
```

| 参数 | 说明 |
|---|---|
| `strategy` | `none`（不登录）/ `reuse_or_login`（复用或登录）/ `force_login`（强制登录） |

### fill — 填写文本框

```json
{"step_id": "fill_message", "action": "fill", "target": {...}, "value": "{{message}}"}
```

| 参数 | 必需 | 说明 |
|---|---|---|
| `target` | 是 | 定位目标（见 Target 定位） |
| `value` | 是 | 填入的文本，支持 `{{var}}` |

### click — 点击

```json
{
  "step_id": "click_send",
  "action": "click",
  "target": {...},
  "hover_target": {...},
  "hover_wait_ms": 500,
  "force": true,
  "mark_ws_start": true,
  "wait_enabled": true,
  "wait_enabled_ms": 10000,
  "optional": true,
  "resolve_timeout_ms": 3000
}
```

| 参数 | 必需 | 说明 |
|---|---|---|
| `target` | 是 | 点击目标 |
| `hover_target` | 否 | 悬浮目标（触发 orb/tooltip 等） |
| `hover_wait_ms` | 否 | 悬浮后等待时间，默认 500 |
| `force` | 否 | 强制点击，跳过可操作性检查 |
| `mark_ws_start` | 否 | 标记 WS 消息监听开始 |
| `wait_enabled` | 否 | 等待元素可点击 |
| `optional` | 否 | 元素不存在时跳过而非报错 |
| `resolve_timeout_ms` | 否 | 元素查找超时，默认 5000 |

### wait_ws_reply — 等待 WS 回复

```json
{"step_id": "wait_reply", "action": "wait_ws_reply", "timeout_ms": 120000}
```

**重要**：此步骤后必须跟 `wait_dom_reply`，否则 DOM 一致性断言会失败。

### wait_dom_reply — 等待 DOM 渲染

```json
{"step_id": "wait_dom", "action": "wait_dom_reply", "region": "chat_panel", "timeout_ms": 60000}
```

| 参数 | 必需 | 说明 |
|---|---|---|
| `region` | 否 | 检查的区域 ID，默认 `chat_panel` |
| `timeout_ms` | 否 | 超时，默认 60000 |

### assert_text_visible — 断言文本可见

```json
{"step_id": "verify", "action": "assert_text_visible", "text": "圆桌讨论", "timeout_ms": 5000}
```

| 参数 | 必需 | 说明 |
|---|---|---|
| `text` | 是 | 期望可见的文本（子串匹配） |
| `timeout_ms` | 否 | 超时，默认 10000 |
| `exact` | 否 | 是否精确匹配，默认 false |

### assert_no_keywords — 断言无禁止关键词

```json
{"step_id": "check", "action": "assert_no_keywords", "keywords": ["Error", "Exception", "500"]}
```

### wait_ms — 固定等待

```json
{"step_id": "wait", "action": "wait_ms", "ms": 2000}
```

### screenshot — 截图

```json
{"step_id": "capture", "action": "screenshot", "name": "my_screenshot.png"}
```

### goto — 导航

```json
{"step_id": "nav", "action": "goto", "url": "https://www.wufanai.com/", "wait_until": "domcontentloaded"}
```

## Target 定位

Target 对象用于定位 Playwright 元素：

```json
{
  "region": "input_box",
  "control_id": "message_input",
  "role": "textbox",
  "name": "消息输入框"
}
```

| 字段 | 说明 |
|---|---|
| `region` | map 中的 region_id，用于空间约束 |
| `control_id` | map 中的 control_id |
| `role` | Playwright role（button / textbox / tab / link 等） |
| `name` | Playwright accessible name |
| `placeholder` | placeholder 文本（备选定位） |

解析优先级：`role + name` → `placeholder` → `region + control_id` → CSS fallback

## 变量替换

- `{{var_name}}` → 从 `vars` 中取值
- `{{expected.xxx}}` → 从 `expected` 中取值
- `{{config.xxx}}` → 从环境配置中取值

## 常见 case 模式

### 模式 A：发送消息并等待回复

```
auth → fill → click(send, mark_ws_start) → wait_ws_reply → wait_dom_reply → assert_no_keywords
```

### 模式 B：UI 导航验证

```
auth → click(hover_target) → assert_text_visible → click(tab) → assert_text_visible
```

### 模式 C：悬浮触发 + 面板操作 + 发送

```
auth → click(orb, hover_target) → assert_text_visible(panel) → close_panel → fill → click(send) → wait_ws_reply → wait_dom_reply → assert
```
