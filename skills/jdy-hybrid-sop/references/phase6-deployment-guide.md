# Phase 6 · 部署与运维指南

---

## 1. Bridge 模式部署步骤

### 1.1 环境准备

```bash
# 系统依赖
sudo apt update && sudo apt install -y python3.12 python3.12-venv nginx

# 创建应用目录
sudo mkdir -p /opt/bridge-app
sudo chown www-data:www-data /opt/bridge-app
```

### 1.2 虚拟环境 + 依赖安装

```bash
cd /opt/bridge-app
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn
```

### 1.3 环境变量配置

```bash
cp .env.example .env
chmod 600 .env
# 编辑 .env 填入生产配置
```

### 1.4 Gunicorn 启动验证

```bash
# 手动测试
./venv/bin/gunicorn -c deploy/gunicorn.conf.py "app:app"

# 验证健康检查
curl http://127.0.0.1:5000/healthz
# 期望: {"status":"ok"}
```

### 1.5 Systemd 服务注册

```bash
sudo cp deploy/bridge.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bridge
sudo systemctl start bridge
sudo systemctl status bridge
```

### 1.6 Nginx 反向代理

```bash
sudo cp deploy/nginx_bridge.conf /etc/nginx/sites-available/bridge
sudo ln -s /etc/nginx/sites-available/bridge /etc/nginx/sites-enabled/
sudo nginx -t          # 语法检查
sudo systemctl reload nginx
```

### 1.7 部署验证

```bash
# 端到端验证
curl https://bridge.example.com/healthz
curl -H "Authorization: Bearer xxx" https://bridge.example.com/api/v1/orders
```

---

## 2. Standard 模式部署步骤（Docker Compose）

### 2.1 环境准备

```bash
# 安装 Docker + Compose
curl -fsSL https://get.docker.com | sh
sudo systemctl enable --now docker

# 克隆代码到服务器
git clone <repo> /opt/std-app && cd /opt/std-app
```

### 2.2 环境变量

```bash
cp deploy/.env.production.example deploy/.env.production
chmod 600 deploy/.env.production
# 编辑填入生产配置
```

### 2.3 构建并启动

```bash
docker compose -f deploy/docker-compose.yml up -d --build

# 查看状态
docker compose ps
docker compose logs -f --tail=100
```

### 2.4 部署验证

```bash
# 后端健康检查
curl http://localhost:8000/healthz

# 前端页面
curl -I http://localhost:80

# 完整链路
curl http://localhost/api/v1/orders
```

### 2.5 常用运维命令

```bash
# 重启单个服务
docker compose restart backend

# 查看实时日志
docker compose logs -f backend

# 更新部署
git pull && docker compose up -d --build

# 清理旧镜像
docker image prune -f
```

---

## 3. 全链路回归测试策略（6 步）

| 步骤 | 测试内容 | 方法 | 通过标准 |
|------|---------|------|---------|
| **T1** | 健康检查 | `GET /healthz` | 返回 200 + `{"status":"ok"}` |
| **T2** | 认证鉴权 | 无 Token 访问业务接口 | 返回 401/403 |
| **T3** | 读操作 | `GET /api/v1/orders?limit=5` | 返回正确数据结构，耗时 < 2s |
| **T4** | 写操作 | `POST /api/v1/orders` 创建测试数据 | 返回 201，简道云侧可查到新记录 |
| **T5** | 异常处理 | 传入非法参数 / 不存在的 ID | 返回结构化错误（非 500） |
| **T6** | 性能基线 | 并发 10 × 读接口 | P99 < 3s，无超时/报错 |

### 自动化脚本示例

```bash
#!/bin/bash
BASE_URL="${1:-https://bridge.example.com}"
FAIL=0

echo "=== T1: Health Check ==="
curl -sf "$BASE_URL/healthz" || { echo "FAIL"; FAIL=$((FAIL+1)); }

echo "=== T2: Auth Required ==="
STATUS=$(curl -so /dev/null -w "%{http_code}" "$BASE_URL/api/v1/orders")
[ "$STATUS" = "401" ] || [ "$STATUS" = "403" ] || { echo "FAIL: got $STATUS"; FAIL=$((FAIL+1)); }

echo "=== T3: Read Operation ==="
curl -sf -H "Authorization: Bearer $TOKEN" "$BASE_URL/api/v1/orders?limit=5" || { echo "FAIL"; FAIL=$((FAIL+1)); }

echo "=== T5: Error Handling ==="
STATUS=$(curl -so /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN" "$BASE_URL/api/v1/orders/invalid-id")
[ "$STATUS" != "500" ] || { echo "FAIL: got 500"; FAIL=$((FAIL+1)); }

echo "--- Result: $FAIL failures ---"
exit $FAIL
```

---

## 4. 常见问题排查

### 4.1 Gunicorn Worker 超时

**症状**：日志出现 `WORKER TIMEOUT (pid:xxx)` + 请求返回 502

**排查路径**：
1. 检查 `gunicorn.conf.py` 中 `timeout` 值（默认 30s 可能不够）
2. 确认简道云 API 响应时间：`curl -w "%{time_total}" <jdy_endpoint>`
3. 检查是否有同步阻塞操作（大文件、未设超时的 DB 查询）

**解决方案**：
```python
# gunicorn.conf.py
timeout = 120           # 根据实际 API 响应调整
graceful_timeout = 30   # worker 优雅退出等待
worker_class = "gthread"
threads = 2             # 避免纯 sync worker 被长请求占满
```

### 4.2 数据写入验证三步法

当写入简道云后需要确认数据一致性：

```
Step 1: 写入后立即 GET 该条记录 → 确认字段值匹配
Step 2: 登录简道云 Web 端人工核对 → 确认 UI 显示正确
Step 3: 等待 30s 后再次 GET → 确认触发器/流程引擎未篡改数据
```

> ⚠️ 简道云触发器和智能引擎可能异步修改刚写入的数据，Step 3 不可省略。

### 4.3 API 常见陷阱

| 陷阱 | 表现 | 解决 |
|------|------|------|
| 分页遗漏 | 只拿到前 100 条 | 使用 `data_id` 游标循环拉取，或设置 `limit=100` 触发自动分页 |
| 字段名大小写 | 写入成功但字段为空 | 简道云字段名区分大小写，以表单设计器为准 |
| 日期格式 | 400 Bad Request | 统一使用 ISO 8601：`2026-06-13T10:30:00+08:00` |
| 多选字段 | 写入覆盖而非追加 | 多选字段值为数组，需先 GET 再合并 |
| 子表单 | 嵌套结构报错 | 子表单值为 `[{field1: val, field2: val}]` 数组格式 |
| Token 过期 | 间歇性 401 | 实现 Token 刷新机制，不要硬编码长期 Token |

---

## 5. 运维手册模板

```markdown
# [项目名称] 运维手册

## 基本信息
- 部署模式: Bridge / Standard
- 服务器: IP / 域名
- 简道云应用: AppID / 表单列表
- 负责人: 姓名 / 联系方式

## 服务启停
### Bridge 模式
- 启动: sudo systemctl start bridge
- 停止: sudo systemctl stop bridge
- 重启: sudo systemctl restart bridge
- 日志: journalctl -u bridge -f

### Standard 模式
- 启动: docker compose up -d
- 停止: docker compose down
- 重启: docker compose restart
- 日志: docker compose logs -f

## 监控告警
- 健康检查: /healthz (每 30s)
- 告警渠道: 企微/钉钉/邮件
- 关键指标: 响应时间 P99、错误率、Worker 数

## 变更流程
1. 提交 MR → Code Review → 合并 main
2. 在 staging 环境验证
3. 执行全链路回归测试（6步）
4. 生产发布 + 观察 15min
5. 记录变更日志

## 应急回滚
- Bridge: git checkout <tag> && systemctl restart bridge
- Standard: docker compose down && git checkout <tag> && docker compose up -d --build

## 联系升级
- L1: 值班工程师
- L2: 项目负责人
- L3: 简道云技术支持
```

---

## 6. G6 门禁检查清单

| # | 检查项 | 通过标准 | 验证方式 |
|---|--------|---------|---------|
| 1 | 部署文档完整 | 包含完整部署步骤 + 验证命令 | 文档审查 |
| 2 | 健康检查可用 | `/healthz` 在生产环境返回 200 | `curl` 验证 |
| 3 | 全链路回归通过 | 6 步测试全部 PASS | 自动化脚本 |
| 4 | 日志可观测 | systemd journal / docker logs 正常输出 | 日志检查 |
| 5 | 环境变量安全 | `.env` 权限 600，不入版本控制 | `ls -la .env` + `.gitignore` |
| 6 | 进程守护 | systemd `Restart=always` 或 compose `restart: always` | 配置审查 |
| 7 | Nginx 超时匹配 | proxy_read_timeout ≥ gunicorn timeout | 配置对比 |
| 8 | 运维手册就绪 | 包含启停/监控/变更/回滚/升级流程 | 文档审查 |
| 9 | 数据写入验证 | 三步法已执行并记录结果 | 测试报告 |
| 10 | 回滚方案验证 | 在 staging 实际执行过一次回滚 | 演练记录 |
