# 简道云开放平台 API 文档完整汇总

> 来源：https://hc.jiandaoyun.com/open/11470
> 抓取时间：2026-06-12

---

## 目录

1. [开发指南](#1-开发指南)
2. [应用接口](#2-应用接口)
3. [表单和数据接口](#3-表单和数据接口)
   - 3.1 [表单接口](#31-表单接口)
   - 3.2 [查询单条数据接口](#32-查询单条数据接口)
   - 3.3 [查询多条数据接口](#33-查询多条数据接口)
   - 3.4 [新建单条数据接口](#34-新建单条数据接口)
   - 3.5 [新建多条数据接口](#35-新建多条数据接口)
   - 3.6 [修改单条数据接口](#36-修改单条数据接口)
   - 3.7 [修改多条数据接口](#37-修改多条数据接口)
   - 3.8 [删除单条数据接口](#38-删除单条数据接口)
   - 3.9 [删除多条数据接口](#39-删除多条数据接口)
4. [文件接口](#4-文件接口)
5. [流程接口](#5-流程接口)
6. [通讯录接口](#6-通讯录接口)
7. [字段与数据类型映射表](#7-字段与数据类型映射表)
8. [API操作关联关系表](#8-api操作关联关系表)
9. [错误对照表](#9-错误对照表)

---

## 1. 开发指南

### 1.1 接口分类

- 应用接口
- 表单和数据接口
- 文件接口
- 流程接口
- 通讯录接口

### 1.2 规则

- 统一 API 访问地址：`https://api.jiandaoyun.com/api`（不可直接访问，需结合 appid 等）
- 所有 API 请求必须使用 HTTPS，需认证
- 所有请求使用 POST 方法
- 数据编码：UTF-8
- 文件上传接口使用 `form_data` 格式，其他均使用 JSON 格式

### 1.3 频率限制

- **全局最大：50 请求/秒**
- 各接口独立频率限制见各接口说明

### 1.4 鉴权方式

使用简单 Token 认证，API KEY 需手动创建。

创建路径：开放平台 >> 密钥管理 >> 创建 API KEY

最大数量：每企业 **500 个 API KEY**

通过 HTTP Headers 设置认证：

```
Authorization: Bearer YOUR_APIKEY
```

示例：

```bash
curl -i https://jiandaoyun.com/api/v1/callback \
  -H "Authorization: Bearer YOUR_APIKEY"
```

### 1.5 代码示例

GitHub 仓库：
- Python: https://github.com/jiandaoyun/api-demo/tree/master/python
- C#: https://github.com/jiandaoyun/api-demo/tree/master/csharp
- Go: https://github.com/jiandaoyun/api-demo/tree/master/go
- Java: https://github.com/jiandaoyun/api-demo/tree/master/java
- Node: https://github.com/jiandaoyun/api-demo/tree/master/node

---

## 2. 应用接口

| 接口名称 | 释义 |
|---|---|
| [用户应用查询接口](https://hc.jiandaoyun.com/open/18538) | 仅获取 API Key 应用授权范围内的应用信息 |
| [用户表单查询接口](https://hc.jiandaoyun.com/open/18539) | 获取当前应用下的所有表单信息 |

---

## 3. 表单和数据接口

所有 API 路径包含 `app_id` 和 `entry_id`，分别代表应用 ID 和表单 ID。`app_id + entry_id` 代表全局唯一的表单 ID。

### 字段名规则

表单字段添加后，以固定字段 ID（`_widget_` 前缀）表示，修改字段信息不会改变字段 ID。

每个字段还有对应的**字段别名**：
- 若设置了别名，则所有 API 中该字段名使用别名
- 若未设置别名，则使用字段 ID 作为实际字段名

字段别名设置路径：扩展功能 >> 数据推送 >> 设置字段别名

---

### 3.1 表单接口

获取指定表单的字段/字段信息，不包含分割线字段和查询字段。

#### 版本历史

| 接口版本 | 更新时间 | 版本说明 |
|---|---|---|
| v1 | 2021.6.1 | 原始接口 |
| v2 | 2021.10.26 | 在 V1 基础上新增系统字段及表单数据修改时间的获取 |
| v5 | 2022.10.28 | 在 v1 基础上请求频率由 5次/秒提升至 30次/秒；参数 app_id 和 entry_id 放入 body，路由修改为 POST app/entry/widget/list |

#### V5 接口

- **请求地址**: `https://api.jiandaoyun.com/api/v5/app/entry/widget/list`
- **请求频率**: 30 次/秒
- **请求方式**: POST

**请求参数：**

| 参数 | 类型 | 必需 | 说明 |
|---|---|---|---|
| app_id | String | 是 | 应用ID |
| entry_id | String | 是 | 表单ID |

**请求示例：**

```json
{
    "app_id": "59264073a2a60c0c08e20bfb",
    "entry_id": "59264073a2a60c0c08e20bfd"
}
```

**响应参数：**

| 参数 | 含义 |
|---|---|
| widgets | 字段信息 |
| widgets[].label | 字段标题 |
| widgets[].name | 字段名称（若设置别名则使用别名，否则使用字段 ID） |
| widgets[].widgetName | 字段 ID |
| widgets[].type | 字段类型，每种字段类型对应一种数据类型 |
| widgets[].items | 仅子表单控件存在，数组包含每个子字段的信息 |
| sysWidgets | 系统字段列表 |
| sysWidgets[].name | 系统字段名称 |
| dataModifyTime | 表单内最新数据修改时间（可用于判断表单内数据是否发生变化） |

**响应示例：**

```json
{
    "widgets": [
        {"name": "_widget_1529400746031", "widgetName": "_widget_1529400746031", "label": "单行文本", "type": "text"},
        {"name": "_widget_1529400746045", "widgetName": "_widget_1529400746045", "label": "多行文本", "type": "textarea"},
        {"name": "_widget_1529400746056", "widgetName": "_widget_1529400746056", "label": "数字", "type": "number"},
        {"name": "_widget_1529400746068", "widgetName": "_widget_1529400746068", "label": "日期", "type": "datetime"},
        {"name": "_widget_1529400746079", "widgetName": "_widget_1529400746079", "label": "日期时间", "type": "datetime"},
        {"name": "_widget_1529400746090", "widgetName": "_widget_1529400746090", "label": "单选按钮组", "type": "radiogroup"},
        {"name": "_widget_1529400746105", "widgetName": "_widget_1529400746105", "label": "复选框组", "type": "checkboxgroup"},
        {"name": "_widget_1529400746119", "widgetName": "_widget_1529400746119", "label": "下拉框", "type": "combo"},
        {"name": "_widget_1529400746136", "widgetName": "_widget_1529400746136", "label": "下拉复选框", "type": "combocheck"},
        {"name": "_widget_1529400746157", "widgetName": "_widget_1529400746157", "label": "地址", "type": "address"},
        {"name": "_widget_1529400746173", "widgetName": "_widget_1529400746173", "label": "定位", "type": "location"},
        {"name": "_widget_1529400746191", "widgetName": "_widget_1529400746191", "label": "图片", "type": "image"},
        {"name": "_widget_1529400746209", "widgetName": "_widget_1529400746209", "label": "附件", "type": "upload"},
        {"name": "_widget_1529400746221", "widgetName": "_widget_1529400746221", "label": "子表单", "type": "subform", "items": []},
        {"name": "_widget_1529400746242", "widgetName": "_widget_1529400746242", "label": "选择数据", "type": "linkdata"},
        {"name": "_widget_1529400746242", "widgetName": "_widget_1529400746242", "label": "关联数据", "type": "lookup"},
        {"name": "_widget_1529400746254", "widgetName": "_widget_1529400746254", "label": "手写签名", "type": "signature"},
        {"name": "_widget_1529400746696", "widgetName": "_widget_1529400746696", "label": "成员单选", "type": "user"},
        {"name": "_widget_1529400746713", "widgetName": "_widget_1529400746713", "label": "成员多选", "type": "usergroup"},
        {"name": "_widget_1529400746729", "widgetName": "_widget_1529400746729", "label": "部门单选", "type": "dept"},
        {"name": "_widget_1529400746746", "widgetName": "_widget_1529400746746", "label": "部门多选", "type": "deptgroup"}
    ],
    "sysWidgets": [
        {"name": "flowState"},
        {"name": "wx_open_id"},
        {"name": "wx_nickname"},
        {"name": "wx_gender"},
        {"name": "creator"},
        {"name": "updater"},
        {"name": "deleter"},
        {"name": "ext"},
        {"name": "createTime"},
        {"name": "updateTime"},
        {"name": "deleteTime"}
    ],
    "dataModifyTime": "2021-09-08T03:40:26.586Z"
}
```

#### 版本对比

| 特性 | V1 | V2 | V5 |
|---|---|---|---|
| 系统字段 (sysWidgets) | ❌ 不返回 | ✅ 返回 | ✅ 返回 |
| dataModifyTime | ❌ 不返回 | ✅ 返回 | ✅ 返回 |
| 请求频率 | 5次/秒 | 5次/秒 | 30次/秒 |
| 参数位置 | URL路径 | URL路径 | 请求体(POST) |
| URL模式 | `/api/v1/app/{app_id}/entry/{entry_id}/widgets` | `/api/v2/app/{app_id}/entry/{entry_id}/widgets` | `/api/v5/app/entry/widget/list` |

---

### 3.2 查询单条数据接口

#### 版本历史

| 接口版本 | 更新时间 | 版本说明 |
|---|---|---|
| v1 | 2018.6.21 | 原始接口 |
| v2 | 2021.3.11 | 子表单新增数据 ID 参数 |
| v4 | 2022.4.21 | 新增互联组织部门/成员获取，新增 type 参数 |
| v5 | 2022.10.28 | 请求频率提升至 30次/秒；参数放入 body |

#### 接口调用

- **请求地址**: `https://api.jiandaoyun.com/api/v5/app/entry/data/get`
- **请求频率**: 30 次/秒
- **请求方式**: POST

**请求参数：**

| 参数 | 类型 | 必需 | 说明 |
|---|---|---|---|
| app_id | String | 是 | 应用ID |
| entry_id | String | 是 | 表单ID |
| data_id | String | 是 | 数据 ID |

**请求示例：**

```json
{
   "app_id": "59264073a2a60c0c08e20bfb",
   "entry_id": "59264073a2a60c0c08e20bfd",
   "data_id": "59e9a2fe283ffa7c11b1ddbf"
}
```

**响应参数：**

| 参数 | 类型 | 说明 |
|---|---|---|
| data | JSON | 单条数据 |

**响应示例：**

```json
{
    "data": {
        "_id": "59e9a2fe283ffa7c11b1ddbf",
        "appId": "59264073a2a60c0c08e20bfb",
        "entryId": "59264073a2a60c0c08e20bfd",
        "creator": {
            "name": "小简", "username": "xiaojian", "status": 1,
            "type": 0, "departments": [1, 3], "integrate_id": "xiaojian"
        },
        "updater": {
            "name": "小简", "username": "xiaojian", "status": 1,
            "type": 0, "departments": [1, 3], "integrate_id": "xiaojian"
        },
        "createTime": "2017-10-20T22:41:51.430Z",
        "updateTime": "2017-10-20T11:12:15.293Z",
        "_widget_1432728651402": "简道云",
        "_widget_1432728651403": 100,
        "_widget_1432728651404": "简道云是一个强大易用的应用搭建工具，可以快速把你的想法变成应用",
        "_widget_1432728651405": "选项一",
        "_widget_1432728651406": ["选项一", "选项二", "选项三"],
        "_widget_1432728651407": "2018-01-01T10:10:10.000Z",
        "_widget_1432728651408": {"id": "5b28effa49b561455dfda91e"},
        "_widget_1432728651409": [
            {"name": "image.jpg", "size": 262144, "mime": "image/jpeg", "url": "https://files.jiandaoyun.com/..."}
        ],
        "_widget_1432728651410": [
            {"name": "产品说明文档.pdf", "size": 524288, "mime": "application/pdf", "url": "https://files.jiandaoyun.com/..."}
        ],
        "_widget_1432728651411": {
            "name": "image.png", "size": 262144, "mime": "image/png",
            "url": "https://files.jiandaoyun.com/..."
        },
        "_widget_1432728651412": {
            "province": "江苏省", "city": "无锡市", "district": "梁溪区",
            "detail": "清扬路138号茂业天地"
        },
        "_widget_1432728651413": {
            "province": "江苏省", "city": "无锡市", "district": "梁溪区",
            "detail": "清扬路138号茂业天地",
            "lnglatXY": [120.31237, 31.49099]
        },
        "_widget_1652345009097": {"verified": false, "phone": "15852540044"},
        "_widget_1432728651414": {
            "name": "小简", "username": "xiaojian", "status": 1,
            "type": 0, "departments": [1, 3], "integrate_id": "xiaojian"
        },
        "_widget_1432728651415": [
            {"name": "小简", "username": "xiaojian", "status": 1,
             "type": 0, "departments": [1, 3], "integrate_id": "xiaojian"}
        ],
        "_widget_1432728651416": {
            "name": "经理部", "dept_no": 1, "type": 0,
            "parent_no": 2, "status": 1, "integrate_id": 1
        },
        "_widget_1432728651417": [
            {"name": "经理部", "dept_no": 1, "type": 0,
             "parent_no": 2, "status": 1, "integrate_id": 1}
        ],
        "_widget_1432728651528": {
            "html": "<p>Hello, world!<img src=\"https://files.xxxxxx.com/xxx\" /></p>",
            "attachments": [
                {"name": "image1.png", "size": 262144, "mime": "image/png",
                 "url": "https://files.xxxxx.com/xxx"}
            ]
        },
        "wx_open_id": "wx98fb14481b3ab5a3",
        "wx_nickname": "jiandaoyun",
        "wx_gender": "男"
    }
}
```

---

### 3.3 查询多条数据接口

#### 版本历史

| 接口版本 | 更新时间 | 版本说明 |
|---|---|---|
| v1 | 2018.6.21 | 原始接口 |
| v2 | 2021.3.11 | 子表单新增数据 ID 参数 |
| v4 | 2022.4.21 | 新增互联组织部门/成员获取，新增 type 参数 |
| v5 | 2022.10.28 | 请求频率提升至 30次/秒；参数放入 body |

#### 接口调用

返回数据始终按照数据 ID 正序排列。

- **请求地址**: `https://api.jiandaoyun.com/api/v5/app/entry/data/list`
- **请求频率**: 30 次/秒
- **请求方式**: POST

**请求参数：**

| 参数 | 类型 | 必需 | 说明 |
|---|---|---|---|
| app_id | String | 是 | 应用ID |
| entry_id | String | 是 | 表单ID |
| data_id | String | 否 | 分页符，上一次查询数据结果的最后一条数据的 ID，没有则留空 |
| fields | Array | 否 | 需要查询的数据字段 |
| filter | JSON | 否 | 数据筛选器 |
| limit | Number | 否 | 查询的数据条数，1~100，默认10 |

#### 数据筛选器 (filter)

| 参数 | 必需 | 类型 | 说明 |
|---|---|---|---|
| rel | 是 | String | "and" = 满足所有条件；"or" = 满足任一条件 |
| cond | 是 | [JSON] | 过滤条件列表 |

**过滤条件结构：**

| 参数 | 必需 | 类型 | 说明 |
|---|---|---|---|
| field | 是 | String | 字段名 |
| type | 否 | String | 字段类型 |
| method | 是 | String | 过滤方法 |
| value | 否 | Array | 过滤值 |

**method 可选值：**

| method | 说明 |
|---|---|
| `not_empty` | 不为空 |
| `empty` | 为空 |
| `eq` | 等于 |
| `ne` | 不等于 |
| `in` | 等于任意一个，最多1000个 |
| `range` | 在 x 与 y 之间，包含 x 和 y |
| `nin` | 不等于任意一个，最多1000个 |
| `like` | 包含 |
| `verified` | 填写了手机号且已验证 |
| `unverified` | 填写了手机号但未验证 |
| `all` | 同时包含，最多1000个 |
| `gt` | 大于 |
| `lt` | 小于 |

#### 支持的字段类型及过滤方式

| 字段类型 | 支持的过滤方式 | 说明 |
|---|---|---|
| flowState | eq, ne, in, nin, empty, not_empty | 流程状态，仅对流程表单有效 |
| data_id | eq, in, empty, not_empty | 数据 id 字段 |
| 提交人 | eq, ne, in, nin, empty, not_empty | — |
| 日期时间 | eq, ne, range, empty, not_empty | 包含日期时间字段和提交时间字段 |
| 数字 | eq, ne, range, empty, not_empty, gt, lt | — |
| 文本 | eq, ne, in, nin, empty, not_empty | 包括单行文本、下拉框、单选按钮组 |
| 复选框组/下拉复选框 | in, all, empty, not_empty | — |
| 手机 | like, verified, unverified, empty, not_empty | — |
| 成员单选/部门单选 | eq, ne, in, nin, empty, not_empty | — |
| 成员多选/部门多选 | in, all, empty, not_empty | — |
| 流水号 | eq, ne, in, nin, like, empty, not_empty | — |
| 关联数据 | eq, ne, in, nin, empty, not_empty | — |
| 其他表单字段(子表单字段除外) | empty, not_empty | — |

#### 分页查询说明

使用 `data_id` 字段进行分页，避免重复获取数据。

以 limit=100 查询 230 条数据为例：
1. 第一次查询：不传 data_id，返回前 100 条
2. 第二次查询：传入第 100 条数据的 `_id` 作为 data_id，返回第 101~200 条
3. 第三次查询：传入第 200 条数据的 `_id` 作为 data_id，返回第 201~230 条

当返回数据条数小于 limit 时，表示所有数据已获取完毕。

---

### 3.4 新建单条数据接口

#### 版本历史

| 版本 | 更新时间 | 说明 |
|------|----------|------|
| v1 | 2018.6.21 | 部门和成员字段使用 `_id` 为主键 |
| v2 | 2019.6.21 | 成员字段使用 `username`，部门字段使用 `dept_no` |
| v3 | 2021.3.31 | 子表单新增数据 ID 参数 |
| v4 | 2022.4.21 | 新增互联组织，新增 type 参数 |
| v5 | 2022.10.28 | 请求频率提升至 20次/秒；参数放入 body |
| — | 2023.08.31 | 新增请求参数 data_creator |

#### 接口调用

- **请求地址**: `https://api.jiandaoyun.com/api/v5/app/entry/data/create`
- **请求频率**: 20 次/秒
- **请求方式**: POST

**请求参数：**

| 参数 | 类型 | 必需 | 说明 | 默认 |
|---|---|---|---|---|
| app_id | String | 是 | 应用ID | — |
| entry_id | String | 是 | 表单ID | — |
| data | JSON | 是 | 数据内容 | — |
| data_creator | String | 否 | 数据提交人（取成员编号 username） | 企业创建者 |
| is_start_workflow | Bool | 否 | 是否发起流程（仅流程表单有效） | false |
| is_start_trigger | Bool | 否 | 是否触发智能助手 | false |
| transaction_id | String | 否 | 事务ID，绑定一批上传文件 | — |

**请求示例：**

```json
{
    "app_id": "59264073a2a60c0c08e20bfb",
    "entry_id": "59264073a2a60c0c08e20bfd",
    "transaction_id": "87cd7d71-c6df-4281-9927-469094395677",
    "data_creator": "Yonne",
    "data": {
        "_widget_1432728651402": {"value": "简道云"},
        "_widget_1725969783950": {"value": "67221b4fac0a62ac8f43a1c3"},
        "_widget_1432728651403": {"value": 100},
        "_widget_1432728651404": {"value": "简道云是一个强大易用的应用搭建工具"},
        "_widget_1432728651405": {"value": "选项一"},
        "_widget_1432728651406": {"value": ["选项一", "选项二", "选项三"]},
        "_widget_1432728651407": {"value": "2018-01-01T10:10:10.000Z"},
        "_widget_1432728651412": {"value": {"province": "江苏省", "city": "无锡市", "district": "梁溪区", "detail": "清扬路138号茂业天地"}},
        "_widget_1432728651413": {"value": {"province": "江苏省", "city": "无锡市", "district": "梁溪区", "detail": "清扬路138号茂业天地", "lnglatXY": [120.31237, 31.49099]}},
        "_widget_1528854613291": {"value": [
            {"_widget_1528854614409": {"value": "子表单数据1"}, "_widget_1528854615499": {"value": 1001}},
            {"_widget_1528854614410": {"value": "子表单数据2"}, "_widget_1528854615419": {"value": 1002}}
        ]},
        "_widget_1652345009097": {"value": {"phone": "15852540044"}},
        "_widget_1652345009126": {"value": "jian"},
        "_widget_1652345009143": {"value": ["jian", "dao"]},
        "_widget_1652345009157": {"value": 12},
        "_widget_1652345009174": {"value": [12, 13]},
        "_widget_1432728651408": {"value": ["6b559cf1-b16c-43bd-a211-8fa8fdeae2ef", "6b559cf1-b16c-43bd-a211-646ab85da8cb"]},
        "_widget_1432728652567": {"value": ["6b559cf1-b16c-43bd-a211-74389cd8ae76", "6b559cf1-b16c-43bd-a211-564e56a65bd6"]},
        "_widget_1432728651528": {"value": "<p>Hello, world!<img data-key=\"6b559cf1-b16c-43bd-a211-74389cd8ae76\" width=\"100\" height=\"100\" /></p>"}
    },
    "is_start_workflow": true
}
```

**各字段类型写入格式：**

| 字段类型 | 写入格式 | 说明 |
|---|---|---|
| 单行文本 | `{"value": "string"}` | — |
| 关联数据 | `{"value": "data_id_string"}` | 关联数据ID |
| 数字 | `{"value": 100}` | 数值 |
| 多行文本 | `{"value": "string"}` | 支持 `\n` 换行 |
| 单选按钮组/下拉框 | `{"value": "选项一"}` | 单个选项值 |
| 复选框组/下拉复选框 | `{"value": ["选项一","选项二"]}` | 数组 |
| 日期时间 | `{"value": "2018-01-01T10:10:10.000Z"}` | ISO 8601 |
| 地址 | `{"value": {"province":"...","city":"...","district":"...","detail":"..."}}` | — |
| 定位 | `{"value": {"province":"...","city":"...","district":"...","detail":"...","lnglatXY":[lng,lat]}}` | — |
| 子表单 | `{"value": [{...}, {...}]}` | 数组 |
| 手机 | `{"value": {"phone": "15852540044"}}` | — |
| 成员单选 | `{"value": "username"}` | — |
| 成员多选 | `{"value": ["username1", "username2"]}` | — |
| 部门单选 | `{"value": dept_no_int}` | — |
| 部门多选 | `{"value": [dept_no1, dept_no2]}` | — |
| 附件/图片 | `{"value": ["file_key1", "file_key2"]}` | — |
| 富文本 | `{"value": "<p>HTML<img data-key=\"file_key\" /></p>"}` | — |

**响应参数：**

| 参数 | 类型 | 说明 |
|---|---|---|
| data | JSON | 返回提交后的完整数据，内容同查询单条数据接口 |

---

### 3.5 新建多条数据接口

#### 版本历史

| 接口版本 | 更新时间 | 版本说明 |
|---|---|---|
| v1 | 2021.12.30 | 原始接口 |
| v5 | 2022.10.28 | 请求频率提升至 10次/秒；参数放入 body |
| v5 | 2023.08.31 | 新增请求参数 data_creator |

#### 接口调用

每次最多创建 **100** 条数据。

- **请求地址**: `https://api.jiandaoyun.com/api/v5/app/entry/data/batch_create`
- **请求频率**: 10 次/秒
- **请求方式**: POST

**请求参数：**

| 参数 | 类型 | 必需 | 说明 | 默认 |
|---|---|---|---|---|
| app_id | String | 是 | 应用ID | — |
| entry_id | String | 是 | 表单ID | — |
| data_list | Array | 是 | 数据内容数组 | — |
| data_creator | String | 否 | 数据提交人（取成员编号 username） | 企业创建者 |
| transaction_id | String | 否 | 事务ID | — |
| is_start_workflow | Bool | 否 | 是否发起流程（仅流程表单有效） | false |

**请求示例：**

```json
{
  "app_id": "59264073a2a60c0c08e20bfb",
  "entry_id": "59264073a2a60c0c08e20bfd",
  "transaction_id": "87cd7d71-c6df-4281-9927-469094395677",
  "data_list": [
    {
      "_widget_1432728651402": {"value": "简道云1"},
      "_widget_1432728651403": {"value": 100},
      "_widget_1725969783950": {"value": "67221b4fac0a62ac8f43a1c4"},
      "_widget_1528854613291": {"value": [
        {"_widget_1528854614409": {"value": "子表单数据11"}, "_widget_1528854615499": {"value": 1001}},
        {"_widget_1528854614410": {"value": "子表单数据12"}, "_widget_1528854615419": {"value": 1002}}
      ]}
    },
    {
      "_widget_1432728651402": {"value": "简道云2"},
      "_widget_1432728651403": {"value": 200}
    },
    {
      "_widget_1432728651402": {"value": "简道云3"},
      "_widget_1432728651403": {"value": 300}
    }
  ],
  "is_start_workflow": true
}
```

**响应参数：**

| 参数 | 类型 | 说明 |
|---|---|---|
| status | String | 返回请求结果 |
| success_count | Number | 该 transaction_id 创建成功的数据条数 |
| success_ids | Array | 本次请求创建成功的数据 ID 列表 |

**响应示例：**

```json
{
  "status": "success",
  "success_count": 3,
  "success_ids": [
    "200001181fe09728936510eb",
    "200001181fe09728936510ec",
    "200001181fe09728936510ed"
  ]
}
```

**注意事项：**

1. 批量创建部分失败时，使用相同的 `transaction_id` 重新请求所有数据。第二次执行的数据会完全覆盖第一次执行的数据。
2. `transaction_id` 有效期为 **1 小时**。
3. 若指定了 `data_creator`，关联触发成员也会记录为该 `data_creator`。

---

### 3.6 修改单条数据接口

#### 版本历史

| 版本 | 更新时间 | 说明 |
|------|----------|------|
| v1 | 2018.6.21 | 部门和成员均使用 _id 为主键 |
| v2 | 2019.6.21 | 成员字段使用 username，部门字段使用 dept_no |
| v3 | 2021.3.31 | 子表单新增数据 ID 参数 |
| v4 | 2022.4.21 | 新增互联组织，新增 type 参数 |
| v5 | 2022.10.28 | 请求频率提升至 20次/秒；参数放入 body |

#### 接口调用

- **请求地址**: `https://api.jiandaoyun.com/api/v5/app/entry/data/update`
- **请求频率**: 20 次/秒
- **请求方式**: POST

**请求参数：**

| 参数 | 类型 | 必需 | 说明 | 默认 |
|---|---|---|---|---|
| app_id | String | 是 | 应用ID | — |
| entry_id | String | 是 | 表单ID | — |
| data_id | String | 是 | 数据ID | — |
| data | JSON | 是 | 数据内容，同新建单条数据接口；子表单需注明子表单数据ID | — |
| is_start_trigger | Bool | 否 | 是否触发智能助手 | false |
| transaction_id | String | 否 | 事务ID | — |

**请求示例：**

```json
{
   "app_id": "604eb6eea71d720006e1336e",
   "entry_id": "604ecfca8e2ade077c72453a",
   "transaction_id": "87cd7d71-c6df-4281-9927-469094395677",
   "data_id": "6052e8072315c0075001d65e",
   "data": {
       "_widget_1615777739654": {"value": "张三"},
       "_widget_1725969783950": {"value": "67221b4fac0a62ac8f43a1c3"},
       "_widget_1615777739673": {
           "value": [
               {"_widget_1615777739744": {"value": "张三"}},
               {"_id": {"value": "606290aba392ca00076da000"}, "_widget_1615777739744": {"value": "李四"}},
               {"_id": {"value": "606290aba392ca00076da0a9"}, "_widget_1615777739744": {"value": "王五"}}
           ]
       }
   },
   "is_start_trigger": true
}
```

**响应参数：**

| 参数 | 类型 | 说明 |
|---|---|---|
| data | JSON | 返回修改后的新数据，内容同查询单条数据接口 |

#### 子表单数据ID处理规则（v3/v4/v5）

1. 每次调用会清空原子表单数据，替换为新的请求数据
2. 缺失或错误的子表单数据 ID 会重新生成
3. 即使内容不变，也会记录"子表单变更"日志
4. 正确传入的子表单数据 ID 保持不变

**重要：子表单和子字段必须整体修改。** 如果原子表单有3行但只传了2行，结果只有2行。

---

### 3.7 修改多条数据接口

#### 版本历史

| 版本 | 更新时间 | 说明 |
|------|----------|------|
| v1 | 2021.12.30 | 原始接口 |
| v5 | 2022.10.28 | 请求频率提升至 10次/秒；参数放入 body |

#### 接口调用

- **请求地址**: `https://api.jiandaoyun.com/api/v5/app/entry/data/batch_update`
- **请求频率**: 10 次/秒
- **请求方式**: POST

**限制：**
- 子表单字段不支持
- 每次最多修改 **100** 条数据
- 附件和图片字段更新时会**清空原有文件**

**请求参数：**

| 参数 | 类型 | 必需 | 说明 |
|---|---|---|---|
| app_id | String | 是 | 应用ID |
| entry_id | String | 是 | 表单ID |
| data_ids | Array | 是 | 要修改的数据 ID 数组 |
| data | JSON | 是 | 数据内容；子表单字段不支持 |
| transaction_id | String | 否 | 事务ID |

**请求示例：**

```json
{
  "app_id": "59264073a2a60c0c08e20bfb",
  "entry_id": "59264073a2a60c0c08e20bfd",
  "transaction_id": "87cd7d71-c6df-4281-9927-469094395677",
  "data_ids": [
    "200001181fe09728936510eb",
    "200001181fe09728936510ec",
    "200001181fe09728936510ed"
  ],
  "data": {
    "_widget_1432728651402": {"value": "简道云1"},
    "_widget_1432728651403": {"value": 100},
    "_widget_1725969783950": {"value": "67221b4fac0a62ac8f43a1c4"}
  }
}
```

**响应参数：**

| 参数 | 类型 | 说明 |
|---|---|---|
| status | String | 请求结果状态 |
| success_count | Number | 成功修改的数据条数 |

**响应示例：**

```json
{
  "status": "success",
  "success_count": 3
}
```

---

### 3.8 删除单条数据接口

#### 版本历史

| 版本 | 更新时间 | 说明 |
|------|----------|------|
| v1 | 2018.6.21 | 原始接口 |
| v5 | 2022.10.28 | 请求频率提升至 20次/秒；参数放入 body |

#### 接口调用

- **请求地址**: `https://api.jiandaoyun.com/api/v5/app/entry/data/delete`
- **请求频率**: 20 次/秒
- **请求方式**: POST

**请求参数：**

| 参数 | 类型 | 必需 | 说明 | 默认 |
|---|---|---|---|---|
| app_id | String | 是 | 应用ID | — |
| entry_id | String | 是 | 表单ID | — |
| data_id | String | 是 | 数据ID | — |
| is_start_trigger | Bool | 否 | 是否触发智能助手 | false |

**请求示例：**

```json
{
    "app_id": "59264073a2a60c0c08e20bfb",
    "entry_id": "59264073a2a60c0c08e20bfd",
    "data_id": "6052e8072315c0075001d65e"
}
```

**响应参数：**

| 参数 | 类型 | 说明 |
|---|---|---|
| status | String | 请求结果 |

**响应示例：**

```json
{
    "status": "success"
}
```

---

### 3.9 删除多条数据接口

#### 版本历史

| 版本 | 更新时间 | 说明 |
|------|----------|------|
| v1 | 2022.6.14 | 原始接口 |
| v5 | 2022.10.28 | 请求频率提升至 10次/秒；参数放入 body |

#### 接口调用

- **请求地址**: `https://api.jiandaoyun.com/api/v5/app/entry/data/batch_delete`
- **请求频率**: 10 次/秒
- **请求方式**: POST

**请求参数：**

| 参数 | 类型 | 必需 | 说明 |
|---|---|---|---|
| app_id | String | 是 | 应用ID |
| entry_id | String | 是 | 表单ID |
| data_ids | String[] | 是 | 要删除的数据 ID 数组 |

**请求示例：**

```json
{
    "app_id": "59264073a2a60c0c08e20bfb",
    "entry_id": "59264073a2a60c0c08e20bfd",
    "data_ids": [
        "200001181fe09728936510eb",
        "200001181fe09728936510ec",
        "200001181fe09728936510ed"
    ]
}
```

**响应参数：**

| 参数 | 类型 | 说明 |
|---|---|---|
| status | String | 返回 "success" 表示成功 |
| success_count | Number | 成功删除的数据条数 |

**响应示例：**

```json
{
    "status": "success",
    "success_count": 3
}
```

---

## 4. 文件接口

### 4.1 获取文件上传凭证和上传地址接口

#### 版本历史

| 接口版本 | 更新时间 | 版本说明 |
|---|---|---|
| v1 | 2021.12.30 | 原始接口 |
| v5 | 2022.10.28 | 请求频率提升至 20次/秒；参数 app_id 和 entry_id 放入 body；路由修改为 POST app/entry/file/get_upload_token |

#### 接口调用

- **请求地址**: `https://api.jiandaoyun.com/api/v5/app/entry/file/get_upload_token`
- **请求频率**: 20 次/秒
- **请求方式**: POST

每次请求返回 100 个文件上传凭证和上传地址。上传的文件与 `transaction_id` 绑定，只有相同 `transaction_id` 的新建或修改请求才能使用该文件。

**请求参数：**

| 参数 | 类型 | 必需 | 说明 |
|---|---|---|---|
| app_id | String | 是 | 应用ID |
| entry_id | String | 是 | 表单ID |
| transaction_id | String | 是 | 事务ID |

**注意事项：**
1. `transaction_id` 建议使用 UUID 格式
2. `transaction_id` 不能包含 `${var}`、`$(var)`、`$(var}`、`${var)` 格式文本

**请求示例：**

```json
{
    "app_id": "59264073a2a60c0c08e20bfb",
    "entry_id": "59264073a2a60c0c08e20bfd",
    "transaction_id": "87cd7d71-c6df-4281-9927-469094395677"
}
```

**响应参数：**

| 参数 | 类型 | 说明 |
|---|---|---|
| token_and_url_list | JSON | 文件上传凭证和上传地址 |
| token_and_url_list[].url | String | 文件上传地址 |
| token_and_url_list[].token | String | 文件上传凭证 |

### 4.2 文件上传接口

- **请求地址**: `{url}` (从获取上传凭证接口返回)
- **请求频率**: 20 次/秒
- **请求方式**: POST (form-data 格式)

**请求参数：**

| 参数 | 必需 | 类型 | 说明 |
|---|---|---|---|
| token | 是 | String | 文件上传凭证 |
| file | 是 | File | 要上传的文件 |

**注意事项：**
1. 请求需要文件上传，参数必须为 form-data 格式
2. `file` 参数必须放在**最后**
3. 一个 token 只能上传一个文件，不允许覆盖

**响应参数：**

| 参数 | 类型 | 说明 |
|---|---|---|
| key | String | 文件 key |

**响应示例：**

```json
{
    "key": "6b559cf1-b16c-43bd-a211-8fa8fdeae2ef"
}
```

**注意事项：**
- `token` 有效期为 **1 小时**
- `transaction_id` 与 `key` 配合使用，`transaction_id` 有效期也为 **1 小时**，过期后 `key` 也不可使用

---

## 5. 流程接口

### 接口列表

| 接口名称 | 释义 |
|---|---|
| 获取单条流程表单数据的审批意见 | 获取单条表单流程数据的审批意见 |
| 查询流程实例信息 | 查询流程实例信息 |
| 结束流程实例 | 结束当前流程实例 |
| 流程待办查询 | 获取当前用户待办信息 |
| 流程待办提交 | 提交流程待办 |
| 流程待办回退 | 回退流程待办 |
| 流程待办转交 | 转交流程待办 |
| 流程激活 | 激活当前流程实例 |
| 流程待办撤回 | 将流程待办撤回 |
| 流程待办加签 | 对当前流程的待办加签 |
| 查询流程日志 | 查询流程日志 |
| 流程待办否决 | 否决流程待办 |
| 查询抄送列表 | 查询抄送列表 |

### 流程错误码表

| 错误码 | 说明 |
|---|---|
| 4005 | 操作失败，不允许撤回 |
| 4007 | 操作失败，没有流程处理人 |
| 4008 | 操作失败，流程已经关闭 |
| 4009 | 操作失败，无权限 |
| 4016 | 操作失败，流程不能转交给自己 |
| 4026 | 流程状态，进行中流程无法激活 |
| 5003 | 流程节点不存在 |
| 5004 | 未提交流程审批意见 |
| 5006 | 无法将数据流转到抄送节点 |
| 5008 | 找不到对应的负责人 |
| 5009 | 找不到回退后的负责人 |
| 5010 | 无效的流程数据 |
| 5011 | 找不到流转节点 |
| 5012 | 未提交流程手写签名 |
| 5024 | 当前用户对该节点无提交权限 |
| 5025 | 当前节点已经流转完成 |
| 5026 | 流程节点批量审批失败 |
| 5034 | 目标节点包含子流程/插件节点 |
| 5044 | 子流程配置错误或找不到发起人 |
| 5045 | 发起子流程数据超过上限 200 |
| 5049 | 当前流程节点未开启转交 |
| 5053 | 流入多级主管审批节点失败，未指定发起部门 |
| 5056 | 不能对非流程表单进行流程操作 |
| 5058 | 数据已关联流程，不可重复发起 |
| 5059 | 数据提交人已被删除 |
| 5060 | 非流程表单，不支持该操作 |
| 50000 | 目标节点不存在 |
| 50004 | 待办任务不存在 |
| 50009 | 流程已被处理，不允许撤回 |
| 50013 | 负责人调整前后数目必须一致 |
| 50015 | 负责人调整前后无实际变化 |
| 50016 | 流程实例不存在 |
| 50019 | 不支持的审批行为 |
| 50024 | 调整后负责人不能为空 |
| 50031 | 流程数据不存在 |
| 50034 | 不支持的流程操作类型 |
| 50040 | 当前节点禁止回退 |
| 50041 | 回退节点为当前节点 |
| 50046 | 历史待办（子流程）过多，不允许激活 |
| 50049 | 不允许回退到没有创建者的发起节点 |
| 50052 | 节点不支持该加签行为 |
| 50053 | 加签候选人列表不能为空 |
| 50054 | 不支持嵌套加签 |
| 50057 | 加签配置未开启 |
| 50059 | 加签候选人不能选择节点负责人 |
| 50060 | 加签候选人非法 |
| 50061 | 不支持多人加签 |
| 50062 | 待被加签人处理中 |
| 50063 | 被加签待办不可批量提交 |
| 50064 | 异步子流程成环，请调整流程配置 |
| 50070 | 不允许回退到插件节点 |
| 50071 | 版本不支持插件节点 |
| 50073 | 禁止回退到进行中节点 |
| 50076 | 该节点不可激活 |

---

## 6. 通讯录接口

### 实体结构

#### 6.1 部门实体结构（department）

| 属性 | 类型 | 含义 | 备注 |
|---|---|---|---|
| dept_no | Number | 部门编号，企业内唯一 | 不同企业之间可能存在重复 |
| name | String | 部门名称 | — |
| parent_no | Number | 父部门编号 | 在企业互联接口中(外部部门)不存在 |
| type | Number | 部门类型 | 0: 常规部门; 2: 企业互联外部部门 |
| status | Number | 部门状态 | 1: 使用中; -1: 集成模式下同步后删除的部门 |
| integrate_id | String | 集成模式同步部门关联 ID | 仅在集成模式下返回，企业互联接口不返回 |
| seq | Number | 部门排序 | 在父部门内的序号，从小到大排列 |

#### 6.2 成员实体结构（user）

| 属性 | 类型 | 含义 | 备注 |
|---|---|---|---|
| username | String | 成员编号，企业内唯一 | 不同企业之间可能存在重复 |
| name | String | 昵称 | — |
| departments | Number[] | 成员所在部门编号列表 | — |
| type | Number | 成员类型 | 0: 常规成员; 2: 企业互联外部对接人 |
| status | Number | 成员状态 | 0: 未确认; 1: 已加入 |
| integrate_id | String | 集成模式同步成员关联 ID | 仅在集成模式下返回 |

#### 6.3 角色实体结构（role）

| 属性 | 类型 | 含义 | 备注 |
|---|---|---|---|
| role_no | Number | 角色编号，企业内唯一 | 不同企业之间可能存在重复 |
| group_no | Number | 角色组编号 | — |
| name | String | 角色名称 | — |
| type | Number | 角色类型 | 0: 常规角色; 2: 企业互联外部角色 |
| status | Number | 角色状态 | 1: 使用中 |
| integrate_id | String | 集成模式同步关联 ID | 仅在集成模式下返回 |

#### 6.4 角色组实体结构（role_group）

| 属性 | 类型 | 含义 | 备注 |
|---|---|---|---|
| group_no | Number | 角色组编号, 企业内唯一 | — |
| name | String | 角色组名称 | — |
| type | Number | 角色组类型 | 0: 常规角色组; 2: 企业互联外部角色组 |
| status | Number | 角色组状态 | 1: 使用中 |
| integrate_id | String | 集成模式同步角色组关联 ID | 仅在集成模式下（飞书除外）返回 |

### 版本说明

| 接口类型 | v1 | v2 | v4 | v5 |
|---|---|---|---|---|
| 成员 | 使用 _id 作为 id | 使用 username 作为 id | 新增 type、status、integrate_id | v4 基础上频率提升 |
| 部门 | 使用 _id 作为id | 使用 dept_no 作为 id | 新增 type、status、integrate_id | v4 基础上频率提升 |
| 角色 | 无 | 角色使用 role_no，角色组使用 group_no | 包含 integrate_id、type 字段 | 新增 status，v4 基础上频率提升 |
| 企业互联 | 无 | 无 | 成员使用 username，部门使用 dept_no | v4 基础上频率提升 |

### 通讯录接口列表

#### 成员接口

| 接口 | 链接 |
|---|---|
| 获取成员信息接口 | /open/18509 |
| 添加成员接口 | /open/18510 |
| 修改成员接口 | /open/18511 |
| 删除成员接口 | /open/18512 |
| 批量删除成员接口 | /open/18513 |
| 增量导入成员接口 | /open/18514 |

#### 部门接口

| 接口 | 链接 |
|---|---|
| （递归）获取部门成员接口 | /open/18515 |
| （递归）获取部门列表接口 | /open/18516 |
| 创建部门接口 | /open/18517 |
| 修改部门接口 | /open/18518 |
| 删除部门接口 | /open/18519 |
| 获取集成模式部门编号接口 | /open/18520 |
| 全量导入部门接口 | /open/18521 |
| 获取部门主管列表接口 | /open/25948 |
| 设置部门主管接口 | /open/25949 |

#### 角色接口

| 接口 | 链接 |
|---|---|
| 列出角色接口 | /open/18522 |
| 创建一个自建角色 | /open/18523 |
| 更新一个自建角色 | /open/18524 |
| 删除一个自建角色 | /open/18525 |
| 列出角色下的成员 | /open/18526 |
| 为自建角色批量添加成员 | /open/18527 |
| 为自建角色批量移除成员 | /open/18528 |

#### 角色组接口

| 接口 | 链接 |
|---|---|
| 列出自建角色组 | /open/18529 |
| 创建自建角色组 | /open/18530 |
| 更新自建角色组 | /open/18531 |
| 删除自建角色组 | /open/18532 |

#### 企业互联接口

| 接口 | 链接 |
|---|---|
| 列出我连接的企业 | /open/18533 |
| 列出我连接的企业的对接人 | /open/18534 |
| 获取我连接的企业对接人的详细信息 | /open/18535 |

### 注意事项

1. 每个通讯录是一个部门树，根部门的 dept_no 始终为 **1**
2. 公共模式和集成模式的支持差异在各具体接口中说明
3. 企业微信/钉钉的部门编号与简道云的 dept_no 暂时一致，但飞书平台部门 ID 为字符串，与 dept_no 不同

---

## 7. 字段与数据类型映射表

### 7.1 表单字段

| 字段名称 | 字段类型 | 数据类型 | 数据样例 | 备注 |
|---|---|---|---|---|
| 单行文本 | text | String | "张三" | — |
| 多行文本 | textarea | String | "我爱简道云" | — |
| 流水号 | sn | String | "00001" | — |
| 数字 | number | Number | 10 | — |
| 日期时间 | datetime | String | "2018-01-01T10:10:10.000Z" | UTC 统一时间格式字符串 |
| 单选按钮组 | radiogroup | String | "一年级" | — |
| 复选框组 | checkboxgroup | Array | ["选项1","选项2"] | — |
| 下拉框 | combo | String | "女" | — |
| 下拉复选框 | combocheck | Array | ["选项1","选项2"] | — |
| 地址 | address | JSON | {"province":"江苏省","city":"无锡市","district":"梁溪区","detail":"清扬路138号茂业天地"} | — |
| 定位 | location | JSON | {"province":"江苏省","city":"无锡市","district":"梁溪区","detail":"清扬路138号茂业天地","lnglatXY":[120.31237,31.49099]} | lnglatXY 表示 [经度,纬度] |
| 图片 | image | Array | [{"name":"image1.png","size":262144,"mime":"image/png","url":"https://..."}] | URL 有效期 15 天 |
| 附件 | upload | Array | [{"name":"产品说明文档.pdf","size":524288,"mime":"application/pdf","url":"https://..."}] | URL 有效期 15 天 |
| 子表单 | subform | Array | [{"_id":"5b23...","_widget_1529400746031":...}] | _id 为服务器生成的子表单数据 ID |
| 选择数据 | linkdata | JSON | {"id":"5b237548b22ab14884086cc0"} | id 为关联数据的 ID |
| 手写签名 | signature | JSON | {"name":"signature.png","size":1024,"mime":"image/png","url":"https://..."} | URL 有效期 15 天 |
| 成员单选 | user | JSON | {"name":"小简","username":"xiaojian","status":1,"type":0,"departments":[1,3],"integrate_id":"xiaojian"} | username 为成员编号；status: -1=离职, 0=未加入, 1=已加入 |
| 成员多选 | usergroup | Array | [{"name":"小简","username":"xiaojian",...}] | status 同上 |
| 部门单选 | dept | JSON | {"name":"经理部","dept_no":1,"type":0,"parent_no":2,"status":1,"integrate_id":1} | dept_no 为部门编号 |
| 部门多选 | deptgroup | Array | [{"name":"经理部","dept_no":1,...}] | — |
| 手机 | phone | JSON | {"phone":"13566666666","verified":true} | 提交数据时 verified 不需要提交 |
| 关联数据 | lookup | String | "66e10594b3eeff4d9888ad43" | 数据全局唯一 ID |
| 计算 | aggregation | Number | 20 | — |
| 计算文本 | aggregationtext | String | "发货成功" | — |
| 富文本 | richtext | JSON | {"html":"<p>Hello</p>","attachments":[...]} | URL 有效期 15 天 |

### 7.2 系统字段

| 系统字段 | 字段名 | 数据类型 | 数据样例 | 备注 |
|---|---|---|---|---|
| 应用Id | appId | String | "5b237267b22ab14884086c49" | 全局唯一 ID |
| 表单Id | entryId | String | "5b237267b22ab14884086cc9" | appId + entryId 确保表单 ID 唯一 |
| 数据ID | _id | String | "5b237267b22ab14884086c50" | 数据全局唯一 ID |
| 扩展字段 | ext | String | "广州" | — |
| 提交时间 | createTime | String | "2018-01-01T10:10:10.000Z" | — |
| 修改时间 | updateTime | String | "2018-01-01T10:10:10.000Z" | — |
| 提交人 | creator | JSON | {"name":"小简","username":"xiaojian",...} | status: -1=离职, 0=未加入, 1=已加入 |
| 修改人 | updater | JSON | {"name":"小简","username":"xiaojian",...} | status 同上 |
| 流程状态 | flowState | Number | "0" | 仅流程表单支持。0=进行中, 1=已完成, 2=手动结束, 3=否决 |

### 7.3 时间格式限制

写入数据时支持的时间格式：

| 支持格式 | 示例 | 备注 |
|---|---|---|
| ISO 日期格式 | '2018-11-09T10:00:00Z' 或 '2018-11-09T10:00:00' | 尾部 Z 代表 UTC 0 时区 |
| 毫秒时间戳 | 1639106951523 | 1639106951（秒）和 0 无效 |
| rfc 3339 | '2020-06-04 14:41:54.767135400+08:00' | — |
| yyyy-MM-dd HH:mm:ss | '2021-10-10 10:10:10' | — |
| yyyy-MM-dd | '2021-10-10' | — |

**不支持的时间格式：** null, undefined, '', IETF 日期格式, 斜杠分隔格式, 数组包裹, 非标准格式

---

## 8. API操作关联关系表

| 功能 | create | update | delete | batch_create | batch_update |
|---|---|---|---|---|---|
| 数据工厂延时计算 | 触发 | 触发 | 触发 | 触发 | 触发 |
| 数据消息推送 | 触发 | 触发 | 不触发 | 触发 | 触发 |
| 触发聚合表 | 触发 | 触发 | 触发 | 触发 | 触发 |
| 数据操作日志 | 记录 | 记录 | 记录 | 记录 | 记录 |
| webhook数据推送 | 不触发 | 不触发 | 不触发 | 不触发 | 不触发 |
| 智能助手 | 可触发 | 可触发 | 可触发 | 不触发 | 不触发 |
| 重复值校验 | 不校验 | 不校验 | — | 不校验 | 不校验 |
| 表单校验 | 不校验 | 不校验 | — | 不校验 | 不校验 |
| 必填校验 | 不校验 | 不校验 | — | 不校验 | 不校验 |
| 流程节点校验 | 不校验 | 不校验 | — | 不校验 | 不校验 |
| 触发流程 | 可触发 | 不触发 | — | 可触发 | 不触发 |
| 聚合表校验 | 校验 | 校验 | 触发 | 不校验 | 不校验 |
| 字段联动、公式 | 不触发 | 不触发 | — | 不触发 | 不触发 |
| 表单推送提醒 | 触发 | 触发 | — | 不触发 | 不触发 |

---

## 9. 错误对照表

所有 API 使用 **状态码 + 错误码** 响应格式。

成功：HTTP 状态码 2xx
错误：HTTP 状态码 400，响应体包含 `code` 和 `msg` 字段。

### 9.1 HTTP 状态码

| 状态码 | 说明 |
|---|---|
| 2xx | 成功响应 |
| 400 | 统一错误响应 |
| 429 | 请求并发限制超出 |
| 502 | 网关异常 |
| 579 | 文件上传失败 |

### 9.2 错误码（状态码为 400 时）

| 错误码 | 说明 | 排查建议 |
|---|---|---|
| 1 | 请求参数无效 | 检查是否有缺少的参数 |
| 1005 | 邮箱已存在 | 尝试邮箱验证码登录确认注册 |
| 1010 | 成员不存在 | 检查成员参数 |
| 1017 | 用户名格式无效 | 格式：字母、数字、下划线，最长50字符 |
| 1018 | 邮箱格式无效 | 检查邮箱地址格式 |
| 1019 | 成员昵称格式无效 | 80字符以内，无特殊字符 |
| 1022 | 成员当前公司/团队不存在 | 稍后重试；如持续请联系技术支持 |
| 1024 | 手机号无效 | 重新输入手机号 |
| 1027 | 手机号已存在 | 使用手机验证码登录确认注册 |
| 1058 | 没有权限调用任务列表 | 用户权限不足 |
| 1065 | 成员已添加到团队 | 检查用户是否已存在 |
| 1082 | 手机号/邮箱不能同时为空 | — |
| 1085 | 成员昵称不能为空 | — |
| 1087 | 唯一字段重复 | 检查是否有重复的成员编号 |
| 1092 | 用户名长度超出限制 | 员工编号50字符以内 |
| 1096 | 请求包含无效的成员参数 | 检查成员参数后重试 |
| 1201 | 角色不存在 | 企业角色不存在 |
| 1202 | 无法操作同步角色或角色组 | — |
| 1203 | 角色/角色组信息无效 | 检查参数 |
| 1205 | 角色组为必填 | — |
| 1206 | 角色组不存在 | — |
| 1207 | 角色/角色组名称长度超出限制 | 24字符以内 |
| 1208 | 不能删除有成员的角色组 | 先移除成员再删除 |
| 2004 | 应用不存在 | — |
| 3000 | 表单不存在 | — |
| 3001 | 成员或部门名称为必填 | — |
| 3005 | 请求包含无效参数 | — |
| 3041 | 表单中流水号字段数超出限制 | 每个表单最多一个流水号字段 |
| 3042 | 字段别名验证失败 | 检查别名是否包含特殊字符 |
| 3083 | 表单中控件数超出限制 | 通常上限500 |
| 3091 | 表单名称字符数超过100 | — |
| 3092 | 标题字符数超过100 | — |
| 4000 | 数据提交失败 | — |
| 4001 | 数据不存在 | — |
| 4007 | 没有流程处理人 | — |
| 4008 | 流程已关闭 | — |
| 4009 | 无审批权限 | — |
| 4012 | 操作失败，表单正在被其他批量编辑任务使用 | 稍后重试 |
| 4015 | 转交节点审批人无效 | — |
| 4016 | 流程不能转交给自己 | — |
| 4025 | 无数据流程权限 | — |
| 4042 | 数据删除失败 | 检查参数 |
| 4402 | 聚合计算验证失败 | 检查参数 |
| 4815 | 筛选条件无效 | 条件可能过长，联系技术支持 |
| 5003 | 流程节点不存在 | — |
| 5004 | 未提交审批意见 | — |
| 5009 | 回退后找不到负责人 | — |
| 5011 | 目标节点无效 | — |
| 5012 | 未提交手写签名 | — |
| 5034 | 目标节点包含子流程/插件节点 | — |
| 5044 | 子流程配置错误或找不到发起人 | — |
| 5045 | 发起子流程数据超过上限200 | — |
| 5049 | 当前流程节点未开启转交 | — |
| 5053 | 流入多级主管审批节点失败，未指定发起部门 | — |
| 6000 | 同级下存在同名子部门 | — |
| 6001 | 父部门不存在 | — |
| 6002 | 部门不存在 | — |
| 6003 | 不能删除有子部门的部门 | — |
| 6004 | 部门更新失败 | 重试或联系技术支持 |
| 6005 | 部门创建失败 | 重试或联系技术支持 |
| 6006 | 不能删除有成员的部门 | — |
| 6010 | 部门 ID 格式无效 | — |
| 6011 | 部门之间存在循环关系 | — |
| 6012 | 部门名称无效 | — |
| 6013 | 同级下部门 ID 已存在 | — |
| 6014 | 根部门必须至少有一个子部门 | — |
| 6015 | 不能删除根部门 | — |
| 6017 | 部门级联层数超出限制 | 最大16层 |
| 6019 | 成员列表不能为空 | — |
| 6020 | 单次导入部门数超出限制 | 上限10万 |
| 6021 | 单次导入成员数超出限制 | 上限2万 |
| 6064 | 父部门已存在 | — |
| 7103 | 系统用量超出限制，系统已被暂停 | 检查版本详情并升级 |
| 7206 | 系统限制超出，系统已被停用 | 联系创建者升级或减少用量 |
| 7212 | 月度数据量超出限制，不能提交新数据 | 联系业务负责人升级 |
| 7216-7219 | 附件上传限制超出 | 联系创建者或业务负责人 |
| 7221 | 表单已超出限制，暂时停用 | API 新增数据限制超出 |
| 8017 | 公司/团队不存在或已关闭 | — |
| 8301 | API Key 鉴权验证失败 | 检查参数 |
| 8302 | 无 API 调用权限 | 检查参数 |
| 8303 | 公司/团队调用频率超出限制 | 等待1秒后重试 |
| 8304 | 调用频率超出限制 | 等待1秒后重试 |
| 9004 | 任务创建失败 | 重试或联系技术支持 |
| 9007 | 获取锁失败 | 重试或联系技术支持 |
| 17017 | 请求包含无效参数 | 平台 API 参数错误 |
| 17018 | API Key 无效 | — |
| 17023 | 一次批量更新超出限制 | 上限100 |
| 17024 | 一次批量创建超出限制 | 上限100 |
| 17025 | transaction_id 包含无效参数 | 格式错误 |
| 17026 | transaction_id 已存在 | 修改后重试 |
| 17027 | API 文件上传失败 | 重试或联系技术支持 |
| 17032 | 字段类型不支持 | — |
| 17033 | 批量删除数量超出限制 | — |
| 17034 | 子字段类型不支持 | — |
| 17052 | 不在 IP 白名单中 | 检查 API Key 配置 |
| 17053 | 不在授权应用范围内 | 检查 API Key 配置 |
| 17054 | 不在授权 API 范围内 | 检查 API Key 配置 |
| 30002 | 无法获取预设 CRM 表单 | CRM 预设表单不支持 API 调用 |
| 50000 | 目标节点不存在 | — |
| 50004 | 任务不存在 | — |
| 50008 | 流程处理错误 | 重试或联系技术支持 |
| 50011 | 任务不存在 | — |
| 50014 | 无权限关闭任务 | 操作人不能为空 |
| 50016 | instance_id 无效 | — |
| 50019 | 不支持的审批行为 | — |
| 50021 | data_id 无效 | — |
| 50031 | data_id 无效 | — |
| 50040 | 当前节点禁止回退 | — |
| 50041 | 不能回退到当前节点 | — |
| 50047 | 流程正在迁移，请稍后重试 | — |
| 50049 | 不能回退到没有创建者的发起节点 | — |
| 50051 | 流程已被审批/转交/回退 | 刷新页面查看 |
| 50053 | 加签候选人列表不能为空 | — |
| 50054 | 不支持嵌套加签 | — |
| 50055 | 未添加前/后加签人 | — |
| 50056 | 父级任务丢失 | — |
| 50057 | 加签功能未开启 | — |
| 50059 | 成员已被添加为审批人 | — |
| 50060 | 审批人无效 | — |
| 50061 | 不能添加超过一个审批人 | — |
| 50062 | 被加签人正在审核任务 | — |
| 50070 | 不能回退到插件节点 | — |
| 50073 | 不能回退到进行中节点 | — |
| 50082 | 缺少回退人员选择 | — |

---

## API 接口路由汇总

| 接口 | 路由 | 版本 | 频率 |
|---|---|---|---|
| 表单字段查询 | `POST /api/v5/app/entry/widget/list` | v5 | 30次/秒 |
| 查询单条数据 | `POST /api/v5/app/entry/data/get` | v5 | 30次/秒 |
| 查询多条数据 | `POST /api/v5/app/entry/data/list` | v5 | 30次/秒 |
| 新建单条数据 | `POST /api/v5/app/entry/data/create` | v5 | 20次/秒 |
| 新建多条数据 | `POST /api/v5/app/entry/data/batch_create` | v5 | 10次/秒 |
| 修改单条数据 | `POST /api/v5/app/entry/data/update` | v5 | 20次/秒 |
| 修改多条数据 | `POST /api/v5/app/entry/data/batch_update` | v5 | 10次/秒 |
| 删除单条数据 | `POST /api/v5/app/entry/data/delete` | v5 | 20次/秒 |
| 删除多条数据 | `POST /api/v5/app/entry/data/batch_delete` | v5 | 10次/秒 |
| 获取上传凭证 | `POST /api/v5/app/entry/file/get_upload_token` | v5 | 20次/秒 |
| 文件上传 | `POST {url}` (七牛上传地址) | v5 | 20次/秒 |

**所有接口基础URL**: `https://api.jiandaoyun.com`

<!-- Packaged by Esther Zhu (Esther.Zhu@fanruan.com) from JianDaoyun open-platform docs. -->
