# 简道云字段类型与 API 数据格式映射

> 评估需求和设计数据接口时的快速查阅表

---

## 1. 表单字段类型

| 字段名称 | 字段类型 | 数据类型 | 数据样例 | API 可写入 | 备注 |
|----------|----------|----------|----------|:---:|------|
| 单行文本 | text | String | "张三" | ✅ | — |
| 多行文本 | textarea | String | "我爱简道云" | ✅ | — |
| 流水号 | sn | String | "00001" | ❌ | 系统自动生成 |
| 数字 | number | Number | 10 | ✅ | — |
| 日期时间 | datetime | String(ISO) | "2018-01-01T10:10:10.000Z" | ✅ | UTC格式 |
| 单选按钮组 | radiogroup | String | "一年级" | ✅ | — |
| 多选按钮组 | checkboxgroup | Array | ["一年级","二年级"] | ✅ | — |
| 下拉框 | combo | String | "选项一" | ✅ | 单选下拉 |
| 多选下拉框 | combocheck | Array | ["选项一","选项二"] | ✅ | — |
| 成员单选 | user | String | "username" | ✅ | 成员编号 |
| 成员多选 | usergroup | Array | ["user1","user2"] | ✅ | — |
| 部门单选 | dept | Number | 12 | ✅ | 部门编号 |
| 部门多选 | deptgroup | Array | [12, 13] | ✅ | — |
| 电话 | phone | Object | {"phone":"13800138000"} | ✅ | — |
| 地址 | address | Object | {"province":"省","city":"市","district":"区","detail":"详细地址"} | ✅ | — |
| 定位 | location | Object | {"province":"省","city":"市","district":"区","detail":"地址","lnglatXY":[120.1,30.2]} | ✅ | — |
| 图片 | image | Array | ["file-key-1"] | ✅ | 文件key数组 |
| 附件 | upload | Array | ["file-key-1","file-key-2"] | ✅ | 文件key数组 |
| 子表单 | subform | Array | [{"_widget_xxx":{"value":"值"}}] | ✅ | 每行含子字段 |
| 关联表单 | linkdata | Array | ["data_id_1"] | ✅ | 关联数据ID数组 |
| 手写签名 | signature | Object | {"url":"..."} | ❌ | API不可写入 |
| 分割线 | splitline | — | — | ❌ | 纯展示控件 |
| 选择数据 | — | — | — | ❌ | API不可写入 |
| 查询 | — | — | — | ❌ | API不可写入 |

---

## 2. 系统字段

| 字段名称 | 字段ID | 数据类型 | 说明 |
|----------|--------|----------|------|
| 流程状态 | flowState | Number | 0=未提交, 1=审批中, 2=通过, 3=拒绝, 5=撤回 |
| 创建人 | creator | Object | {"username":"xxx","name":"昵称"} |
| 创建时间 | createTime | String(ISO) | UTC格式 |
| 修改时间 | updateTime | String(ISO) | UTC格式 |
| 数据ID | _id | String | 全局唯一 |

---

## 3. 日期时间格式说明

所有日期时间字段使用 **ISO 8601 UTC 格式**：

```
2018-01-01T10:10:10.000Z
```

### 时区转换
- 北京时间 (UTC+8) = UTC 时间 + 8小时
- 示例：北京时间 2024-01-15 09:00:00 → API 值 "2024-01-15T01:00:00.000Z"

### 常用日期操作
| 场景 | filter 写法 |
|------|------------|
| 等于某天 | `{"field":"createTime","method":"eq","value":"2024-01-15"}` |
| 日期范围 | `{"field":"createTime","method":"range","value":["2024-01-01","2024-01-31"]}` |
| 今天之后 | `{"field":"createTime","method":"gte","value":"2024-01-15"}` |
| 不限结束 | `{"field":"createTime","method":"range","value":["2024-01-01",null]}` |

---

## 4. 文件字段处理流程

### 上传附件/图片的完整流程

```
1. 生成 UUID 作为 transaction_id
2. 调用 get_upload_token → 获取 url + token
3. POST form-data 到 url（token + file）→ 获取 key
4. 新建/修改数据时，将 key 填入 image/upload 字段的 value 数组中
   例：{"_widget_image": {"value": ["file-key-abc123"]}}
```

### 注意事项
- transaction_id 必须与后续数据操作的 transaction_id **完全一致**
- token 有效期 1 小时，超时需重新获取
- 读取数据时返回的 URL 有效期仅 15 天
- 如需永久访问，应将文件下载到自有存储

---

## 5. 子表单数据格式

### 读取时返回格式
```json
{
  "_widget_subform": [
    {
      "_id": "row_id_1",
      "_widget_child_text": "值1",
      "_widget_child_number": 100
    },
    {
      "_id": "row_id_2",
      "_widget_child_text": "值2",
      "_widget_child_number": 200
    }
  ]
}
```

### 修改时注意事项
- **保留已有行**：必须在每行中包含 `_id` 字段
- **新增行**：省略 `_id` 字段
- **删除行**：在修改数据中不包含该行

```json
{
  "_widget_subform": {
    "value": [
      {"_id": "row_id_1", "_widget_child_text": {"value": "修改后的值"}},
      {"_widget_child_text": {"value": "新增行的值"}}
    ]
  }
}
```

> ⚠️ 子表单最多 200 行（硬性约束 H2）
