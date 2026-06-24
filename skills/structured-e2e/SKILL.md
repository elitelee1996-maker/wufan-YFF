---
name: 结构化 E2E 用例生成
description: 从自然语言或代码变更生成悟帆 E2E 测试用例。当用户想为新功能编写 E2E 测试、检查现有测试覆盖情况、或将一段操作流程转化为可执行 case 时触发。触发词：E2E、端到端、测试用例、生成 case、覆盖报告。
---

# 结构化 E2E 用例生成

## 触发条件

- 用户说"写一个 E2E 测试"、"生成 case"、"覆盖报告"
- 用户描述了一段 UI 操作流程，想转化为可执行用例
- 用户改了前端组件，想补对应 E2E 覆盖

## 工作流程

### 1. 获取当前覆盖状态

```bash
python core/skills/builtin/structured-e2e/scripts/coverage_report.py
```

输出 JSON + 人类可读摘要，告诉你哪些 map/rule/case 已存在，哪些功能还没覆盖。

### 2. 识别目标页面/功能

根据用户描述或代码变更，确定：
- 目标页面 → 对应的 `map_id`（查 `tests/e2e_corevo/fixtures/maps/`）
- 目标功能 → 对应的 `region_id` 和 `control_id`（查 map.json）

### 3. 检查 map 是否存在

- 已有 map → 直接进入 case 生成
- 没有 map → 提示用户先用 `explore_ui.py` 探索 UI 并构建 map：
  ```bash
  python -m tests.e2e_corevo.tools.explore_ui --step all --headed
  ```

### 4. 生成 case JSON

遵循 `references/case-format.md` 的 schema。核心规则：

- 每个 case 必须有显式 `steps` 数组
- 认证步骤放在第一步（`auth` action）
- 使用 `{{var_name}}` 做变量替换
- 涉及消息发送的 case 必须包含完整的 **wait_ws_reply + wait_dom_reply** 序列
- 包含 `assert_no_keywords` 兜底断言

### 5. 输出 case 文件 + 运行命令

```bash
# 推荐：运行 case + 自动检查 skill 文档是否需要更新
python core/skills/builtin/structured-e2e/scripts/run_with_drift.py --case tests/e2e_corevo/fixtures/cases/case_XXX.json --headed

# 或手动分步运行
python -m tests.e2e_corevo.tools.run_case --case tests/e2e_corevo/fixtures/cases/case_XXX.json --headed
```

### 6. Drift 检查（自动反馈闭环）

运行 `run_with_drift.py` 会在 case 通过后自动执行 drift 检查：

```bash
# 检查所有 case 的 drift 状态
python core/skills/builtin/structured-e2e/scripts/drift_check.py
```

**drift 检查做的事情**：
- 对比同一个 case 的最新报告和上一次报告
- 如果 case 从 failed → passed，分析失败原因是否匹配已知坑
- 如果是新坑（不在 SKILL.md 中），返回 exit code 2 + 提示
- 如果 case 从 passed → failed（回归），返回 exit code 2 + 提示

**exit code 含义**：
- `0` = case 通过，无 drift
- `1` = case 失败
- `2` = case 通过但 skill 文档需要更新

当 exit code = 2 时，应该：
1. 把新发现的坑加到 SKILL.md 的踩坑清单
2. 把修复模式加到 `references/case-format.md`
3. 重新运行确认通过

## 踩坑清单（必读）

这些是从实际运行中总结的教训，生成 case 时必须检查：

### 1. wait_ws_reply 后必须跟 wait_dom_reply

任何包含 `wait_ws_reply` 的 case，**必须**在它之后加一个 `wait_dom_reply` 步骤。否则 runner 的 DOM 一致性断言会因 `final_text` 为空而失败。

```json
{"step_id": "wait_reply", "action": "wait_ws_reply", "timeout_ms": 120000},
{"step_id": "wait_dom", "action": "wait_dom_reply", "region": "chat_panel", "timeout_ms": 60000}
```

### 2. dispatch 面板会遮挡发送按钮

任务派遣面板打开时，hint overlay（"Agent 也可以在对话中自行发起后台任务"）会遮挡发送按钮。必须在发送前关闭面板：

```json
{"step_id": "close_dispatch_panel", "action": "click", "target": {"region": "dispatch_panel", "control_id": "close_panel", "role": "button", "name": "×"}, "optional": true, "resolve_timeout_ms": 2000},
{"step_id": "wait_panel_closed", "action": "wait_ms", "ms": 500},
{"step_id": "send", "action": "click", "target": {...}, "mark_ws_start": true}
```

不要用 `force: true` 绕过遮挡 —— 点击会穿透到错误元素，消息不会实际发送。

### 3. tab 元素是 button 不是 tab

EmptyChannelPanel 和 DispatchCreatePanel 的模式切换 tab 是 `<button>` 元素，不是 `role="tab"`。target 中必须用 `"role": "button"`。

```json
{"role": "button", "name": "主持"}  // ✓ 正确
{"role": "tab", "name": "主持"}      // ✗ 找不到
```

### 4. 断言文本必须来自实际渲染组件

不要从不同组件取断言文本。同一个功能在不同页面的文本可能不同：

| 功能 | EmptyChannelPanel (创建面板) | ReplayMessageList (回放) |
|---|---|---|
| 主持人模式 | `主持人控场多角色深度评估` | `主持人引导每轮讨论` |
| 轮流模式 | `Go-to-Market` | `轮序模式` |
| 自由模式 | `话题自由流转` | `自由模式` |

生成断言时，检查 map 对应页面的实际组件源码。

### 5. input_box bounds 必须覆盖实际 textarea 位置

InputBar 组件的 textarea 位置会因 prompt tag（如"圆桌 · 主持人模式"）而下移。map 的 input_box bounds 必须用 `explore_ui.py` 实测，不能从代码估算。

建议 input_box 高度设为 170px（从输入区顶部到工具栏底部）。

### 6. 悬浮触发的 orb 必须用 hover_target

ChannelBar 的圆桌/派遣 orb 只在悬浮 "+" 按钮后才出现。click step 必须带 `hover_target` 和 `hover_wait_ms`：

```json
{
  "action": "click",
  "target": {"region": "mode_selector", "control_id": "roundtable_orb", "role": "button", "name": "圆桌讨论"},
  "hover_target": {"region": "mode_selector", "control_id": "collab_options_toggle", "role": "button", "name": "展开协同任务选项"},
  "hover_wait_ms": 500,
  "force": true
}
```

## Map 构建指南

### 用 explore_ui.py 探索 UI

```bash
python -m tests.e2e_corevo.tools.explore_ui --step channelbar --headed
python -m tests.e2e_corevo.tools.explore_ui --step roundtable --headed
python -m tests.e2e_corevo.tools.explore_ui --step dispatch --headed
```

输出截图 + 元素坐标到 `tests/e2e_corevo/reports/explore_ui/`。

### 从源码读取组件属性

关键文件：
- `web/src/components/Chat/ChannelBar.tsx` — ChannelBar、EmptyChannelPanel、模式 tab
- `web/src/components/Chat/DispatchCreatePanel.tsx` — 派遣面板、模式 tab
- `web/src/components/Chat/InputBar.tsx` — 输入框、发送按钮（data-cvo-id 属性）
- `web/src/components/Chat/ChatContainer.tsx` — 面板状态管理、模板文本

### 生成分区截图验证

```bash
python -m tests.e2e_corevo.tools.generate_map_partitions --headed
```

在真实截图上叠加分区边框，人工核对 bounds 是否准确。

## 质量检查清单

生成 case 后自验：

- [ ] 第一步是 `auth`
- [ ] 有 `wait_ws_reply` 的一定有 `wait_dom_reply`
- [ ] dispatch 发送前有关闭面板步骤
- [ ] tab 的 role 是 `button` 不是 `tab`
- [ ] 断言文本来自正确的组件源码
- [ ] input_box 的 region bounds 覆盖实际 textarea 位置
- [ ] 悬浮交互有 `hover_target` + `hover_wait_ms` + `force`
