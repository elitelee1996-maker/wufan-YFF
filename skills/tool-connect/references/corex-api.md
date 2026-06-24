# ToolContext 完整 API

CoreX 工具的 `main.py` 入口函数接收 `ctx`（ToolContext），它是访问平台能力的统一入口。

```python
async def execute(ctx, **params):
    # ctx: ToolContext
    # params: tool.json 中声明的参数
    return "result"
```

函数可以是 `async def` 或普通 `def`。同步函数自动在线程池中执行，不阻塞平台。

## 持久化工具目录

| 方法 | 说明 |
|------|------|
| `ctx.get_tool_home(subdir="")` → Path | 获取 per-user 持久化 HOME 目录，CLI 配置和 auth 状态跨调用保留 |

用于 CLI 中转工具，替代 `tempfile.mkdtemp()`。路径按 team_id + tool_name + user_id 隔离。

```python
tool_home = ctx.get_tool_home()
# → data/teams/{team_id}/tool_homes/{tool_name}/{user_id}/

env = {"HOME": str(tool_home), "PATH": "/usr/local/bin:/usr/bin:/bin"}
# CLI 的配置文件、auth token 等会持久保存在这个目录中
```

## 外部服务凭据

| 方法 | 说明 |
|------|------|
| `ctx.connections.get(slug)` | 获取连接器视图(按当前用户身份自动筛选 user 字段) |
| `conn.field(key)` | 读取字段值(必需字段缺失时抛 MissingConnectionField) |
| `conn.field(key, default=None)` | 可选字段,允许缺失 |
| `conn.is_complete()` | 连接器是否已完整可用 |

示例:
```python
conn = ctx.connections.get("openweather")
api_key = conn.field("api_key")
```

## HTTP 客户端

| 方法 | 说明 |
|------|------|
| `ctx.http` | 复用连接池的 httpx.AsyncClient，工具生命周期内共享 |

用 `ctx.http` 替代每次创建 `httpx.AsyncClient()`，自动管理连接池生命周期：

```python
resp = await ctx.http.get("https://api.example.com/data", headers={"Authorization": f"Bearer {api_key}"})
data = resp.json()
```

## 文件操作

| 方法 | 说明 |
|------|------|
| `ctx.save_file(name, content)` → str | 保存到会话文件目录，返回 Agent 路径 |
| `ctx.save_shared_file(name, content)` → str | 保存到共享文件目录 |
| `ctx.read_file(path)` → str | 读取工作空间内文件 |

## LLM 调用

| 方法 | 说明 |
|------|------|
| `await ctx.call_llm(prompt, model=None, images=None, json_mode=False)` → str | LLM 调用 |

支持多模态输入和 JSON 模式：

```python
summary = await ctx.call_llm("总结这段数据", json_mode=True)
description = await ctx.call_llm("描述这张图片", images=["screenshot.png"])
```

## Agent 节点

工具是确定性的执行程序。当流程中某个步骤需要多步推理 + 动态使用工具才能完成时，嵌入 Agent 节点。如果只需一次性判断/提取/总结，用 `ctx.call_llm()` 即可。

| 方法 | 说明 |
|------|------|
| `await ctx.create_agent(task, ...)` → str | 创建 Agent 节点执行需要多步推理的子任务 |
| `await ctx.call_agent(task)` → str | 简化调用（等价于 create_agent） |

**何时用 Agent 节点而非 call_llm：**

| 流程中某步骤需要... | 用什么 | 场景 |
|------|------|------|
| 一次性判断/分类/提取/总结 | `ctx.call_llm()` | 非结构化数据转结构化、打标签、摘要 |
| 多步推理 + 动态使用工具 | `ctx.create_agent()` | 搜索资料 → 分析 → 验证 → 再搜索 |

**Agent 节点来源：**

| 场景 | 写法 |
|------|------|
| 复用团队已有主 Agent | `name="产品经理"` |
| 复用已有子 Agent | `name="translator"` |
| 派生当前 Agent 分身 | `name="self"` |
| 临时创建专用角色 | `system_prompt="你是..."` |
| 简单委托 | 仅传 task |

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| task | str | 必填，任务描述 |
| name | str | 已有伙伴名称 / "self" |
| system_prompt | str | 临时 Agent 的系统提示词 |
| model | str | 模型（sonnet / opus / haiku） |
| tools | list[str] | 允许的工具列表 |
| disabled_tools | list[str] | 禁止的工具列表 |
| max_iterations | int | 最大迭代次数，默认 15 |

## 工具互调

| 方法 | 说明 |
|------|------|
| `await ctx.call_tool(tool_name, **kwargs)` → str | 调用其他已注册工具 |

可调用内置工具或其他自定义工具：

```python
files = await ctx.call_tool("grep", pattern="error", path="logs/")
content = await ctx.call_tool("read", path="config.yaml")
```

## 缓存

| 方法 | 说明 |
|------|------|
| `ctx.cache` | 会话级 dict 缓存，同一会话内多次工具调用共享 |

适合缓存 token、连接信息等跨调用复用的数据：

```python
if "auth_token" not in ctx.cache:
    api_key = ctx.connections.get("your_service").field("api_key")
    ctx.cache["auth_token"] = await fetch_token(api_key)
token = ctx.cache["auth_token"]
```

## 进度报告

| 方法 | 说明 |
|------|------|
| `await ctx.report_progress(message, percentage=None)` | 向前端报告进度 |

```python
await ctx.report_progress("正在获取第 1 页数据...", 10)
await ctx.report_progress("数据处理完成", 100)
```

## 日志

| 方法 | 说明 |
|------|------|
| `ctx.log` | 工具专用 logger，自动关联工具名 |

```python
ctx.log.info(f"获取到 {len(results)} 条记录")
ctx.log.warning("API 返回了空结果")
```

## 依赖校验

| 方法 | 说明 |
|------|------|
| `ctx.require(*packages)` → list[str] | 检查包是否安装，返回缺失包名 |

```python
missing = ctx.require("pandas", "lxml")
if missing:
    return f"缺少依赖: {', '.join(missing)}"
```

## 多模态返回

| 方法 | 说明 |
|------|------|
| `ctx.return_with_images(text, image_paths)` → dict | 构建含图片的返回 |

## 平台事件

| 方法 | 说明 |
|------|------|
| `await ctx.emit_event(event_type, payload=None)` | 发射自定义事件，可触发下游自动化管道 |

`event_type` 会自动添加 `custom.` 前缀：

```python
await ctx.emit_event("price_alert", {"symbol": "GOLD", "price": 2800, "threshold": 2750})
```

## 上下文信息

| 属性 | 说明 |
|------|------|
| `ctx.session_id` | 当前会话 ID |
| `ctx.user_id` | 当前用户 ID |
| `ctx.agent_id` | 当前 Agent ID |
