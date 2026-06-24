# Phase 4 · Bridge 模式工程脚手架

> **三大核心原则**
> 1. `app.py` **只做路由注册**，禁止写业务逻辑
> 2. `JDYClient` 是简道云 API 的**唯一出口**，禁止散落的 requests 调用
> 3. **配置驱动**：所有环境差异通过 `config/settings.py` + `.env` 管理

---

## 1. 完整目录结构

```
project-root/
├── app.py                    # Flask/FastAPI 入口（≤200行，仅路由注册）
├── config/
│   ├── __init__.py
│   └── settings.py           # Pydantic Settings / dataclass 配置
├── services/
│   ├── __init__.py
│   └── jdy_client.py         # JDYClient 单例封装
├── api/
│   ├── __init__.py
│   ├── order_api.py          # 蓝图/Router：订单模块
│   ├── inventory_api.py      # 蓝图/Router：库存模块
│   └── ...                   # 按业务域拆分
├── models/                   # ORM / 数据模型（可选）
├── utils/                    # 通用工具函数
├── tests/
│   ├── test_jdy_client.py
│   └── test_order_api.py
├── deploy/
│   ├── gunicorn.conf.py
│   ├── bridge.service        # systemd unit
│   └── nginx_bridge.conf     # Nginx 反向代理
├── .env                      # 环境变量（不入版本控制）
├── .env.example              # 环境变量模板
├── requirements.txt
└── README.md
```

---

## 2. app.py 模板（≤200 行）

```python
"""Bridge 模式应用入口 —— 仅负责路由注册与中间件挂载"""
from flask import Flask
from config.settings import get_settings
from services.jdy_client import init_jdy_client


def create_app() -> Flask:
    app = Flask(__name__)
    settings = get_settings()

    # ---------- 基础配置 ----------
    app.config.update(
        SECRET_KEY=settings.secret_key,
        JSON_AS_ASCII=False,
    )

    # ---------- 初始化外部服务 ----------
    init_jdy_client(settings)

    # ---------- 注册蓝图（每个业务域一个文件） ----------
    from api.order_api import bp as order_bp
    from api.inventory_api import bp as inventory_bp

    app.register_blueprint(order_bp, url_prefix="/api/v1/orders")
    app.register_blueprint(inventory_bp, url_prefix="/api/v1/inventory")

    # ---------- 健康检查 ----------
    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

> ⚠️ **门禁**：`app.py` 超过 200 行或包含业务逻辑 → G4 不通过。

---

## 3. config/settings.py 模板

```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """所有配置项均从环境变量 / .env 读取"""
    # --- 应用 ---
    secret_key: str = "change-me"
    debug: bool = False

    # --- 简道云 ---
    jdy_api_key: str
    jdy_base_url: str = "https://api.jiandaoyun.com/api/v5"
    jdy_timeout: int = 30

    # --- 数据库（如有） ---
    database_url: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

---

## 4. services/jdy_client.py 接口清单

```python
"""JDYClient —— 简道云 API 唯一出口"""
import httpx
from config.settings import Settings

_client: httpx.Client | None = None


def init_jdy_client(settings: Settings):
    global _client
    _client = httpx.Client(
        base_url=settings.jdy_base_url,
        headers={"Authorization": f"Bearer {settings.jdy_api_key}"},
        timeout=settings.jdy_timeout,
    )


def _get() -> httpx.Client:
    if _client is None:
        raise RuntimeError("JDYClient not initialized. Call init_jdy_client() first.")
    return _client


# ---- 标准 CRUD 封装 ----
def list_data(form_id: str, filter_cond: dict | None = None,
              fields: list[str] | None = None, limit: int = 100) -> list[dict]:
    """查询表单数据列表"""
    ...

def get_data(form_id: str, data_id: str) -> dict:
    """获取单条记录"""
    ...

def create_data(form_id: str, data: dict) -> dict:
    """新增记录"""
    ...

def update_data(form_id: str, data_id: str, data: dict) -> dict:
    """更新记录"""
    ...

def delete_data(form_id: str, data_id: str) -> None:
    """删除记录"""
    ...

def search_data(form_id: str, keyword: str, fields: list[str]) -> list[dict]:
    """关键词搜索"""
    ...
```

> ⚠️ **门禁**：项目中出现 `requests.get/post` 直接调用简道云 URL → G4 不通过。

---

## 5. api/{module}_api.py 蓝图模板

```python
"""订单模块 API 蓝图"""
from flask import Blueprint, request, jsonify
from services import jdy_client

bp = Blueprint("orders", __name__)

FORM_ID = "64a1b2c3d4e5f60001234567"  # 建议移到 settings 或常量文件


@bp.get("/")
def list_orders():
    filters = request.args.to_dict()
    data = jdy_client.list_data(FORM_ID, filter_cond=filters)
    return jsonify(data=data)


@bp.post("/")
def create_order():
    payload = request.get_json(force=True)
    result = jdy_client.create_data(FORM_ID, payload)
    return jsonify(result), 201


@bp.put("/<data_id>")
def update_order(data_id: str):
    payload = request.get_json(force=True)
    result = jdy_client.update_data(FORM_ID, data_id, payload)
    return jsonify(result)
```

---

## 6. systemd 服务配置

```ini
# deploy/bridge.service
[Unit]
Description=Bridge Mode Application
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/bridge-app
EnvironmentFile=/opt/bridge-app/.env
ExecStart=/opt/bridge-app/venv/bin/gunicorn \
    -c deploy/gunicorn.conf.py \
    "app:app"
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### gunicorn.conf.py

```python
bind = "127.0.0.1:5000"
workers = 4
worker_class = "gthread"
threads = 2
timeout = 120
graceful_timeout = 30
accesslog = "-"
errorlog = "-"
```

---

## 7. Nginx 反向代理配置

```nginx
# deploy/nginx_bridge.conf
upstream bridge_backend {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name bridge.example.com;

    location / {
        proxy_pass http://bridge_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 120s;
        proxy_send_timeout 120s;
    }

    location /healthz {
        proxy_pass http://bridge_backend/healthz;
        access_log off;
    }
}
```

---

## 8. G4 门禁检查清单

| # | 检查项 | 通过标准 | 验证方式 |
|---|--------|---------|---------|
| 1 | app.py 行数 | ≤ 200 行 | `wc -l app.py` |
| 2 | app.py 无业务逻辑 | 不含 DB 查询/数据处理代码 | Code Review |
| 3 | JDYClient 唯一出口 | 全项目无散落 requests 调用简道云 | `grep -r "requests\." --include="*.py" \| grep -v jdy_client` |
| 4 | 配置驱动 | 无硬编码 URL/Key/密码 | `grep -rn "api.jiandaoyun\|Bearer " --include="*.py"` |
| 5 | 蓝图按业务域拆分 | api/ 下每个文件对应一个业务域 | 目录审查 |
| 6 | .env.example 存在 | 包含所有必需环境变量说明 | 文件检查 |
| 7 | 健康检查端点 | `/healthz` 返回 200 | `curl localhost:5000/healthz` |
| 8 | systemd + nginx 配置就绪 | deploy/ 下文件完整 | 文件检查 |
