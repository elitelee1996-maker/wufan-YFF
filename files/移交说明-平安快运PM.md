# 平安快运项目管理系统 — 移交工作包说明

> **移交人**: 李琦  
> **移交日期**: 2026-06-16  
> **项目名称**: 平安快运项目管理（pingankuaiyun-pm）  
> **架构模式**: Bridge 单体架构（Flask 后端 + 单页 HTML 前端）

---

## 一、项目概述

平安快运项目管理系统是一个**简道云 + 二开混合架构**项目，为平安大件运输业务提供项目计划铺排、WBS 任务管理、依赖关系编排、资源日历管理等功能。系统通过 iframe 嵌入简道云详情页使用。

### 核心能力

| 模块 | 功能 | 状态 |
|------|------|------|
| 项目计划铺排 | 左右分屏：左侧任务清单+依赖标签，右侧甘特图 | ✅ 已上线 v3 |
| 依赖关系管理 | 编辑弹窗（左右分栏：左侧表单+右侧实时网络图） | 🔄 原型已确认，待集成 |
| 资源日历 | 资源占用可视化日历 | ✅ 已上线 |
| 正向推算 | CPM 关键路径计算 | ✅ 已上线 |
| 版本管理 | 基线保存/对比 | ✅ 已上线 |
| 模板导入 | 从简道云模板导入项目计划 | ✅ 已上线 |

---

## 二、服务器与部署信息

### 服务器

| 项目 | 值 |
|------|-----|
| 域名 | `frank.minitool.top` |
| SSH | `ssh deploy@frank.minitool.top` (端口 22) |
| 项目路径 | `/home/deploy/apps/pingankuaiyun-pm/` |
| 后端端口 | `8201` |
| 运行方式 | systemd + gunicorn (2 worker, timeout 120s) |

### 目录结构

```
/home/deploy/apps/pingankuaiyun-pm/
├── backend/
│   ├── app.py              # Flask 主程序（1159行，单文件架构）
│   ├── requirements.txt    # Flask, Flask-CORS, requests, gunicorn
│   ├── .env                # 环境变量（简道云 API Key）
│   ├── venv/               # Python 虚拟环境
│   ├── check_*.py          # 数据检查脚本（调试用）
│   ├── test_*.py           # 测试脚本（E2E、性能、批量）
│   └── inspect_wbs.py      # WBS 数据检查工具
└── frontend/
    ├── plan-scheduling-v3.html      # ⭐ 主页面（当前生产版本，4322行）
    ├── plan-scheduling-v2.html      # v3 内容（与 v3 同步）
    ├── plan-scheduling-v2.html.bak  # v2 原始备份
    ├── plan-scheduling-v3.html.bak  # v3 原始备份
    ├── plan-scheduling.html         # v1 原始版本
    ├── resource-calendar.html       # 资源日历页面
    ├── prototype-D-split.html       # ⭐ 依赖编辑弹窗原型（已确认方案）
    ├── prototype-D-mini.html        # 迷你缩略图原型（备选）
    └── prototype-A-fab.html         # 悬浮按钮原型（备选）
```

### Nginx 配置

位于 `/etc/nginx/conf.d/frank.conf`，关键规则：

```nginx
# 静态文件（前端 HTML）
location /pingankuaiyun-pm/ {
    root /home/deploy/apps;
    try_files $uri $uri/ @pm_fallback;
    # iframe 嵌入简道云所需的 CORS 头
    add_header X-Frame-Options "ALLOW-FROM https://www.jiandaoyun.com" always;
    add_header Content-Security-Policy "frame-ancestors 'self' https://www.jiandaoyun.com https://*.jiandaoyun.com" always;
}

# API 代理到 Flask
location /pingankuaiyun-pm/api/ {
    proxy_pass http://127.0.0.1:8201/api/;
}
```

### 常用运维命令

```bash
# 查看服务状态
sudo systemctl status pingankuaiyun-pm

# 重启服务（修改后端代码后）
sudo systemctl restart pingankuaiyun-pm

# 查看日志
sudo journalctl -u pingankuaiyun-pm -f

# 前端 HTML 更新不需要重启（nginx 直接读取磁盘文件）
# 只需 SFTP 上传覆盖即可
```

### 访问地址

| 页面 | URL |
|------|-----|
| 项目计划铺排（生产） | `https://frank.minitool.top/pingankuaiyun-pm/plan-scheduling-v2.html` |
| 项目计划铺排 v3 | `https://frank.minitool.top/pingankuaiyun-pm/plan-scheduling-v3.html` |
| 资源日历 | `https://frank.minitool.top/pingankuaiyun-pm/resource-calendar.html` |
| 依赖编辑原型 | `https://frank.minitool.top/pingankuaiyun-pm/prototype-D-split.html` |
| API 健康检查 | `https://frank.minitool.top/pingankuaiyun-pm/api/health` |

> **注意**: 生产环境使用 v2 URL（内容为 v3），因为简道云 iframe 配置的是 v2 地址。

---

## 三、简道云集成配置

### 应用信息

| 项目 | 值 |
|------|-----|
| 简道云 App ID | `6a221e4c7a414a370a2f0ebe` |
| API Key | 存储在 `.env` 文件的 `CVO_CONN_JDY_PINGANKUAIYUN_PM_API_KEY` |
| API 基础 URL | `https://api.jiandaoyun.com/api/v5` |

### 表单 Entry ID 映射

| 业务表 | Entry ID | 用途 |
|--------|----------|------|
| **模板体系** | | |
| 项目计划模板 | `6a2980a05ef2138f4eb96d95` | 模板库 |
| 标准任务清单 | `6a2983071f700c07107b7829` | 模板下的标准任务 |
| 计划任务依赖关系 | `6a2986bba0998e2b671fd432` | 模板任务的依赖 |
| 任务负责人角色选项 | `6a2984645591d3de7361d858` | 角色下拉选项 |
| 资源类型选项 | `6a29849c767d1ae9f7628435` | 资源类型下拉 |
| **项目执行体系** | | |
| 项目计划 | `6a221e50149908216c2d30a6` | 项目主表 |
| 项目任务清单(WBS) | `6a2ad5352af7b21519d2bcc2` | WBS 节点 |
| 项目任务依赖关系 | `6a2ad723ec48001a5816a88c` | 任务间依赖 |
| **资源管理** | | |
| 外部资源库 | `6a288d8faf5ba611720f2da1` | 资源主表 |
| 外部资源占用情况 | `6a288eaed76e024835d0f30a` | 资源占用记录 |
| 外部资源绑定 | `6a288ca32e46716f12e356eb` | 资源绑定关系 |

> **注意**: `resource_unavailable`、`resource_conflict`、`conflict_decision`、`warning`、`action_item`、`version_snapshot` 这几个 Entry ID 在代码中仍为占位符（`XXX_TABLE_ENTRY_ID`），对应的简道云表尚未创建。

---

## 四、后端 API 路由清单

后端 `app.py` 共 23 个路由，按功能分组：

### 系统

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/` | 首页（重定向到 index.html） |
| GET | `/api/health` | 健康检查 |

### 项目管理

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/api/projects` | 项目列表 |
| GET | `/api/projects/<id>` | 项目详情 |
| POST | `/api/projects` | 创建项目 |
| PUT | `/api/projects/<id>` | 更新项目 |

### WBS 任务

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/api/wbs/<project_id>` | 获取项目 WBS 树 |
| POST | `/api/wbs/<project_id>` | 批量保存 WBS（含依赖） |
| POST | `/api/wbs/<project_id>/forward-pass` | 运行正向推算（CPM） |

### 依赖关系

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/api/dependencies/<project_id>` | 获取依赖列表 |
| POST | `/api/dependencies/<project_id>` | 批量保存依赖 |

### 资源管理

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/api/resources` | 资源列表 |
| POST | `/api/resources` | 创建资源 |
| GET | `/api/resources/occupation` | 资源占用查询 |
| POST | `/api/resources/occupation` | 创建资源占用 |

### 模板

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/api/templates` | 模板列表 |
| GET | `/api/templates/<id>` | 模板详情（含任务+依赖） |
| POST | `/api/templates` | 创建模板 |
| POST | `/api/templates/<id>/apply` | 应用模板到项目 |

### 版本管理

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/api/versions/<project_id>` | 版本列表 |
| POST | `/api/versions/<project_id>` | 创建版本快照 |

### 成员

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/api/members` | 成员列表 |

---

## 五、前端版本演进

| 版本 | 文件 | 行数 | 关键特性 | 状态 |
|------|------|------|---------|------|
| v1 | `plan-scheduling.html` | 3762 | 基础版：任务列表+甘特图 | 已废弃 |
| v2 | `plan-scheduling-v2.html.bak` | 4321 | +依赖标签+网络图+依赖编辑弹窗+行高亮 | 已备份 |
| v3 | `plan-scheduling-v3.html` | 4322 | 修复网络图布局（按 level 分列） | ⭐ 当前生产 |
| 原型D | `prototype-D-split.html` | 779 | 依赖编辑弹窗左右分栏（左表单+右实时网络图） | ⭐ 已确认，待集成 |

### v3 → 下一步的待办

1. **将 prototype-D-split.html 的依赖编辑弹窗集成到 v3**  
   - 当前 v3 的依赖编辑弹窗是单栏布局（表单在上，网络图在下方折叠区）
   - 已确认的方案是左右分栏：左侧操作表单，右侧实时网络图预览
   - 原型文件 `prototype-D-split.html` 已完整实现所有交互

2. **补建缺失的简道云表**  
   - `resource_unavailable`（资源不可用时段）
   - `resource_conflict`（资源冲突记录）
   - `conflict_decision`（冲突决策记录）
   - `warning`（预警记录）
   - `action_item`（行动项）
   - `version_snapshot`（版本快照）

---

## 六、设计决策记录

### 6.1 网络图布局修复（已完成）

**问题**: 原网络图只画叶子节点，拓扑排序导致节点挤在一起  
**方案**: 改用任务层级(level)作为列号，同层按编号排序  
**效果**: Level 1 → 第1列，Level 2 → 第2列，Level 3 → 第3列  
**汇总任务**: 虚线边框 + 更大尺寸区分

### 6.2 网络图展示方式（已确认方案D-分栏）

**背景**: 页面嵌入简道云详情页后，任务列表很长，底部网络图被淹没  
**备选方案**:
- A. 悬浮按钮 + 弹窗 → 原型已做，不占空间但无信息密度
- D. 迷你缩略图 + 点击放大 → 原型已做，常驻可见但可能遮挡

**最终决策**: 网络图只在编辑依赖关系时才有意义，因此不做独立入口，而是将网络图嵌入依赖编辑弹窗的右侧，形成**左右分栏**布局：
- 左侧：紧前活动列表 + 紧后活动列表（只读）+ 添加依赖表单
- 右侧：实时依赖关系网络图（随操作动态刷新）

**交互细节**:
- 添加依赖后，新依赖线用虚线动画高亮
- 当前编辑任务用绿色粗边框标识
- 紧前节点绿色底，紧后节点橙色底，其他节点淡化
- 支持缩放和 Tooltip

### 6.3 页面布局（已确认）

左右分屏：左侧任务清单（520px 固定宽度），右侧甘特图（弹性宽度）

---

## 七、工作包文件清单

```
平安快运PM-移交工作包/
├── 📄 移交说明-平安快运PM.md          ← 本文档
│
├── 📁 后端代码/
│   ├── app.py                         # Flask 主程序（1159行）
│   ├── requirements.txt               # Python 依赖
│   └── .env                           # 环境变量（含 API Key）
│
├── 📁 前端代码/
│   ├── plan-scheduling-v3.html        # ⭐ 当前生产版本
│   ├── plan-scheduling-v2.html.bak    # v2 备份
│   ├── plan-scheduling.html           # v1 原始版本
│   └── resource-calendar.html         # 资源日历
│
├── 📁 原型文件/
│   ├── prototype-D-split.html         # ⭐ 依赖编辑弹窗（已确认方案）
│   ├── prototype-D-mini.html          # 迷你缩略图方案（备选）
│   └── prototype-A-fab.html           # 悬浮按钮方案（备选）
│
├── 📁 部署配置/
│   ├── pingankuaiyun-pm.service       # systemd 服务文件
│   └── nginx-config-snippet.conf      # nginx 配置片段
│
├── 📁 测试脚本/
│   ├── test_e2e.py                    # 端到端测试
│   ├── test_perf.py                   # 性能测试
│   ├── test_batch.py                  # 批量操作测试
│   ├── test_save.py                   # 保存功能测试
│   └── test_timing.py                 # 时序测试
│
├── 📁 数据检查脚本/
│   ├── check_all.py                   # 全量数据检查
│   ├── check_codes.py                 # 编码检查
│   ├── check_data.py                  # 数据完整性检查
│   ├── check_grade.py                 # 等级检查
│   ├── check_project.py              # 单项目检查
│   ├── check_projects.py             # 多项目检查
│   └── inspect_wbs.py                # WBS 结构检查
│
└── 📁 项目评估文档/
    ├── 平安快运PM项目-综合评估报告.md  # 项目评估报告
    ├── ipd_requirement_doc.md          # IPD 需求文档
    └── knowledge_retrieval_report.md   # 经验检索报告
```

---

## 八、快速上手指南

### 1. 连接服务器

```bash
ssh deploy@frank.minitool.top
# 密码请联系李琦获取
```

### 2. 查看当前运行状态

```bash
# 后端服务
sudo systemctl status pingankuaiyun-pm

# API 健康检查
curl https://frank.minitool.top/pingankuaiyun-pm/api/health
```

### 3. 更新前端页面

```bash
# 前端是纯静态 HTML，直接 SFTP 上传覆盖即可
# 不需要重启任何服务（nginx 直接读取磁盘文件）
scp your-file.html deploy@frank.minitool.top:/home/deploy/apps/pingankuaiyun-pm/frontend/
```

### 4. 更新后端代码

```bash
# 1. 上传 app.py
scp app.py deploy@frank.minitool.top:/home/deploy/apps/pingankuaiyun-pm/backend/

# 2. 重启服务
ssh deploy@frank.minitool.top
sudo systemctl restart pingankuaiyun-pm

# 3. 检查日志
sudo journalctl -u pingankuaiyun-pm -f --no-pager -n 50
```

### 5. 下一步开发重点

将 `prototype-D-split.html` 中的依赖编辑弹窗集成到 `plan-scheduling-v3.html`：

1. 打开 `prototype-D-split.html`，找到 `<!-- Dependency Edit Modal -->` 部分
2. 将弹窗 HTML、CSS（`.dep-modal` 相关）、JS（`openDepModal`、`renderDepGraph` 等函数）移植到 v3
3. 替换 v3 中原有的 `dep-modal` 相关代码
4. 测试所有交互：添加依赖→右侧图实时更新、删除依赖→图刷新、循环检测

---

## 九、已知问题与风险

| # | 问题 | 严重程度 | 说明 |
|---|------|---------|------|
| 1 | 6 个 Entry ID 为占位符 | 中 | `resource_unavailable` 等表未建，相关 API 会报错 |
| 2 | 认证装饰器未实现 | 低 | `require_api_key` 装饰器目前是空操作，生产环境需补充 |
| 3 | `list_data_full` 逐条查询 | 中 | 数据量大时性能差，建议优化为批量获取 |
| 4 | 前端无构建流程 | 低 | 纯 HTML 单文件，修改后直接上传，无版本控制 |
| 5 | 服务器无 Git 仓库 | 低 | 代码变更无版本记录，建议初始化 Git |

---

## 十、联系方式

如有任何疑问，请联系：
- **李琦**: liqijob@sina.com

---

*本文档由擎析 Agent 自动生成，基于项目实际代码和部署状态整理。*
