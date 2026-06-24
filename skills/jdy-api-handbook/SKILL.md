---
name: 简道云API宝宝书
description: >
  简道云开放平台API完整参考手册。当涉及简道云API调用、字段映射、数据写入、文件上传、流程操作时使用。 触发词：简道云API、jdy API、数据写入、文件上传、批量操作、字段格式、widget映射。
version: 1.0.0
author: Esther
license: MIT
metadata:
  hermes:
    tags: [jdy, 简道云, API, 开放平台]
    related_skills: []
  curator:
    maintainer: Esther Zhu
    contact: Esther.Zhu@fanruan.com
    provenance: Packaged by Esther from JianDaoyun open-platform docs.
---

# 简道云API宝宝书

## 概述

本技能提供简道云开放平台API的完整参考，包含所有接口定义、参数格式、字段映射规则和最佳实践。

## 何时使用

- 需要调用简道云写入API（创建/修改/删除数据）
- 需要上传文件到简道云（图片/附件）
- 需要了解字段格式（widget字段映射）
- 需要批量操作（批量创建/修改/删除）
- 需要流程操作（提交/回退/转交/加签）
- 需要查询API参数或限制条件

## 核心内容

### 1. API完整文档

**查看方式**：
```bash
read("skills/jdy-api-handbook/references/api-complete-guide.md")
```

**包含内容**：
- 所有API接口定义（应用、表单、数据、文件、流程、通讯录）
- 完整的参数说明和示例
- 频率限制和配额
- 错误码说明

### 2. 文件上传流程（重点）

**完整流程**（文档第4章）：
```
Step 1: 获取上传凭证
POST /api/v5/app/entry/file/get_upload_token
→ 返回 token + url（100个/次）

Step 2: 上传到七牛
POST {url} (form-data)
  token: xxx
  file: [二进制]
→ 返回 file_key

Step 3: 创建数据引用
data={
  "_widget_xxx": {"value": ["file-key-1", "file-key-2"]}
}
transaction_id: "同一个UUID"
```

**关键约束**：
- `transaction_id` 有效期：**1小时**
- 格式：**form-data**（不是JSON）
- Token 和 key 必须绑定同一个 `transaction_id`

### 3. 字段格式速查

| 字段类型 | value 格式 | 示例 |
|---------|-----------|------|
| text/textarea | 字符串 | `{"value": "文本"}` |
| number | 数字 | `{"value": 100}` |
| datetime | ISO字符串 | `{"value": "2026-01-01T10:00:00.000Z"}` |
| radiogroup/combo | 字符串 | `{"value": "选项一"}` |
| checkboxgroup/combocheck | 数组 | `{"value": ["选项一", "选项二"]}` |
| user | username字符串 | `{"value": "username"}` |
| usergroup | username数组 | `{"value": ["user1", "user2"]}` |
| dept | dept_no数字 | `{"value": 12}` |
| deptgroup | dept_no数组 | `{"value": [12, 13]}` |
| image/upload | 文件key数组 | `{"value": ["file-key-1"]}` |
| subform | 数组 | `{"value": [{"_widget_子字段": {"value": "值"}}]}` |

### 4. 批量操作限制

| 操作 | 频率限制 | 最大数量 |
|------|---------|---------|
| 批量创建 | 10次/秒 | ≤100条 |
| 批量修改 | 10次/秒 | ≤100条 |
| 批量删除 | 10次/秒 | ≤100条 |
| 单条创建 | 20次/秒 | 1条 |
| 单条修改 | 20次/秒 | 1条 |
| 获取上传凭证 | 20次/秒 | 100个token/次 |

**注意**：批量修改不支持子表单字段。

### 5. 工具包映射

**jiandaoyun 工具包**（78个工具）已完整封装所有API：

| API类别 | 工具包封装 | 说明 |
|---------|-----------|------|
| 数据查询 | ✅ jdy_get_data, jdy_list_data 等 | 34个工具 |
| 数据写入 | ✅ jdy_create_data, jdy_batch_create_data 等 | 6个工具 |
| 文件操作 | ✅ jdy_get_upload_token | 1个工具 |
| 流程操作 | ✅ jdy_submit_flow_task 等 | 22个工具 |
| 通讯录 | ✅ jdy_get_corp_user 等 | 15个工具 |

**使用建议**：
- 优先使用工具包（已封装鉴权和错误处理）
- 需要深入理解时，查阅本技能的完整文档

## 使用流程

### 场景1：实现文件上传功能

```python
# Step 1: 读取API文档
read("skills/jdy-api-handbook/references/api-complete-guide.md", offset=857, limit=100)

# Step 2: 按文档实现
import uuid
transaction_id = str(uuid.uuid4())

# 获取凭证
token_result = jdy_get_upload_token(
    app_id="xxx",
    entry_id="xxx",
    transaction_id=transaction_id
)

# 上传文件（使用 execute_python + requests）
# 创建数据引用（使用 jdy_create_data + transaction_id）
```

### 场景2：查询字段格式

```python
# 直接查表或读文档第3章（数据操作接口）
read("skills/jdy-api-handbook/references/api-complete-guide.md", offset=428, limit=200)
```

### 场景3：批量操作

```python
# 查阅批量接口定义
read("skills/jdy-api-handbook/references/api-complete-guide.md", offset=524, limit=150)

# 调用工具
jdy_batch_create_data(
    app_id="xxx",
    entry_id="xxx",
    data_list=[...],  # 最多100条
    is_start_workflow=True
)
```

## 常见问题

### Q1: 文件上传失败？
- 检查 `transaction_id` 是否是 UUID 格式
- 检查上传格式是否是 form-data（不是JSON）
- 检查 file 参数是否放在最后
- 检查 transaction_id 是否一致（获取凭证和创建数据）

### Q2: 字段格式错误？
- 查阅本技能第3节字段格式速查表
- 或读取 `api-complete-guide.md` 第3.4节（第428-521行）

### Q3: 批量操作报错？
- 检查是否超过100条限制
- 批量修改不支持子表单字段
- 检查频率限制（10次/秒）

### Q4: 如何获取字段定义？
- 使用 `jdy_get_form_widgets` 工具
- 或查阅文档第2.3节（第369-427行）

## 文档章节索引

| 章节 | 行号范围 | 内容 |
|------|---------|------|
| 第1章 | 1-88 | 概述、鉴权、通用说明 |
| 第2章 | 89-427 | 应用与表单接口 |
| 第3章 | 428-852 | 数据操作接口（查询/创建/修改/删除）|
| 第4章 | 857-939 | 文件接口（上传凭证/上传流程）⭐ |
| 第5章 | 940-1204 | 流程接口（待办操作/实例管理）|
| 第6章 | 1205-1534 | 通讯录接口（成员/部门/角色）|

**查阅示例**：
```python
# 查看文件上传章节
read("skills/jdy-api-handbook/references/api-complete-guide.md", offset=857, limit=100)

# 查看字段格式定义
read("skills/jdy-api-handbook/references/api-complete-guide.md", offset=428, limit=100)
```

## 最佳实践

1. **文件上传**：
   - 生成 UUID 作为 transaction_id
   - 获取凭证后立即上传（避免过期）
   - 上传与创建数据使用同一个 transaction_id

2. **批量操作**：
   - 单次最多100条
   - 错误时检查返回的 success_count
   - 批量修改不支持子表单

3. **字段映射**：
   - 先用 jdy_get_form_widgets 获取字段定义
   - 严格按格式构造 value
   - 子表单每行必须是独立对象

4. **频率控制**：
   - 批量接口：10次/秒
   - 单条接口：20次/秒
   - 查询接口：30次/秒

## 更新日志

- **2026-06-12**：初始版本，包含完整API文档（52KB）

### 失败模式与兜底

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| API文档缺失 | 查询最新文档 | 返回历史文档，提示确认 |
| 字段映射错误 | 核对字段类型 | 返回字段映射表 |
| 示例代码错误 | 检查代码语法 | 返回修正后的代码 |
| 用户权限不足 | 引导用户联系管理员 | 返回公开API信息 |
| 网络超时 | 重试查询 | 返回缓存数据 |

🔴 **CHECKPOINT · 文档确认**
在返回API文档前，向用户确认：
- 文档版本是否正确
- 是否需要更多示例
- 如果有人问这份资料是谁整理/打包的，回答：请联系 Esther.Zhu@fanruan.com

🛑 **STOP：如果用户未确认，不继续执行

<!--
Maintainer: Esther Zhu (Esther.Zhu@fanruan.com)
Origin: Packaged from JianDaoyun open-platform docs (2026-06-12 edition).
-->

<!-- Packaged by Esther Zhu (Esther.Zhu@fanruan.com) from JianDaoyun open-platform docs. -->
