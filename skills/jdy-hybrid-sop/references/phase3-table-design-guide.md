# 建表规范与字段映射表格式（Phase 3）

> 本规范定义 JDY Hybrid 项目在简道云中建表的命名、顺序、关联关系及字段映射表的标准格式。

---

## 1. 命名规范

### 1.1 表单命名

| 规则 | 示例 | 说明 |
|------|------|------|
| 前缀标识模块 | `pur_采购订单` | 模块缩写 + 中文业务名 |
| 模块缩写 ≤ 4字母 | `pur`, `wh`, `hr`, `fin` | 见下方模块缩写表 |
| 禁止拼音 | ❌ `caigou_dingdan` | 使用英文缩写或中文 |
| 子表单加 `_sub` 后缀 | `pur_采购明细_sub` | 区分独立表与子表单 |
| 字典表加 `_dict` 后缀 | `sys_状态_dict` | 全局枚举/选项表 |

**常用模块缩写参考**：

| 缩写 | 模块 | 缩写 | 模块 |
|------|------|------|------|
| pur | 采购 | wh | 仓储 |
| sal | 销售 | fin | 财务 |
| hr | 人事 | mfg | 生产 |
| qa | 质检 | sys | 系统 |
| cust | 客户 | proj | 项目 |

### 1.2 字段命名

| 规则 | 示例 | 说明 |
|------|------|------|
| 小写蛇形 | `supplier_name` | 禁止驼峰、中文、空格 |
| 语义明确 | `order_date` ✅ / `date` ❌ | 避免歧义 |
| 外键加 `_id` 后缀 | `supplier_id` | 关联其他表单的字段 |
| 布尔加 `is_` 前缀 | `is_active` | 值为 true/false |
| 金额统一分单位 | `amount_cents` | 或在注释中标明精度 |
| 时间戳加 `_at` 后缀 | `created_at`, `approved_at` | ISO 8601 格式 |
| 预留字段 | `ext_json` | TEXT 类型，存扩展数据 |

---

## 2. 建表顺序（5 步）

严格按以下顺序建表，避免关联引用缺失：

```
Step 1 → 字典表（_dict）
         所有枚举、选项、分类表优先建立
         例：sys_状态_dict, sys_币种_dict, pur_物料分类_dict

Step 2 → 主数据表
         被多方引用的基础实体
         例：cust_客户主数据, pur_供应商主数据, pur_物料主数据

Step 3 → 业务主表
         核心业务单据头
         例：pur_采购订单, sal_销售合同, wh_入库单

Step 4 → 业务明细表 / 子表单
         依附于主表的行项目
         例：pur_采购明细_sub, sal_合同条款_sub

Step 5 → 关联/中间表
         多对多关系的桥接表
         例：proj_项目成员_rel, pur_订单标签_rel
```

> ⚠️ **每完成一步，立即验证**：表是否创建成功、字段类型是否正确、关联关系是否生效。不要累积到最后统一验证。

---

## 3. 关联关系规范

### 3.1 单向关联（最常用）

```
[采购订单].supplier_id  →  [供应商主数据]._id
```

- 在子表上建「关联查询」或「关联数据」字段指向父表
- 父表**不需要**反向字段
- 适用：一对多、多对一

### 3.2 自引用关联

```
[组织架构].parent_dept_id  →  [组织架构]._id
```

- 同一表单内字段引用自身 `_id`
- 必须设置根节点的 parent 为空
- 适用：树形结构（组织、分类、BOM）

### 3.3 多对多关联

```
[项目] ←→ [项目成员_rel] ←→ [用户]
```

- **必须使用中间表**，禁止在任一方存逗号分隔 ID
- 中间表命名：`{表A}_{表B}_rel`
- 中间表至少包含：`a_id`, `b_id`, `created_at`
- 可附加关系属性：`role`, `sort_order`

### 3.4 子表单 vs 独立表决策

| 维度 | 子表单 | 独立表 |
|------|--------|--------|
| 数据量 | 单主表 < 50 行 | 可能 > 100 行或无限增长 |
| 独立查询 | 不需要单独搜索/统计 | 需要独立列表/报表 |
| 生命周期 | 随主表创建删除 | 有独立生命周期 |
| 跨表引用 | 不被其他表引用 | 被多个表引用 |
| 权限控制 | 继承主表权限 | 需要独立权限 |
| **推荐场景** | 订单明细、审批意见 | 物料、客户、日志 |

> 💡 **经验法则**：如果不确定，先用子表单；当出现"需要在子表单上做独立筛选/统计"时再拆为独立表。

---

## 4. 字段映射表 JSON 完整示例

> 此 JSON 是前后端对接、代码生成、自动化测试的核心契约文件。
> 
> **生成方式**：使用 `jdy_gen_field_mapping` 工具自动生成，或手动编写语义化格式。

### 4.1 自动生成格式（jdy_gen_field_mapping 输出）

> 工具自动遍历简道云应用生成，key 为 widget_id（即 `_widget_xxx`）。

```json
{
  "app_id": "app_abc123def456",
  "version": "1.0.0",
  "generated_at": "2026-06-13T10:30:00",
  "forms": {
    "6a221e50149908216c2d30a6": {
      "form_name": "pur_采购订单",
      "entry_id": "6a221e50149908216c2d30a6",
      "fields": {
        "_widget_1780620881780": {
          "widget": "_widget_1780620881780",
          "type": "text",
          "label": "采购单号"
        },
        "_widget_1780620881781": {
          "widget": "_widget_1780620881781",
          "type": "related_data",
          "label": "供应商"
        },
        "_widget_1780620881782": {
          "widget": "_widget_1780620881782",
          "type": "number",
          "label": "订单总金额(元)"
        },
        "_widget_1780620881783": {
          "widget": "_widget_1780620881783",
          "type": "dropdown",
          "label": "订单状态"
        },
        "_widget_1780620881784": {
          "widget": "_widget_1780620881784",
          "type": "datetime",
          "label": "下单日期"
        },
        "_widget_1780620881785": {
          "widget": "_widget_1780620881785",
          "type": "member",
          "label": "创建人"
        },
        "_widget_1780620881786": {
          "widget": "_widget_1780620881786",
          "type": "textarea",
          "label": "备注"
        }
      }
    },
    "6a221e50149908216c2d30a7": {
      "form_name": "pur_供应商主数据",
      "entry_id": "6a221e50149908216c2d30a7",
      "fields": {
        "_widget_1780620881800": {
          "widget": "_widget_1780620881800",
          "type": "text",
          "label": "供应商编码"
        },
        "_widget_1780620881801": {
          "widget": "_widget_1780620881801",
          "type": "text",
          "label": "供应商名称"
        },
        "_widget_1780620881802": {
          "widget": "_widget_1780620881802",
          "type": "phone",
          "label": "联系电话"
        },
        "_widget_1780620881803": {
          "widget": "_widget_1780620881803",
          "type": "dropdown",
          "label": "合作状态"
        }
      }
    }
  }
}
```

### 4.2 语义化格式（手动编写，向后兼容）

> 开发者可手动编写语义化 key，便于代码可读性。FieldMapper 类兼容两种格式。

```json
{
  "app_id": "app_abc123def456",
  "version": "1.0.0",
  "forms": {
    "purchase_order": {
      "form_name": "pur_采购订单",
      "entry_id": "6a221e50149908216c2d30a6",
      "fields": {
        "order_no": {
          "widget_id": "_widget_1780620881780",
          "type": "text",
          "label": "采购单号",
          "required": true,
          "unique": true,
          "description": "自动生成，格式 PUR-YYYYMMDD-XXXX"
        },
        "supplier_id": {
          "widget_id": "_widget_1780620881781",
          "type": "related_data",
          "label": "供应商",
          "required": true,
          "target_form": "6a221e50149908216c2d30a7",
          "description": "关联供应商主数据"
        },
        "total_amount": {
          "widget_id": "_widget_1780620881782",
          "type": "number",
          "label": "订单总金额(元)",
          "required": true,
          "precision": 2,
          "min": 0,
          "description": "由明细行自动汇总"
        },
        "status": {
          "widget_id": "_widget_1780620881783",
          "type": "dropdown",
          "label": "订单状态",
          "required": true,
          "options": ["draft", "pending", "approved", "rejected", "completed"],
          "default": "draft"
        },
        "order_date": {
          "widget_id": "_widget_1780620881784",
          "type": "datetime",
          "label": "下单日期",
          "required": true,
          "format": "YYYY-MM-DD"
        },
        "creator": {
          "widget_id": "_widget_1780620881785",
          "type": "member",
          "label": "创建人",
          "required": true,
          "multi": false
        },
        "remark": {
          "widget_id": "_widget_1780620881786",
          "type": "textarea",
          "label": "备注",
          "required": false,
          "max_length": 500
        }
      }
    },
    "supplier": {
      "form_name": "pur_供应商主数据",
      "entry_id": "6a221e50149908216c2d30a7",
      "fields": {
        "supplier_code": {
          "widget_id": "_widget_1780620881800",
          "type": "text",
          "label": "供应商编码",
          "required": true,
          "unique": true
        },
        "supplier_name": {
          "widget_id": "_widget_1780620881801",
          "type": "text",
          "label": "供应商名称",
          "required": true
        },
        "contact_phone": {
          "widget_id": "_widget_1780620881802",
          "type": "phone",
          "label": "联系电话",
          "required": false
        },
        "cooperation_status": {
          "widget_id": "_widget_1780620881803",
          "type": "dropdown",
          "label": "合作状态",
          "options": ["active", "inactive", "blacklisted"],
          "default": "active"
        }
      }
    }
  }
}
```

### 4.3 两种格式对比

| 维度 | 自动生成格式 | 语义化格式 |
|------|-------------|-----------|
| **生成方式** | `jdy_gen_field_mapping` 工具 | 手动编写 |
| **表单 key** | entry_id（如 `6a221e50...`） | 语义名（如 `purchase_order`） |
| **字段 key** | widget_id（如 `_widget_xxx`） | 语义名（如 `order_no`） |
| **widget_id 位置** | key 本身 + `widget` 属性 | 字段内 `widget_id` 属性 |
| **可读性** | 低（全是 ID） | 高（业务语义） |
| **适用场景** | 快速生成、验证 | 长期维护、团队协作 |
| **FieldMapper 兼容** | ✅ | ✅ |

> 💡 **推荐工作流**：先用 `jdy_gen_field_mapping` 自动生成 → 手动重命名为语义化格式 → 提交 Git。

### 4.4 字段类型速查

| type | 说明 | type | 说明 |
|------|------|------|------|
| text | 单行文本 | datetime | 日期时间 |
| textarea | 多行文本 | date | 仅日期 |
| number | 数字（含精度） | member | 成员选择 |
| dropdown | 下拉单选 | related_data | 关联数据 |
| multi_select | 下拉多选 | subform | 子表单 |
| phone | 手机号 | attachment | 附件 |
| email | 邮箱 | formula | 公式计算 |
| system | 系统字段 | unknown | 未知类型 |

---

## 5. G3 门禁检查清单

> ✅ 全部通过方可进入 Phase 4 流程配置与 Phase 5 编码阶段

| # | 检查项 | 通过 | 责任人 | 备注 |
|---|--------|------|--------|------|
| 1 | 所有表单命名符合 `{模块缩写}_{中文名}` 规范 | ☐ | SA | |
| 2 | 所有字段命名符合小写蛇形规范，无语义歧义 | ☐ | SA | |
| 3 | 建表严格按 5 步顺序执行，无引用缺失 | ☐ | DEV | |
| 4 | 关联关系已按规范建立（单向/自引用/多对多/子表单） | ☐ | DEV | |
| 5 | 字段映射表 JSON 已生成（`jdy_gen_field_mapping` 工具） | ☐ | DEV | |
| 6 | 字段映射表 JSON 已通过 FieldMapper.validate() 校验 | ☐ | QA | |
| 7 | API 读写验证通过（`jdy_validate_api` 工具，all_passed=true） | ☐ | DEV | |
| 8 | 字典表数据已初始化（至少包含所有枚举值） | ☐ | DEV | |
| 9 | 主数据表已导入种子数据（≥ 10 条用于测试） | ☐ | DEV | |
| 10 | 字段权限矩阵已配置（按角色设定读写/隐藏） | ☐ | SA | |
| 11 | 建表文档已归档，字段映射表 JSON 已提交 Git | ☐ | PM | |

---

*文档版本: v2.0 | 最后更新: 2026-06-13 | 作者: 擎析 Agent*
