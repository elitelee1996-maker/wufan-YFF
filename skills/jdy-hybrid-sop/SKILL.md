---
name: 简道云二开SOP
description: >
  简道云+二开混合架构的六阶段开发SOP与工程架构规范。当用户启动新的简道云二开项目、 需要按标准流程推进开发、或遇到反复返工/bug修复混乱等问题时使用。覆盖从需求锁定到 测试部署的全链路，每阶段含输入物、输出物和质量门禁。支持 Bridge（Flask+HTML）和 Standard（FastAPI+React）两种架构模式。触发词：二开SOP、开发流程、项目启动、 建表规范、工程搭建、原型交付、质量门禁、混合架构开发。
---

# 简道云+二开混合架构开发SOP

## 核心定位

本技能定义简道云二开项目的**标准化开发流程和工程架构规范**。

**解决的问题**：需求没冻结就画原型、原型没确认就写代码、字段ID硬编码、app.py膨胀、
建表未完成就进入开发、基础功能不工作就部署等反复返工问题。

**核心原则**：六阶段流水线 + 六道门禁，门禁不通过不进下一阶段。

## 六阶段总览

```
Phase 1       Phase 2       Phase 3       Phase 4       Phase 5       Phase 6
需求锁定  →   原型交付  →   建表配表  →   工程搭建  →   功能开发  →   测试部署

📋需求规格书   🖥️HTML原型    📊字段映射表   🏗️项目骨架    ✅功能代码    🚀部署包
🔑环境检查单   📝原型验收单   🔗API验证     ⚙️配置文件    📋测试报告    📖运维手册

🚦G1          🚦G2          🚦G3          🚦G4          🚦G5          🚦G6
需求冻结      客户验收      API读写验证   健康检查通过   全链路回归    生产验证
```

### 阶段间铁律

| 规则 | 说明 |
|------|------|
| **不跳阶段** | 不允许从 Phase 1 直接到 Phase 5 |
| **门禁阻塞** | G2 没通过不能建表，G3 没通过不能写业务代码 |
| **变更回溯** | Phase N 变更影响 Phase N-1 输出物时，必须回溯更新并重过门禁 |
| **原型即交付** | Phase 2 的 HTML 原型直接作为生产页面，不做二次重写 |

## 架构模式选择

```
需求复杂度评估
├── 页面 ≤ 15 且 展示/看板为主 且 无复杂状态管理
│   └── Bridge 模式（Flask + Standalone HTML）
├── 页面 > 15 或 多步表单/实时协作/复杂权限
│   └── Standard 模式（FastAPI + React + Docker）
└── 混合场景 → 核心用 Standard，可视化用 Bridge
```

详细决策指南见 `references/phase4-bridge-scaffold.md` 和 `references/phase4-standard-scaffold.md`。

## Phase 1：需求锁定

**目标**：将模糊需求转化为结构化需求规格书，获得客户书面确认。

**输入**：客户沟通记录、行业知识（APQC/七层分析框架）

**输出**：
- 需求规格书（模板见 `references/phase1-requirements-template.md`）
- 环境检查单（API Key权限、简道云版本、服务器资源）
- 架构模式决策记录

### G1 门禁

```
□ 功能清单每项标注"简道云实现"或"二开实现"
□ 用户角色可见范围和关键操作已明确
□ 核心流程步骤和异常分支已描述
□ 数据实体关系已梳理（主表+关联关系）
□ 架构模式已选定并记录理由
□ API Key 已获取且权限已验证
□ 简道云版本已确认
□ 服务器资源已确认
□ 客户已确认需求规格书
```

**阻塞条件**：API Key 未获取、核心功能清单未确认 → 不允许进入 Phase 2。

## Phase 2：原型交付

**目标**：产出高保真可交互 HTML 原型，Bridge模式下直接作为生产页面。

**输入**：Phase 1 需求规格书（已通过 G1）

**输出**：
- HTML 原型文件（每个核心页面一个文件）
- 原型验收单（逐页面功能点确认）
- 页面-功能映射表

**原型规范**：
- Bridge：单文件 HTML，Fine Design CDN，Mock 数据内嵌，所有交互可操作
- Standard：同样用 HTML 做原型，标注需 React 重实现的交互

详细检查清单见 `references/phase2-prototype-checklist.md`。

### 双模式页面分类（🆕 2026-06-14）

> **核心理念**：简道云表单不只是数据库，它同时也是前端交互闭环的一部分。二开页面做"面"（全局聚合），简道云原生页面做"点"（单条记录深度交互），两者通过数据链接双向跳转。

原型设计时，必须对每个页面进行**模式分类**：

| 模式 | 名称 | 做什么 | 简道云做不了的原因 | 典型页面 |
|------|------|--------|-------------------|---------|
| **A：数据汇聚页** | 二开定制页面 | 跨多条数据的聚合展示、复杂计算可视化、批量交互 | 甘特图/日历/网络图等需要自定义渲染和交互 | 甘特图、资源日历、依赖编辑器、预警看板 |
| **B：原生详情页** | 简道云原生页面 | 单条记录的字段编辑、流程审批、智能助手触发、按钮操作 | 不需要二开——简道云原生就有这些能力 | 项目详情、任务详情、资源详情、预警处理 |

**分类判定规则**：
- 页面需要展示**多条数据的聚合视图**（树、图、日历、看板）→ 模式 A
- 页面需要**自定义交互**（拖拽、连线、滑块模拟）→ 模式 A
- 页面只是**单条记录的查看/编辑**→ 模式 B（不需要二开）
- 页面需要**流程审批操作**（提交/回退/转交）→ 模式 B（不需要二开）

**模式 A 页面必须设计"数据链接出口"**：
- 每条数据旁放置链接按钮，点击后打开简道云原生详情页
- 链接格式：`https://www.jiandaoyun.com/open/entry/{entry_id}?data_id={data_id}`
- 用户在简道云详情页完成编辑后，回到汇聚页刷新即可看到最新数据

**模式 B 页面必须设计"智能助手闭环"**：
- 数据变更 → 智能助手触发 → Webhook 调用 Bridge 层 → 重新计算 → 写回简道云
- 确保汇聚页刷新后能看到最新计算结果

在原型验收单中，每个页面必须标注模式 A 或模式 B。

### G2 门禁

```
□ 客户已逐页面确认原型
□ 原型验收单已签署
□ 所有"需修改"项已修复
□ 页面-功能映射表已完成
□ 交互行为已冻结（后续只改数据源）
```

**冻结原则**：验收后只允许改数据源（Mock→API）、样式微调、Bug修复。
不允许改布局结构、交互流程、功能范围。

## Phase 3：建表配表

**目标**：在简道云中完成所有表单创建、字段配置、关联关系，并验证 API 读写。

**输入**：需求规格书（数据实体）、页面-功能映射表

**输出**：
- 表结构文档
- **字段映射表 JSON**（entry_id + widget_id，前后端共用的单一数据字典）
- API 验证报告（每张表 CRUD 验证通过）

**建表顺序**：选项表 → 主表 → 明细表 → 关系表 → 计算字段/聚合表

详细规范见 `references/phase3-table-design-guide.md`。

### G3 门禁

```
□ 每张表 entry_id 已记录到字段映射表（非占位符）
□ 每个字段 widget_id 已记录
□ 关联关系可正常选择
□ 计算字段有值（非空白/报错）
□ 每张表 API create→list→get→update 验证通过
□ 字段映射表 JSON 格式合法
□ 选项表数据已填充
```

**阻塞条件**：entry_id 是占位符、API 验证未通过 → 不允许进入 Phase 4。

## Phase 4：工程搭建

**目标**：搭建项目骨架，确保健康检查通过。

**输入**：架构模式决策、页面-功能映射表、字段映射表 JSON

**输出**：项目骨架、配置文件、/api/health 返回 200、部署配置

### Bridge 模式核心结构

```
{project}/
├── app.py                 # ≤ 200 行，仅路由注册
├── config/
│   ├── field_mapping.json # ★ Phase 3 产出
│   └── settings.py        # 环境配置
├── services/
│   ├── jdy_client.py      # ★ 唯一 JDY API 客户端
│   └── {business}.py      # 业务逻辑（每模块一文件）
├── api/
│   └── {module}_api.py    # API 蓝图（每模块一文件）
├── static/                # Phase 2 原型（直接作为生产页面）
├── requirements.txt
├── deploy.sh
└── {project}.service      # systemd
```

### 关键设计原则

| 原则 | 说明 |
|------|------|
| app.py ≤ 200 行 | 只做路由注册，不含业务逻辑 |
| JDYClient 唯一实现 | services/jdy_client.py 是唯一 API 客户端 |
| 配置驱动 | 所有 entry_id/widget_id 从 field_mapping.json 读取 |
| 业务模块隔离 | 每个模块一个 api 文件 + 一个 service 文件 |
| 原型即页面 | static/ 下就是 Phase 2 原型，只改数据源 |

详细脚手架见 `references/phase4-bridge-scaffold.md` 和 `references/phase4-standard-scaffold.md`。
代码模板见 `templates/` 目录。

### G4 门禁

```
□ 目录结构符合规范
□ field_mapping.json 可被代码加载
□ jdy_client.py 初始化成功
□ /api/health 返回 200 + jdy_configured: true
□ 所有 HTML 原型已复制到 static/
□ 路由正确（每个页面可访问）
□ systemd 含 --timeout 120
□ Nginx proxy_read_timeout ≥ 120s
□ 无硬编码 entry_id/widget_id（grep 验证）
```

## Phase 5：功能开发

**目标**：将原型 Mock 数据替换为真实 API 调用。

**输入**：HTML 原型（G2通过）、字段映射表（G3通过）、项目骨架（G4通过）

**开发流程**（对每个页面）：
1. 后端：API 路由 + 业务逻辑（从 field_mapping.json 读字段ID）
2. 后端：单元测试（happy path + 1 error case）
3. 前端：Mock → API 调用
4. 前端：loading/error/空数据处理
5. 联调验证
6. 按功能清单逐项自测
7. **双模式链接嵌入**（🆕 模式 A 页面必做）

详细编码规范见 `references/phase5-coding-standards.md`。

### 双模式链接嵌入规范（🆕 2026-06-14）

> 模式 A（数据汇聚页）和模式 B（简道云原生详情页）之间通过**数据链接**双向跳转。这是混合架构的核心交互纽带。

#### 链接嵌入方式

| 场景 | 实现方式 | 代码示例 |
|------|---------|---------|
| 汇聚页 → 原生详情页 | 每条数据旁放链接按钮 | `<a href="https://jdy.com/open/entry/{entry_id}?data_id={id}" target="_blank">📄 详情</a>` |
| 原生详情页 → 汇聚页 | 简道云链接字段，URL公式拼接 | `CONCAT("https://server.com/gantt?project_id=", 项目ID)` |
| 详情页编辑后回到汇聚页 | 用户手动切换或汇聚页定时刷新 | `setInterval(refreshData, 30000)` 或 WebSocket |

#### 数据闭环链路

```
用户在汇聚页(模式A)发现异常
  → 点击数据链接跳转到简道云详情页(模式B)
    → 在详情页编辑字段（原生CRUD）
      → 智能助手检测到数据变更
        → Webhook调用Bridge层重新计算
          → Bridge层写回计算结果到简道云
            → 用户回到汇聚页刷新，看到最新数据
```

#### 编码检查项

- [ ] 模式 A 页面中每条数据都有跳转链接
- [ ] 链接 URL 使用 field_mapping.json 中的 entry_id，不硬编码
- [ ] 链接 target="_blank" 在新窗口打开
- [ ] 汇聚页有刷新机制（手动按钮或定时）
- [ ] Bridge 层有 Webhook 接收端点（接收智能助手回调）

### G5 门禁

```
□ 功能清单每项已实现并可操作
□ Mock 数据已全部替换为 API 调用
□ 表单提交后简道云可查到数据（API 回查）
□ 列表/表格正确显示简道云数据
□ 错误处理覆盖：超时/限流/格式错误
□ 无 console 报错 / 无未捕获异常
□ 多步操作中间失败不导致数据不一致
□ 性能可接受（页面 < 3s，查询 < 5s）
□ 模式 A 页面每条数据有跳转链接（🆕 双模式）
□ 链接 URL 使用 FieldMapper 读取 entry_id，不硬编码
□ Bridge 层 Webhook 端点可接收智能助手回调
```

## Phase 6：测试部署

**目标**：全链路回归测试 + 生产环境部署验证。

**输入**：功能代码（G5通过）

**输出**：测试报告、部署包、运维手册

**回归测试**：身份识别 → 核心流程 happy path → 数据写入验证 → 异常场景 → 权限验证 → 性能验证

详细部署指南见 `references/phase6-deployment-guide.md`。

### G6 门禁

```
□ 生产环境 /api/health 正常
□ 核心流程在生产环境走通
□ 生产 API Key 权限已验证
□ 日志可正常输出
□ 运维手册已交付
□ 客户已在生产环境确认
```

## 工程稳健性要点

### 配置驱动（消灭硬编码）

```python
# FieldMapper 提供语义化访问
fm = FieldMapper()
widget = fm.widget("project", "project_name")  # → "_widget_1781178100748"
```

模板见 `templates/field_mapper.py`。

### 统一错误处理

```python
# 所有 API 响应统一格式
{"success": true/false, "data": ..., "error": ...}
```

### 数据写入三步验证

创建 → 回查 → 验证关键字段非空。不能只看 HTTP 200。

### 前端 API 客户端

BASE_URL 用 `window.location.origin`，不硬编码 IP。
模板见 `templates/api_client.js`。

## 参考文档索引

| 文档 | 内容 |
|------|------|
| `references/phase1-requirements-template.md` | 需求规格书模板 |
| `references/phase2-prototype-checklist.md` | 原型开发与验收检查清单 |
| `references/phase3-table-design-guide.md` | 建表规范与字段映射表格式 |
| `references/phase4-bridge-scaffold.md` | Bridge 模式工程脚手架 |
| `references/phase4-standard-scaffold.md` | Standard 模式工程脚手架 |
| `references/phase5-coding-standards.md` | 编码规范与最佳实践 |
| `references/phase6-deployment-guide.md` | 部署与运维指南 |

## 代码模板索引

| 模板 | 用途 |
|------|------|
| `templates/app_bridge.py` | Bridge 模式 Flask 主应用模板 |
| `templates/jdy_client.py` | JDYClient 标准实现 |
| `templates/field_mapper.py` | FieldMapper 配置驱动类 |
| `templates/api_client.js` | 前端 API 客户端模板 |
| `templates/deploy.sh` | 部署脚本模板 |

## 与现有技能的关系

| 技能 | 关系 |
|------|------|
| jdy-hybrid-framework | 被本SOP引用，设计原则不变 |
| jdy-app-architecture | Phase 1 使用 |
| jdy-architecture-patterns | Phase 3 使用 |
| jdy-custom-dev-capabilities | Phase 1 能力边界评估 |
| jdy-framework-generator | Phase 4 代码生成 |
| prototype-designer | Phase 2 原型设计 |