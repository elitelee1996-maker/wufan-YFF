# Phase 4 · Standard 模式工程脚手架

> Standard 模式采用 **backend / frontend 完全分离**架构，后端 FastAPI + 前端 React，通过 Docker Compose 统一编排部署。

---

## 1. Backend / Frontend 分离目录结构

```
project-root/
├── backend/
│   ├── main.py               # FastAPI 入口
│   ├── config.py             # Pydantic Settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── order.py          # Pydantic Request/Response 模型
│   │   └── common.py         # 通用响应包装
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── order_router.py
│   │   └── inventory_router.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── jdy_client.py     # JDYClient 封装
│   ├── tests/
│   ├── alembic/              # 数据库迁移（如需本地库）
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/            # 页面组件（按路由拆分）
│   │   │   ├── OrderList.tsx
│   │   │   └── OrderDetail.tsx
│   │   ├── components/       # 可复用 UI 组件
│   │   ├── services/         # API 调用层
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
├── deploy/
│   ├── docker-compose.yml
│   ├── nginx.conf            # 前端静态资源 + API 反代
│   └── .env.production
├── Makefile                  # 常用命令快捷入口
└── README.md
```

---

## 2. FastAPI main.py 模板

```python
"""Standard 模式后端入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from services.jdy_client import init_jdy_client

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- 初始化外部服务 ----------
@app.on_event("startup")
async def startup():
    init_jdy_client(settings)

# ---------- 注册路由 ----------
from routers.order_router import router as order_router
from routers.inventory_router import router as inventory_router

app.include_router(order_router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(inventory_router, prefix="/api/v1/inventory", tags=["Inventory"])

# ---------- 健康检查 ----------
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
```

---

## 3. Pydantic 模型规范

### 3.1 请求模型

```python
# models/order.py
from pydantic import BaseModel, Field
from datetime import date


class CreateOrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100, description="客户名称")
    product_id: str = Field(..., description="产品ID")
    quantity: int = Field(..., gt=0, description="数量")
    expected_date: date = Field(..., description="期望交付日期")

    model_config = {"json_schema_extra": {"examples": [
        {"customer_name": "张三", "product_id": "P001", "quantity": 10, "expected_date": "2026-07-01"}
    ]}}
```

### 3.2 响应模型

```python
class OrderResponse(BaseModel):
    id: str
    customer_name: str
    status: str
    created_at: str


class ApiResponse(BaseModel):
    """统一响应包装"""
    code: int = 0
    message: str = "success"
    data: dict | list | None = None
```

### 3.3 规范要求

| 规则 | 说明 |
|------|------|
| 命名 | Request 后缀 `Request`，Response 后缀 `Response` |
| 字段描述 | 所有字段必须有 `Field(description=...)` |
| 校验 | 字符串设 `min/max_length`，数值设 `gt/lt/ge/le` |
| 示例 | 至少提供一个 `json_schema_extra.examples` |
| 禁止 | 不使用 `Optional` 代替默认值；不用裸 `dict` 作响应 |

---

## 4. React 页面组件规范

### 4.1 页面组件模板

```tsx
// pages/OrderList.tsx
import { useEffect, useState } from 'react';
import { fetchOrders, Order } from '../services/api';

export default function OrderList() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOrders()
      .then(setOrders)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>加载中...</div>;

  return (
    <div className="order-list">
      <h1>订单列表</h1>
      <table>
        <thead>
          <tr><th>客户</th><th>状态</th><th>创建时间</th></tr>
        </thead>
        <tbody>
          {orders.map(o => (
            <tr key={o.id}>
              <td>{o.customer_name}</td>
              <td>{o.status}</td>
              <td>{o.created_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

### 4.2 规范要求

| 规则 | 说明 |
|------|------|
| 文件命名 | PascalCase，与路由名一致 |
| 组件类型 | 页面用 `default export`，子组件用 `named export` |
| 状态管理 | 局部状态用 `useState`，全局用 Zustand/Context |
| API 调用 | 统一走 `services/api.ts`，禁止组件内直接 fetch |
| TypeScript | 所有 props/state 必须定义 interface/type |
| 错误处理 | API 调用必须有 catch/loading 状态 |

---

## 5. docker-compose.yml 模板

```yaml
version: "3.9"

services:
  backend:
    build: ./backend
    container_name: std-backend
    restart: always
    env_file: ./deploy/.env.production
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/healthz"]
      interval: 30s
      timeout: 5s
      retries: 3

  frontend:
    build: ./frontend
    container_name: std-frontend
    restart: always
    depends_on:
      backend:
        condition: service_healthy
    volumes:
      - ./deploy/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    ports:
      - "80:80"
```

### Backend Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Frontend Dockerfile

```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

---

## 6. nginx.conf 模板

```nginx
server {
    listen 80;
    server_name _;

    # 前端静态资源
    root /usr/share/nginx/html;
    index index.html;

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API 反向代理
    location /api/ {
        proxy_pass http://std-backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 120s;
    }

    # 健康检查（不走日志）
    location /healthz {
        proxy_pass http://std-backend:8000/healthz;
        access_log off;
    }

    # 缓存静态资源
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2?)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 7. G4 门禁检查清单

| # | 检查项 | 通过标准 | 验证方式 |
|---|--------|---------|---------|
| 1 | 前后端分离 | backend/ 和 frontend/ 独立目录 | 目录审查 |
| 2 | FastAPI 入口规范 | main.py 仅做路由注册+中间件 | Code Review |
| 3 | Pydantic 模型完整 | 所有接口有 Request/Response 模型 | `grep -r "BaseModel" backend/models/` |
| 4 | 模型字段校验 | 无裸 dict 响应，字段有 Field 描述 | Code Review |
| 5 | React TS 严格 | 无 `any` 类型，组件有 type 定义 | `tsc --noEmit` |
| 6 | API 调用集中 | 组件内无直接 fetch/axios | `grep -r "fetch\|axios" frontend/src/pages/` |
| 7 | Docker Compose 可构建 | `docker compose build` 成功 | CI 验证 |
| 8 | Nginx 配置完整 | SPA fallback + API 反代 + 缓存 | 配置审查 |
| 9 | 健康检查 | 后端 `/healthz` + compose healthcheck | `curl` + `docker inspect` |
| 10 | .env.example 齐全 | 前后端均有环境变量模板 | 文件检查 |
