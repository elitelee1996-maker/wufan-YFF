# 连接凭证

> 让 Agent 调用外部 SaaS 服务时，**不用每次问用户要 API Key** — 凭证统一存到"连接凭证"里，Agent 自动读取。

## 心智模型: 一次连接，处处可用

```
连接凭证 (Connection)              可被这些资产共享读取
┌─────────────────────┐            ┌──────────────────┐
│  飞书开放平台         │   ←───    │  飞书工作流工具    │
│  ├─ app_id (team)   │            │  飞书消息推送 MCP  │
│  ├─ app_secret(team)│            │  飞书技能          │
│  └─ user_token(user)│   ←───    │  Agent 临时脚本    │
└─────────────────────┘            └──────────────────┘
```

**一个连接器**对接**一个外部服务** (飞书 / GitHub / OpenWeather / 自建 API ...)，内部包含**多个字段** (api_key / app_secret / base_url 等)。

**字段有 owner_level**:
- **team** — 管理员配一次，全员共享 (典型: app_id / app_secret / company_secret)
- **user** — 每人各自填，互不可见 (典型: 每个成员自己的 user_token / personal API Key)

> "团队中一起用 vs 各用各的"靠**字段的 owner_level** 决定，不是靠"建几个连接器"。一个连接器**同时**有 team 字段和 user 字段是常态。

**入口**: 设置 → 连接凭证 → 顶部"+ 新建连接凭证"。

---

## 字段类型

| type | 含义 | 形态 |
|---|---|---|
| **secret** | 密钥 / Token，加密存储，UI 打码显示 | API Key、app_secret、OAuth Token |
| **text** | 普通字符串，不加密 | 用户名、公司代号、应用名 |
| **url** | URL 地址，带 https 校验 | 自建服务的 base URL |
| **email** | 邮箱，带格式校验 | 通知邮箱 |

**owner_level 选哪种**:
- 全团队共用一份 → **team** (管理员配一次)
- 每个人各自一份 → **user** (每个人在设置里填自己的)

---

## 三种典型连接形态

### 形态 1: 纯 team — 全员共用一份

例: 公司订了一个 OpenWeather API，一份 key 全员用。

```
OpenWeather
└─ api_key (team, secret) ← 管理员配一次
```

成员看不到 key 明文，但能用任何调用 OpenWeather 的工具。

### 形态 2: 纯 user — 每人各自一份

例: GitHub Personal Token，每个成员有自己的。

```
GitHub
└─ token (user, secret) ← 每个人在设置里填自己的
```

每个成员 own 自己的 token，互不可见。没填的成员调 GitHub 工具时 Agent 提示填。

### 形态 3: 混合 — 团队配置 + 个人身份令牌

例: 飞书开放平台 — app_id / app_secret 是公司应用层 (全员共用)，user_token 是每个员工的飞书身份。

```
飞书开放平台
├─ app_id (team, text)        ← 管理员配
├─ app_secret (team, secret)  ← 管理员配
└─ user_token (user, secret)  ← 每个员工各自授权
```

这是企业 SaaS 最常见模式。管理员搭好底，员工只填自己的 token。

---

## 何时需要凭证

| 用户需求 | 是否需要凭证 |
|---|---|
| 查公开数据 (天气、汇率公开 API) | 不需要 |
| 调外部 SaaS 服务的 API | **需要** (api_key / token) |
| 操作内部企业系统 (飞书 / 钉钉 / 自建 KMS) | **需要** |
| Agent 内部计算 / 数据分析 | 不需要 |
| 推消息到 IM 群 | **需要** (Webhook URL) |

> **关键判断**: 凡是要调外部 SaaS 服务 API，99% 需要凭证。凭证管"我是谁 / 我有权调"，工具 / 技能管"怎么调、调来干嘛"。

凭证 + 工具 / 凭证 + MCP / 凭证 + 技能的组合判断详见 `workflows.md` 流程 3。

---

## Agent 在对话里能做的事

### 创建凭证 / 填字段

调用 `tool-connect` 内置技能 — 它有 `connection_credential` 工具的完整用法 (action: list / inspect / declare / request 等)。Agent 可以在对话里:

- 列出已有连接 (`connection_credential(action="list")`)
- 看某个连接的字段定义 (`action="inspect"`)
- 创建一个**新的自定义连接器** (`action="declare"`)
- 弹一个凭证填写卡让用户当场填字段值 (`action="request"`)

> **永远不要在对话里收凭证明文**。用户把 plaintext key 粘给你，立即告知"不能这样填，我帮你弹一个安全的凭证填写卡" — 通过 `connection_credential(action="request")` 让用户在专用 UI 里填。

### 在脚本里读凭证

Agent 在 `execute_python` / `bash` 里调外部 API 时，**怎么读凭证**直接走 `tool-connect` 内置技能里 **"读取凭据的三种上下文"** 那张表。

简要复习 (具体看 `tool-connect`):

| 在哪写代码 | 怎么读凭据 |
|---|---|
| 自定义工具 `tools/<name>/main.py` 的 `execute(ctx, ...)` | `ctx.connections.get("<slug>").field("<key>")` |
| `execute_python` / `bash` 临时脚本 | 环境变量 `$CVO_CONN_<SLUG>_<FIELD>` (大写) |
| `tool.json` 声明式 API 工具 (url / headers / query) | `${conn:<slug>.<field>}` 占位符 |

---

## Agent 做不到，必须用户手动

这些是**结构性操作**，Agent 自己改不了，必须用户在设置 → 连接凭证里点:

- 改字段值 (改 API Key 等)
- 切换字段所有权 (team ↔ user)
- 改字段定义 (加字段 / 删字段 / 改 type)
- 撤销 OAuth 授权
- 删除整个连接

> Agent 调用 `connection_credential(action="user_action_handbook")` 可以拿到一份操作手册念给用户。

---

## 做不好怎么办: 凭证配齐了但工具还报错

排查顺序:

1. **该工具真的装备到当前 Agent 了吗?** Agent 配置页 → 工具 → 看是不是 enabled
2. **凭证字段名跟工具代码里读的 key 对得上吗?** (slug 大小写敏感，field 大小写敏感)
3. **字段是 team 还是 user?** user 级要看**当前用户**有没有填，不是只 owner 填了就行
4. **API Key 本身过期 / 被吊销?** 去外部 SaaS 后台看一下
5. **OAuth token 刷新机制?** 飞书 / 钉钉的 token 有有效期，到期要重新扫码授权

如果排查完没结论，引导用户在小精灵反馈面板提一条，附上工具名、连接 slug、报错信息。

---

## 常见问题

**Q: 我不想给团队全员用我的 token，但又要团队都能调 GitHub 工具?**

A: 把 token 字段设成 **user** 级 (个人私有)。每个成员各自填自己的，互不可见。**字段定义本身**是 team 共享的 (大家用同一个连接器，只是各填各的 token)。

**Q: 多个连接器 slug 冲突了?**

A: slug 在空间内全局唯一 (格式 `[a-z][a-z0-9_]{1,48}`)，同空间不能有两个 `github`。需要区分时用后缀 (`github_main` / `github_qa`)。

**Q: 个人空间也能用连接凭证吗?**

A: 能。个人空间下"团队"就是你一个人，team 字段 ≈ user 字段，都是你的。

**Q: 自定义连接需要 owner / admin 权限吗?**

A: member 也能创建自定义连接。但**装备**了凭证的工具到 Agent 上仍按 Agent 的发布策略走。

---

## 一行心法

**永远不要在对话里收 API Key 明文** — 用户粘 plaintext，立即引导走 `connection_credential(action="request")` 弹凭证填写卡，或让他去设置 → 连接凭证 自己填。
