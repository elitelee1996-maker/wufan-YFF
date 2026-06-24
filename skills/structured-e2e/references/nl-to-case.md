# 自然语言 → Case 转换指南

## 常见操作模式映射

| 用户描述 | Step 类型 | 示例 |
|---|---|---|
| "登录" | `auth` | `{"action": "auth", "strategy": "reuse_or_login"}` |
| "输入 XXX" | `fill` | `{"action": "fill", "target": {...}, "value": "XXX"}` |
| "点击 XXX 按钮" | `click` | `{"action": "click", "target": {"role": "button", "name": "XXX"}}` |
| "悬浮后点击 YYY" | `click` + `hover_target` | click step 带 hover_target 参数 |
| "等待回复" | `wait_ws_reply` + `wait_dom_reply` | 两步必须一起出现 |
| "检查没有报错" | `assert_no_keywords` | `{"action": "assert_no_keywords", "keywords": ["Error", "500"]}` |
| "看到 XXX 文字" | `assert_text_visible` | `{"action": "assert_text_visible", "text": "XXX"}` |
| "等 N 秒" | `wait_ms` | `{"action": "wait_ms", "ms": 3000}` |
| "截图" | `screenshot` | `{"action": "screenshot", "name": "xxx.png"}` |
| "打开页面" | `goto` | `{"action": "goto", "url": "https://..."}` |

## 页面功能 → Map/Region 映射

| 功能区域 | map_id | region_id | 关键 control_id |
|---|---|---|---|
| 登录页 | `corevo_login` / `cas_login` | `credential_form` | `login_submit` |
| 工作台聊天 | `agent_workspace` | `chat_panel` + `input_box` | `message_input`, `send` |
| 圆桌讨论入口 | `agent_workspace_roundtable` | `mode_selector` | `roundtable_orb`, `collab_options_toggle` |
| 圆桌创建面板 | `agent_workspace_roundtable` | `create_panel` | `create_roundtable`, `mode_tab_moderator/ordered/free` |
| 任务派遣入口 | `agent_workspace_dispatch` | `mode_selector` | `dispatch_orb`, `collab_options_toggle` |
| 派遣创建面板 | `agent_workspace_dispatch` | `dispatch_panel` | `create_dispatch`, `mode_tab_solo/squad/fan` |
| 输入工具栏 | 各 workspace map | `input_toolbar` | `send_message`, `add_attachment`, `thinking_mode` |

## 从代码变更推断 Case

当用户改了前端组件时：

1. 找到修改的组件文件（如 `ChannelBar.tsx`）
2. 确定组件所在的页面（如 `agent_workspace_roundtable`）
3. 识别交互元素（按钮、输入框、tab）
4. 生成覆盖该交互路径的 case

### 示例

> 用户改了 `DispatchCreatePanel.tsx` 的 tab 切换逻辑

→ 生成 case_008（任务派遣模式切换）覆盖单兵/编队/扇出三个 tab

## Case 生成模板

### 发送消息类

```json
{
  "case_id": "case_XXX",
  "title": "XXX 模式下发消息",
  "map_ref": "对应 map",
  "vars": {"message": "测试消息"},
  "steps": [
    {"step_id": "login", "action": "auth", "strategy": "reuse_or_login"},
    {"step_id": "enter_mode", "action": "click", "target": {...}, "hover_target": {...}, "hover_wait_ms": 500, "force": true},
    {"step_id": "fill", "action": "fill", "target": {"region": "input_box", "control_id": "message_input", "role": "textbox", "name": "消息输入框"}, "value": "{{message}}"},
    {"step_id": "send", "action": "click", "target": {"region": "input_toolbar", "control_id": "send_message", "role": "button", "name": "发送"}, "mark_ws_start": true},
    {"step_id": "wait_ws", "action": "wait_ws_reply", "timeout_ms": 120000},
    {"step_id": "wait_dom", "action": "wait_dom_reply", "region": "chat_panel", "timeout_ms": 60000},
    {"step_id": "check", "action": "assert_no_keywords", "keywords": ["Error", "Exception", "500"]}
  ]
}
```

### UI 导航验证类

```json
{
  "case_id": "case_XXX",
  "title": "XXX 模式切换",
  "map_ref": "对应 map",
  "steps": [
    {"step_id": "login", "action": "auth", "strategy": "reuse_or_login"},
    {"step_id": "enter", "action": "click", "target": {...}, "hover_target": {...}, "hover_wait_ms": 500, "force": true},
    {"step_id": "verify_panel", "action": "assert_text_visible", "text": "面板标题", "timeout_ms": 8000},
    {"step_id": "click_tab", "action": "click", "target": {"region": "panel_region", "control_id": "tab_id", "role": "button", "name": "tab名称"}},
    {"step_id": "verify_mode", "action": "assert_text_visible", "text": "模式描述文本", "timeout_ms": 3000}
  ]
}
```
