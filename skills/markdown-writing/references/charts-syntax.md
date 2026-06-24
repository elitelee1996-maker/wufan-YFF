# Charts 语法参考

这是悟帆 `ChartRenderer` 支持的 charts 代码块语法参考。

> **重要原则**
> 
> 1. **charts 不是必需的**。文学体(散文、日记、随笔)不要使用 charts。
> 2. **数据必须真实**。所有 charts 里的数据来源于你掌握的事实,**严禁编造**。
> 3. **克制使用**。一篇 Markdown 一般不超过 3–5 个 charts;每个主要章节 0–2 个为宜。
> 4. **JSON 必须合法**。键名完全匹配,字符串用双引号,避免尾逗号。渲染失败时前端会降级为原始 JSON 展示。

## 基本语法

在 Markdown 中用 ` ```charts ` 代码块包裹 JSON:

` ` `charts
{
  "type": "...",
  "title": "...",
  ...
}
` ` `

(实际写作去掉反引号之间的空格)

---

## 一、数据展示类

### table — 多维数据对比(最常用)

用于并列对比多项之间的多个属性。

```json
{
  "type": "table",
  "title": "主流 SaaS 工具对比",
  "columns": ["产品", "价格", "核心优势", "市场份额"],
  "data": [
    ["Notion", "¥99/月", "all-in-one 笔记", "35%"],
    ["Obsidian", "免费", "本地 Markdown + 插件", "28%"],
    ["Logseq", "免费", "大纲 + 块引用", "12%"]
  ]
}
```

### bar — 柱状图(数值对比)

```json
{
  "type": "bar",
  "title": "各产品月活用户数(单位:万)",
  "data": [
    {"category": "产品 A", "value": 1250},
    {"category": "产品 B", "value": 860},
    {"category": "产品 C", "value": 520}
  ]
}
```

### pie — 饼图(占比分布)

```json
{
  "type": "pie",
  "title": "2026 Q1 营收来源占比",
  "data": [
    {"category": "订阅收入", "value": 62},
    {"category": "企业授权", "value": 25},
    {"category": "增值服务", "value": 13}
  ]
}
```

### line — 折线图(趋势变化)

```json
{
  "type": "line",
  "title": "月活用户增长趋势",
  "xAxis": ["2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03"],
  "series": [
    {"name": "DAU(万)", "data": [42, 48, 55, 61, 68, 76]},
    {"name": "MAU(万)", "data": [380, 410, 445, 485, 520, 560]}
  ]
}
```

### metrics — 关键指标卡片

```json
{
  "type": "metrics",
  "title": "本季度核心指标",
  "data": [
    {"label": "营收", "value": "15.7 亿", "change": "+12%", "trend": "up"},
    {"label": "客户数", "value": "36,000+", "change": "+8%", "trend": "up"},
    {"label": "续约率", "value": "92%", "change": "-1%", "trend": "down"},
    {"label": "NPS", "value": "48"}
  ]
}
```

`trend` 可选值:`"up"` / `"down"` / `"flat"`。

### combo — 组合图(柱 + 线)

适合同时展示"绝对量"和"比率"。

```json
{
  "type": "combo",
  "title": "订单量与转化率",
  "xAxis": ["1 月", "2 月", "3 月", "4 月"],
  "bars": [{"name": "订单量", "data": [1200, 1450, 1680, 1820]}],
  "lines": [{"name": "转化率(%)", "data": [3.2, 3.8, 4.1, 4.5]}]
}
```

---

## 二、结构展示类

### comparison — 两方 / 多方对比

```json
{
  "type": "comparison",
  "title": "自研 vs 采购方案",
  "items": [
    {"dimension": "初期投入", "自研": "高(约 200 万)", "采购": "低(约 30 万)"},
    {"dimension": "长期成本", "自研": "低", "采购": "高(年费)"},
    {"dimension": "灵活性", "自研": "完全自主", "采购": "受限于厂商路线图"},
    {"dimension": "上线周期", "自研": "6–9 个月", "采购": "2–4 周"}
  ]
}
```

### timeline — 时间线 / 发展历程

```json
{
  "type": "timeline",
  "title": "产品发展历程",
  "data": [
    {"period": "2024 Q1", "events": "内部孵化,完成第一版原型"},
    {"period": "2024 Q4", "events": "首个付费客户签约"},
    {"period": "2025 Q3", "events": "完成 Pre-A 轮融资"},
    {"period": "2026 Q1", "events": "SaaS 与本地版双线公测"}
  ]
}
```

### mindmap — 思维导图(层级结构)

```json
{
  "type": "mindmap",
  "title": "核心竞争力拆解",
  "root": "核心竞争力",
  "children": [
    {
      "name": "技术壁垒",
      "children": ["自研 Agent 引擎", "多模态编排", "上下文压缩专利"]
    },
    {
      "name": "产品力",
      "children": ["开箱即用", "极简交互", "深度个性化"]
    },
    {
      "name": "生态",
      "children": ["开发者社区", "Skill 市场", "MCP 生态接入"]
    }
  ]
}
```

### flowchart — 流程 / 决策图

```json
{
  "type": "flowchart",
  "title": "技术选型决策流程",
  "nodes": [
    {"id": "start", "label": "评估需求", "children": ["scale", "budget"]},
    {"id": "scale", "label": "用户量 > 10 万?", "children": ["cloud", "self"]},
    {"id": "budget", "label": "预算是否紧张?"},
    {"id": "cloud", "label": "选云原生方案", "description": "交付快、弹性好"},
    {"id": "self", "label": "选自建方案", "description": "可控、长期成本低"}
  ]
}
```

### radar — 雷达图(多维能力评估)

```json
{
  "type": "radar",
  "title": "产品能力评估",
  "dimensions": ["功能完整度", "易用性", "性能", "生态", "性价比"],
  "series": [
    {"name": "产品 A", "data": [9, 8, 7, 6, 8]},
    {"name": "产品 B", "data": [7, 9, 8, 8, 7]},
    {"name": "产品 C", "data": [6, 7, 9, 5, 9]}
  ]
}
```

### matrix — 矩阵(2×2 / 4 象限)

```json
{
  "type": "matrix",
  "title": "项目优先级矩阵",
  "xAxis": {"label": "重要性", "low": "低", "high": "高"},
  "yAxis": {"label": "紧急度", "low": "低", "high": "高"},
  "items": [
    {"name": "项目 A", "x": 9, "y": 8, "quadrant": "立即做"},
    {"name": "项目 B", "x": 8, "y": 3, "quadrant": "排期"},
    {"name": "项目 C", "x": 3, "y": 9, "quadrant": "授权别人做"},
    {"name": "项目 D", "x": 2, "y": 2, "quadrant": "不做"}
  ]
}
```

### roadmap — 路线图

```json
{
  "type": "roadmap",
  "title": "2026 年产品路线",
  "phases": [
    {
      "period": "Q1",
      "theme": "稳定性与性能",
      "items": ["核心模块重构", "上下文压缩 v2", "监控大盘上线"]
    },
    {
      "period": "Q2",
      "theme": "生态开放",
      "items": ["Skill 市场公测", "MCP 全量开放", "SDK v1.0"]
    },
    {
      "period": "Q3",
      "theme": "企业能力",
      "items": ["多租户完善", "企业 SSO", "审计合规"]
    }
  ]
}
```

---

## 三、总结 / 摘要类

### summary — 核心洞察摘要

```json
{
  "type": "summary",
  "title": "核心结论",
  "insights": [
    {"title": "市场格局已定", "description": "头部 3 家占据 80% 份额,新进入者窗口期不足 12 个月。"},
    {"title": "企业客户更看重服务", "description": "60% 的采购决策由'本地部署 + 实施团队'驱动,而非单纯功能。"},
    {"title": "开源社区是试金石", "description": "拥有健康开源生态的产品付费转化率高出行业均值 2.3 倍。"}
  ]
}
```

### rating — 评分 / 评级

```json
{
  "type": "rating",
  "title": "综合评级",
  "ratings": [
    {"dimension": "推荐指数", "score": 4, "max": 5},
    {"dimension": "风险等级", "level": "低", "note": "财务健康、团队稳定"},
    {"dimension": "发展潜力", "score": 5, "max": 5}
  ]
}
```

### scorecard — 计分卡

```json
{
  "type": "scorecard",
  "title": "Q1 团队绩效卡",
  "items": [
    {"metric": "交付准时率", "actual": "96%", "target": "95%", "status": "pass"},
    {"metric": "线上故障数", "actual": "1", "target": "≤ 2", "status": "pass"},
    {"metric": "客户 NPS", "actual": "42", "target": "50", "status": "watch"}
  ]
}
```

`status` 可选:`"pass"` / `"watch"` / `"fail"`。

---

## 四、列表 / 字典类

### list — 结构化列表

比普通 Markdown 列表更强的列表;适合"标题 + 副标题 + 正文"的条目。

```json
{
  "type": "list",
  "title": "本周重点",
  "items": [
    {
      "title": "A 项目上线",
      "subtitle": "灰度 3 天 → 全量",
      "description": "当前日活稳定在 XX,P99 延迟 120ms,暂无 P0 反馈。"
    },
    {
      "title": "B 项目联调",
      "subtitle": "进行中 · 60%",
      "description": "已完成登录、权限、核心业务三大接口,剩余 2 个边缘接口预计下周三前完成。"
    }
  ]
}
```

### glossary — 术语表

```json
{
  "type": "glossary",
  "title": "专有名词解释",
  "items": [
    {"term": "ReAct", "definition": "一种 Agent 执行范式:Reason → Act → Observe 循环。"},
    {"term": "Context Compression", "definition": "在对话 token 超过模型上下文窗口时,对历史消息进行摘要或掩码以腾出空间。"},
    {"term": "BYOK", "definition": "Bring Your Own Key,用户自带 LLM API Key,而非使用平台统一密钥。"}
  ]
}
```

---

## 五、最佳实践

1. **每个 chart 必有标题**:`title` 字段不要省略,它是阅读锚点。
2. **控制条目数量**:`bar` / `pie` / `table` 的数据行数建议 3–10 条,超过时拆分成多个 chart 或用 `table`。
3. **`radar` 维度 3–6 个最佳**:过多会让图变得密不透风。
4. **`timeline` 事件 3–8 条**:过长考虑切成两条 timeline 或用 `roadmap` 分阶段。
5. **不要为了用 chart 而用 chart**:如果一张图传达的信息不如一句话清楚,就用一句话。

## 常见错误

- ❌ 在 `table.data` 里混用字符串和数字,导致列宽不稳——**统一用字符串**。
- ❌ 在 `line.series[].data` 里放 `null`——前端会断线,改用 0 或直接不画。
- ❌ 忘记 `"type"` 字段或拼错成 `"Type"`/`"kind"`——大小写敏感,必须 `"type"`。
- ❌ JSON 里出现尾逗号或单引号——**标准 JSON 语法**,不是 JavaScript 对象字面量。

## 渲染失败时的降级

如果 `ChartRenderer` 无法解析你的 JSON,前端会把代码块原样展示为一段预格式化文本。这不是灾难性的——只是不好看。但仍应尽量保证 JSON 合法。
