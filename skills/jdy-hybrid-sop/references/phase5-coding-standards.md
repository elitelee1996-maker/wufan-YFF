# 编码规范（Phase 5）

> 本规范适用于 JDY Hybrid 项目中所有二开代码（后端 + 前端），确保代码可维护、可测试、可审计。

---

## 1. 后端规范

### 1.1 配置驱动读取字段 ID

**❌ 严禁硬编码字段 ID**

```python
# ❌ 错误：字段 ID 散落在业务代码中
result = jdy_api.query("form_x7k9m2p4q", fields=["fld_a1b2c3d4", "fld_e5f6g7h8"])
```

**✅ 正确：从配置文件中读取**

```python
# config/field_mapping.py
FIELD_MAPPING = {
    "purchase_order": {
        "form_id": "form_x7k9m2p4q",
        "fields": {
            "order_no": "fld_a1b2c3d4",
            "supplier_id": "fld_e5f6g7h8",
            "total_amount": "fld_i9j0k1l2",
            "status": "fld_m3n4o5p6"
        }
    }
}

# services/order_service.py
from config.field_mapping import FIELD_MAPPING

class OrderService:
    def __init__(self):
        self.form_config = FIELD_MAPPING["purchase_order"]
        self.form_id = self.form_config["form_id"]
        self.fields = self.form_config["fields"]

    def get_orders(self, filters: dict) -> list:
        field_ids = list(self.fields.values())
        return jdy_api.query(self.form_id, fields=field_ids, filter=filters)
```

> 💡 **配置文件来源**：直接从 Phase 3 产出的字段映射表 JSON 自动生成，禁止手动抄写。

### 1.2 统一响应格式

所有 API 接口必须返回统一结构：

```json
{
  "code": 0,
  "message": "success",
  "data": { ... },
  "request_id": "req_20240315_abc123",
  "timestamp": "2024-03-15T10:30:00+08:00"
}
```

**错误响应**：

```json
{
  "code": 40001,
  "message": "供应商不存在",
  "data": null,
  "request_id": "req_20240315_def456",
  "timestamp": "2024-03-15T10:31:00+08:00"
}
```

**错误码规范**：

| 范围 | 含义 | 示例 |
|------|------|------|
| 0 | 成功 | - |
| 40000-40099 | 参数校验错误 | 40001 必填字段缺失 |
| 40100-40199 | 认证/授权错误 | 40101 token过期 |
| 40300-40399 | 业务规则违反 | 40301 重复提交 |
| 40400-40499 | 资源不存在 | 40401 订单不存在 |
| 50000-50099 | 服务端内部错误 | 50001 数据库异常 |
| 50200-50299 | 外部服务调用失败 | 50201 简道云API超时 |

**后端实现示例**：

```python
from dataclasses import dataclass
from typing import Any, Optional
import uuid
from datetime import datetime

@dataclass
class ApiResponse:
    code: int = 0
    message: str = "success"
    data: Any = None
    request_id: str = ""
    timestamp: str = ""

    def __post_init__(self):
        if not self.request_id:
            self.request_id = f"req_{datetime.now():%Y%m%d}_{uuid.uuid4().hex[:8]}"
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data,
            "request_id": self.request_id,
            "timestamp": self.timestamp
        }

# 使用
@app.get("/api/orders")
async def get_orders():
    try:
        orders = await order_service.get_orders()
        return ApiResponse(data=orders).to_dict()
    except BusinessError as e:
        return ApiResponse(code=e.code, message=str(e)).to_dict()
    except Exception as e:
        logger.exception("Unexpected error")
        return ApiResponse(code=50001, message="系统内部错误").to_dict()
```

### 1.3 异常捕获规范

```python
# ✅ 分层捕获，禁止裸 except
async def create_order(payload: dict):
    # 1. 参数校验层
    try:
        validated = OrderCreateSchema(**payload)
    except ValidationError as e:
        raise BusinessError(code=40001, message=f"参数校验失败: {e}")

    # 2. 业务规则层
    supplier = await supplier_service.get_by_id(validated.supplier_id)
    if not supplier or supplier.status != "active":
        raise BusinessError(code=40301, message="供应商无效或已停用")

    # 3. 外部调用层
    try:
        result = await jdy_api.create_record(form_id, record_data)
    except JdyApiTimeoutError:
        raise ExternalServiceError(code=50201, message="简道云接口超时，请稍后重试")
    except JdyApiError as e:
        raise ExternalServiceError(code=50202, message=f"简道云接口错误: {e.detail}")

    # 4. 兜底
    # 不应到达此处，若到达说明有未预期的异常类型
    logger.error(f"Unhandled exception in create_order: {type(e).__name__}")
    raise SystemError(code=50001, message="系统内部错误")
```

**禁止事项**：
- ❌ `except Exception: pass` — 吞掉异常
- ❌ `except: ...` — 裸 except
- ❌ 在 except 中只 print 不 log
- ❌ 将原始异常信息暴露给前端（生产环境）

### 1.4 多步操作回滚

当一次业务操作涉及多个写入步骤时，必须实现补偿回滚：

```python
async def approve_order(order_id: str, approver: str):
    """审批通过：更新订单状态 + 生成入库单 + 发送通知"""
    completed_steps = []

    try:
        # Step 1: 更新订单状态
        await order_service.update_status(order_id, "approved")
        completed_steps.append(("update_status", order_id))

        # Step 2: 生成入库单
        inbound_id = await inbound_service.create_from_order(order_id)
        completed_steps.append(("create_inbound", inbound_id))

        # Step 3: 发送通知
        await notification_service.send_approval_notice(order_id, approver)
        completed_steps.append(("send_notice", order_id))

    except Exception as e:
        logger.error(f"approve_order failed at step, rolling back: {e}")
        # 逆序回滚
        for step_name, step_arg in reversed(completed_steps):
            try:
                if step_name == "send_notice":
                    await notification_service.revoke_notice(step_arg)
                elif step_name == "create_inbound":
                    await inbound_service.delete(step_arg)
                elif step_name == "update_status":
                    await order_service.update_status(step_arg, "pending")
            except Exception as rollback_err:
                logger.critical(f"Rollback failed for {step_name}: {rollback_err}")
                # 记录人工介入工单
                await alert_service.create_manual_intervention(
                    operation="approve_order",
                    failed_step=step_name,
                    context={"order_id": order_id, "error": str(rollback_err)}
                )
        raise BusinessError(code=50002, message="审批操作部分失败，已回滚，请联系管理员")
```

> ⚠️ **关键原则**：回滚本身也可能失败，必须有告警机制确保人工兜底。

---

## 2. 前端规范

### 2.1 API 客户端统一

**❌ 禁止直接使用 fetch/axios 散落各处**

```typescript
// ❌ 错误
const res = await fetch('/api/orders', { headers: { Authorization: token } });
const data = await res.json();
```

**✅ 正确：封装统一客户端**

```typescript
// src/utils/api-client.ts
import axios from 'axios';
import type { ApiResponse } from '@/types/api';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 15000,
});

// 请求拦截：注入 token + request_id
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  config.headers['X-Request-ID'] = crypto.randomUUID();
  return config;
});

// 响应拦截：统一解包 + 错误处理
client.interceptors.response.use(
  (response) => {
    const body = response.data as ApiResponse;
    if (body.code !== 0) {
      return Promise.reject(new BusinessError(body.code, body.message));
    }
    return body.data;
  },
  (error) => {
    if (error.response?.status === 401) {
      router.push('/login');
      return Promise.reject(error);
    }
    return Promise.reject(error);
  }
);

export const api = {
  get: <T>(url: string, params?: object) =>
    client.get<T>(url, { params }).then(r => r.data),
  post: <T>(url: string, data?: object) =>
    client.post<T>(url, data).then(r => r.data),
  put: <T>(url: string, data?: object) =>
    client.put<T>(url, data).then(r => r.data),
  delete: <T>(url: string) =>
    client.delete<T>(url).then(r => r.data),
};
```

### 2.2 Loading / Error 处理

```tsx
// ✅ 每个数据请求必须处理三态
function OrderList() {
  const { data, isLoading, error, refetch } = useQuery(['orders'], () =>
    api.get<Order[]>('/api/orders')
  );

  if (isLoading) return <Skeleton rows={5} />;
  if (error) return (
    <ErrorBanner
      message={error.message}
      onRetry={refetch}
    />
  );
  if (!data?.length) return <EmptyState description="暂无采购订单" />;

  return <OrderTable data={data} />;
}
```

**禁止事项**：
- ❌ 请求期间页面空白无任何反馈
- ❌ 错误只 console.log 不展示给用户
- ❌ loading 结束后不重置状态导致闪烁

### 2.3 写入操作验证

```tsx
// ✅ 所有写入操作必须有确认 + 防重复 + 结果反馈
function ApproveButton({ orderId }: { orderId: string }) {
  const [confirming, setConfirming] = useState(false);
  const mutation = useMutation(
    () => api.post(`/api/orders/${orderId}/approve`),
    {
      onSuccess: () => {
        toast.success('审批通过');
        queryClient.invalidateQueries(['orders']);
      },
      onError: (err: BusinessError) => {
        toast.error(err.message);
      },
    }
  );

  const handleApprove = () => {
    if (mutation.isLoading) return; // 防重复
    setConfirming(true);
  };

  return (
    <>
      <Button onClick={handleApprove} disabled={mutation.isLoading}>
        {mutation.isLoading ? '处理中...' : '审批通过'}
      </Button>
      <ConfirmModal
        open={confirming}
        title="确认审批通过？"
        content="通过后系统将自动生成入库单并通知相关人员"
        onConfirm={() => {
          setConfirming(false);
          mutation.mutate();
        }}
        onCancel={() => setConfirming(false)}
      />
    </>
  );
}
```

### 2.4 禁止硬编码 widget_id / field_id

```typescript
// ❌ 错误
const supplierField = record['fld_e5f6g7h8'];

// ✅ 正确：从配置常量读取
import { FIELD_IDS } from '@/config/field-mapping';

const supplierField = record[FIELD_IDS.purchaseOrder.supplierId];

// @/config/field-mapping.ts (由构建脚本从字段映射表JSON自动生成)
export const FIELD_IDS = {
  purchaseOrder: {
    formId: 'form_x7k9m2p4q',
    orderNo: 'fld_a1b2c3d4',
    supplierId: 'fld_e5f6g7h8',
    totalAmount: 'fld_i9j0k1l2',
    status: 'fld_m3n4o5p6',
  },
} as const;
```

> 💡 **自动化建议**：在 CI 中增加脚本，从字段映射表 JSON 自动生成 TypeScript 常量文件，杜绝手写 ID。

---

## 3. 联调流程

### 3.1 联调前准备

| 步骤 | 负责人 | 产出 |
|------|--------|------|
| 1. 接口文档确认 | 后端 | Swagger/OpenAPI 文档，含请求/响应示例 |
| 2. Mock Server 部署 | 前端 | 基于接口文档的 Mock 服务可访问 |
| 3. 联调环境就绪 | DevOps | 后端服务 + 简道云沙箱 + 前端预览地址 |
| 4. 测试账号准备 | BA | 各角色测试账号及密码 |
| 5. 字段映射表同步 | SA | 确认前后端使用的字段 ID 配置一致 |

### 3.2 联调执行

```
Day 1-2: 冒烟联调
  → 核心链路跑通（创建→审批→完成）
  → 发现阻塞性问题立即修复

Day 3-5: 全量联调
  → 按功能清单逐项验证
  → 每日站会同步进度和阻塞项
  → 问题录入 Issue Tracker，标注严重级别

Day 6: 回归验证
  → 修复项全部回归
  → 边界场景补充测试
  → 性能基线测试
```

### 3.3 联调问题分级

| 级别 | 定义 | 响应时效 | 示例 |
|------|------|---------|------|
| P0-阻塞 | 核心链路不通，无法继续联调 | 2小时内 | 登录失败、主接口500 |
| P1-严重 | 功能不可用但有临时绕过方案 | 当日 | 审批后状态未更新 |
| P2-一般 | 功能可用但体验差/数据不对 | 2日内 | 列表排序错误、文案错误 |
| P3-轻微 | 优化建议 | 排入迭代 | 按钮颜色不一致 |

---

## 4. G5 门禁检查清单

> ✅ 全部通过方可进入 Phase 6 测试与验收阶段

| # | 检查项 | 通过 | 责任人 | 备注 |
|---|--------|------|--------|------|
| 1 | 后端所有字段 ID 从配置文件读取，零硬编码 | ☐ | BE Lead | grep 扫描通过 |
| 2 | 所有 API 返回统一响应格式，错误码符合规范 | ☐ | BE Lead | |
| 3 | 异常分层捕获，无裸 except / 吞异常 | ☐ | BE Lead | Code Review |
| 4 | 多步写入操作已实现补偿回滚 + 失败告警 | ☐ | BE Lead | |
| 5 | 前端使用统一 API 客户端，无散落 fetch/axios | ☐ | FE Lead | grep 扫描通过 |
| 6 | 前端所有数据请求处理 loading/error/empty 三态 | ☐ | FE Lead | |
| 7 | 前端所有写入操作有确认弹窗 + 防重复提交 | ☐ | FE Lead | |
| 8 | 前端零硬编码 widget_id / field_id | ☐ | FE Lead | grep 扫描通过 |
| 9 | 联调问题 P0/P1 全部关闭，P2 关闭率 ≥ 90% | ☐ | QA | |
| 10 | 单元测试覆盖率 ≥ 70%（后端核心服务） | ☐ | BE Lead | |
| 11 | 接口文档与实际实现一致（Swagger 验证通过） | ☐ | QA | |
| 12 | 代码已通过 SonarQube / ESLint 扫描，无 Critical 问题 | ☐ | Tech Lead | |

---

*文档版本: v1.0 | 最后更新: YYYY-MM-DD | 作者: ___*
