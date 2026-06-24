---
name: 产品手册
description: "悟帆 (WuFan AI) 平台的产品知识与操作手册。三类触发: ① 用户问产品层概念或操作 (空间、智能体资产、连接凭证、飞书钉钉企微集成、大模型接入、流动版受控版、分享、邀请成员、反馈); ② 用户想要建主 Agent / 建伙伴 / 接外部能力 / 切版本 / 接自有模型等典型流程; ③ Agent 自己在某类任务上反复做不好需要找改进方向。给真实正确的产品知识与操作指引, 杜绝“以为能做实际不能 / 以为做不到实际能 / 瞎编”三类幻觉。"
---

# 悟帆产品手册

平台理念是**"用户和 Agent 对话解决一切"**。所有需要建造、连接、装配的事 — 优先在对话里由 Agent 主导完成；用户手动操作是兜底。

但 Agent 对自己背后这个产品的理解是有限的，会出现三类典型幻觉:

1. **以为自己能做** — 实际是用户必须手动操作的事，Agent 编了一段"代码方案"应付
2. **以为做不到** — 平台明明有现成功能，Agent 却让用户"自己想办法"
3. **瞎编** — 路径、按钮名、参数名、限制规则，全凭通用经验猜

本技能给真实正确的产品知识、操作路径与"做不好时怎么办"的方向。

## 何时使用本技能

按用户的提问类型，按需读对应文档。**不要一次读全 7 份**。

| 用户在问什么 | 读哪份 |
|---|---|
| 概念解释: "什么是空间 / 资产 / 凭证 / 流动版 / MCP / 频道?" | `references/concepts.md` |
| 接入飞书 / 钉钉 / 企业微信 (CLI、群里 @bot、群推送) | `references/channels-im.md` |
| 接外部服务凭证 (GitHub、Notion、自建 API、企查查 ...) | `references/connections.md` |
| 找 / 装 / 装备资产 (技能、工具、伙伴、MCP、卡片、能力套件) | `references/assets-management.md` |
| 整体流程: "我想建一个 Agent / 接 X 能力 / 邀请成员 / 切版本 / 接自己的模型 / 分享" | `references/workflows.md` |
| 用户反复说"还是不对" / Agent 同类任务一直做不好 | `references/task-troubleshoot.md` |
| 用户想反馈 bug、提建议、吐槽 | `references/feedback.md` |

## 平台为创建/安装资产准备的内置技能 (在对话里随时调用)

涉及具体怎么造资产时，在对话里直接调用对应内置技能即可。这些技能由平台为各自场景专门准备，里面的步骤、模板、最佳实践是最权威的:

| Agent 想做的事 | 调用哪个内置技能 |
|---|---|
| 创建自定义工具 / 配置连接凭证 / 在脚本里读凭证 | `tool-connect` (工具与连接) |
| 创建、安装、调整技能；写 SKILL.md；拆 references | `skill-creator` (技能创建) |
| 安装 MCP server，配置 mcp.json，STDIO/SSE 模式 | `mcp-installer` (MCP 服务安装) |
| 创建子 Agent / 伙伴，写 agent.md，设计能力边界 | `subagent-creator` (伙伴创建) |

## 三条铁律

- **不照搬** — 文档给的是产品的事实，根据用户的具体上下文 (个人空间还是团队空间? 是 owner 还是 member? 是流动版还是受控版?) 给量身指引。
- **不瞎编** — 文档里没说的事，不要凭"通用平台经验"猜。真不知道就老实说"我不太确定，建议直接到[对应入口]看一下，或在小精灵反馈面板里提一条让团队确认"。
- **指路精准** — 涉及操作时，给到 (a) 入口在哪 (b) 关键步骤 (c) 可能的限制或前置条件。别只说"在设置里"。

## references 索引

| 文件 | 内容 |
|---|---|
| [`concepts.md`](./references/concepts.md) | 核心概念字典 |
| [`workflows.md`](./references/workflows.md) | 典型流程: 建主 Agent / 建伙伴 / 接外部能力 / 邀请成员 / 切版本 / 接自有模型 / 分享 |
| [`channels-im.md`](./references/channels-im.md) | 飞书 / 钉钉 / 企业微信集成 (CLI vs 频道 vs 自定义群推送) |
| [`connections.md`](./references/connections.md) | 连接凭证: 团队字段 vs 个人字段、组合形态 |
| [`assets-management.md`](./references/assets-management.md) | 资产探索 / 安装 / 装备 / 删除 / 发布 |
| [`task-troubleshoot.md`](./references/task-troubleshoot.md) | 任务做不好时的诊断与改进 |
| [`feedback.md`](./references/feedback.md) | 反馈通道与撰写指引 |

## 一行铁律

**不知道就老实说"不确定"，不要瞎编产品功能** — 用户因为信任 Agent 而问，错误指引比"不确定"杀伤力大 100 倍。
