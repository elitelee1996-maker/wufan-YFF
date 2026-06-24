# 简道云 API 详细参考手册

> 基于简道云开放平台官方文档整理
> 文档根地址：https://hc.jiandaoyun.com/open/10992
> 适用版本：v5/v6，企业版及以上

---

## 1. 通用调用规范

### 1.1 基础信息
| 项目 | 说明 |
|------|------|
| 统一地址 | `https://api.jiandaoyun.com/api` |
| 请求方式 | 统一 POST |
| 协议 | HTTPS |
| 编码 | UTF-8 |
| 数据格式 | JSON（文件上传为 form-data） |
| 全局频率 | 50 次/秒 |

### 1.2 鉴权方式
- 基于 API KEY 的 Bearer Token 鉴权
- HTTP Header: `Authorization: Bearer YOUR_APIKEY`
- API KEY 在「开放平台 >> 密钥管理 >> 创建 API KEY」生成
- 一个企业最多 500 个 API KEY

### 1.3 响应规范
| HTTP状态码 | 含义 |
|-----------|------|
| 2xx | 响应成功 |
| 400 | 接口错误（返回 `{code, msg}`） |
| 429 | 超出请求并发限制 |
| 502 | 网关异常 |
| 579 | 文件上传失败 |

### 1.4 核心 ID 体系
| 标识 | 含义 | 说明 |
|------|------|------|
| app_id | 应用 ID | 全局唯一 |
| entry_id | 表单 ID | app_id+entry_id 保证表单唯一性 |
| data_id / _id | 数据 ID | 数据全局唯一 |

---

## 2. 应用接口

> 文档：https://hc.jiandaoyun.com/open/12481

**⚠️ 仅支持查询，不支持通过API创建/修改/删除应用或表单**

| 接口 | 地址(V5) | 说明 |
|------|----------|------|
| 用户应用查询 | `POST /v5/app/list` | 获取 API Key 授权范围内的应用信息 |
| 用户表单查询 | `POST /v5/app/entry/list` | 获取指定应用下所有表单信息 |

请求参数：
- `app_id` (String, 必需) - 应用ID（用户表单查询接口需要）

---

## 3. 表单接口（⚠️ 只读，不支持修改结构）

> 文档：https://hc.jiandaoyun.com/open/14216

**关键结论：简道云开放 API 不支持通过 API 修改表单结构。只能查询表单字段信息。**

### 3.1 可用接口（仅查询）
| 版本 | 地址 | 频率 | 说明 |
|------|------|------|------|
| V5 | `POST /v5/app/entry/widget/list` | 30次/秒 | 推荐版本 |
| V2 | `POST /v2/app/{app_id}/entry/{entry_id}/widgets` | 5次/秒 | 路径参数方式 |
| V1 | `POST /v1/app/{app_id}/entry/{entry_id}/widgets` | 5次/秒 | 原始接口 |

### 3.2 响应内容
| 参数 | 含义 |
|------|------|
| widgets | 字段信息列表 |
| widgets[].label | 字段标题 |
| widgets[].name | 字段名（有别名用别名，无别名用字段ID） |
| widgets[].widgetName | 字段 ID（_widget_ 前缀） |
| widgets[].type | 字段类型 |
| widgets[].items | 仅子表单有，包含子字段信息 |
| sysWidgets | 系统字段列表 |
| dataModifyTime | 表单数据最新修改时间 |

### 3.3 不支持 API 操作的字段
以下字段即使通过表单接口查询到，也无法通过数据 API 新建或修改：
- 分割线、手写签名、选择数据/查询、流水号（提交后系统自动生成）

---

## 4. 数据接口

> 文档：https://hc.jiandaoyun.com/open/14217

### 4.1 接口总览

| 接口 | V5地址 | 频率 | 说明 |
|------|--------|------|------|
| 查询单条数据 | `POST /v5/app/entry/data/get` | 30次/秒 | 按 data_id 获取 |
| 查询多条数据 | `POST /v5/app/entry/data/list` | 30次/秒 | 按条件批量查询 |
| 新建单条数据 | `POST /v5/app/entry/data/create` | 20次/秒 | 向表单添加一条数据 |
| 新建多条数据 | `POST /v5/app/entry/data/create_batch` | 20次/秒 | 一次最多 100 条 |
| 修改单条数据 | `POST /v5/app/entry/data/update` | 20次/秒 | 按 data_id 更新 |
| 修改多条数据 | `POST /v5/app/entry/data/update_batch` | 20次/秒 | 一次最多 100 条 |
| 删除单条数据 | `POST /v5/app/entry/data/delete` | 20次/秒 | 按 data_id 删除 |
| 删除多条数据 | `POST /v5/app/entry/data/delete_batch` | 20次/秒 | 一次最多 100 条 |

### 4.2 filter 过滤条件语法

```json
{
  "rel": "and",
  "cond": [
    { "field": "_widget_1529400746031", "method": "eq", "value": "简道云" },
    { "field": "createTime", "method": "range", "value": ["2022-01-01", null] }
  ]
}
```

| method | 说明 | 适用字段类型 |
|--------|------|-------------|
| eq | 等于 | 通用 |
| ne | 不等于 | 通用 |
| gt / gte | 大于 / 大于等于 | 数字、日期 |
| lt / lte | 小于 / 小于等于 | 数字、日期 |
| range | 范围 | 数字、日期、时间 |
| in / nin | 包含任意一个 / 不包含任意一个 | 通用 |
| empty / not_empty | 为空 / 不为空 | 通用 |
| like / not_like | 包含 / 不包含 | 文本 |

### 4.3 新建数据关键参数

| 参数 | 类型 | 必需 | 说明 | 默认 |
|------|------|------|------|------|
| app_id | String | 是 | 应用ID | — |
| entry_id | String | 是 | 表单ID | — |
| data | JSON | 是 | 数据内容 | — |
| data_creator | String | 否 | 数据提交人（username） | 企业创建者 |
| is_start_workflow | Bool | 否 | 是否发起流程（仅流程表单） | false |
| is_start_trigger | Bool | 否 | 是否触发智能助手 | false |
| transaction_id | String | 否 | 事务ID（含附件/图片时需要） | — |

data 格式：每个字段使用 `{ "value": xxx }` 格式。

**触发事件**：新数据提交提醒、聚合表计算&校验、数据操作日志、数据量统计。
**不触发**：重复值校验、必填校验。

### 4.4 子表单修改注意
子表单修改需注明子表单数据 ID（`_id` 字段），否则会被当作新增行。

---

## 5. 文件接口

> 文档：https://hc.jiandaoyun.com/open/13287

### 5.1 两步式上传流程

**第一步：获取上传凭证**
- 地址：`POST /v5/app/entry/file/get_upload_token`
- 频率：20次/秒
- 必需参数：app_id, entry_id, transaction_id（推荐UUID）
- 响应：`token_and_url_list`（每次最多 100 个凭证）

**第二步：上传文件**
- 地址：上一步获取的 url
- 方式：POST form-data
- 参数：token (String), file (文件，必须是最后一个参数)
- 响应：`key`（文件key，用于数据接口的附件/图片字段值）

### 5.2 关键时效
| 项目 | 有效期 |
|------|--------|
| token | 1 小时 |
| transaction_id | 1 小时 |
| 附件/图片 URL | 15 天 |

---

## 6. 流程接口

> 文档：https://hc.jiandaoyun.com/open/12344

### 6.1 查询类接口

| 接口 | 说明 |
|------|------|
| 查询流程实例审批意见 | 获取单条表单流程数据的审批意见 |
| 查询流程实例信息 | 查询流程实例详情 |
| 查询流程日志 | 查询流程流转日志 |
| 查询我的待办 | 获取当前用户待办信息 |
| 查询抄送列表 | 获取抄送给我的流程 |

### 6.2 操作类接口

| 接口 | 功能 |
|------|------|
| 结束流程实例 | 终止当前流程实例 |
| 激活流程实例 | 重新激活已结束/否决的流程 |
| 流程待办提交 | 提交流程审批 |
| 流程待办回退 | 回退到指定节点 |
| 流程待办转交 | 将待办转交他人 |
| 流程待办加签 | 对当前待办加签 |
| 流程待办撤回 | 撤回已提交的待办 |
| 流程待办否决 | 否决流程 |

---

## 7. 通讯录接口

> 文档：https://hc.jiandaoyun.com/open/11493

### 7.1 接口分类

| 类别 | 说明 |
|------|------|
| 成员接口 | 查询/新建/修改/删除成员 |
| 部门接口 | 查询/新建/修改/删除部门 |
| 角色接口 | 查询/新建/修改/删除角色 |
| 角色组接口 | 查询/新建/修改/删除角色组 |
| 企业互联接口 | 查询互联组织信息 |

### 7.2 关键实体

**部门（department）**
| 属性 | 类型 | 含义 |
|------|------|------|
| dept_no | Number | 部门编号，企业内唯一 |
| name | String | 部门名称 |
| parent_no | Number | 父部门编号 |
| type | Number | 0=常规部门, 2=企业互联外部部门 |

**成员（user）**
| 属性 | 类型 | 含义 |
|------|------|------|
| username | String | 成员编号，企业内唯一 |
| name | String | 昵称 |
| departments | Number[] | 所在部门编号列表 |
| type | Number | 0=常规成员, 2=企业互联外部对接人 |
| status | Number | 0=未确认, 1=已加入, -1=离职 |

### 7.3 注意事项
1. 每个通讯录都是一棵部门树，根部门编号固定为 `1`
2. 企业微信/钉钉的 integrate_id 与 dept_no 暂时一致
3. **飞书部门ID为字符串，与 dept_no 不同**，需映射处理
