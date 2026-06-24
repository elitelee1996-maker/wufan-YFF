#!/usr/bin/env bash
# Bridge模式部署脚本模板
# 用法: ./deploy.sh <项目名称> [端口]
set -euo pipefail

PROJECT_NAME="${1:?用法: $0 <项目名称> [端口]}"
PORT="${2:-5000}"
DEPLOY_DIR="/opt/${PROJECT_NAME}"
VENV_DIR="${DEPLOY_DIR}/venv"
SERVICE_NAME="${PROJECT_NAME}-bridge"
HEALTH_URL="http://127.0.0.1:${PORT}/health"

echo "==> 部署 ${PROJECT_NAME} (Bridge模式, 端口 ${PORT})"

# 1. 创建目录
echo "[1/7] 创建部署目录..."
mkdir -p "${DEPLOY_DIR}"/{static,logs}

# 2. 创建虚拟环境
echo "[2/7] 创建 Python 虚拟环境..."
python3 -m venv "${VENV_DIR}"

# 3. 安装依赖
echo "[3/7] 安装依赖..."
"${VENV_DIR}/bin/pip" install --upgrade pip -q
if [ -f requirements.txt ]; then
    "${VENV_DIR}/bin/pip" install -r requirements.txt -q
else
    "${VENV_DIR}/bin/pip" install flask requests gunicorn -q
fi

# 4. 复制代码
echo "[4/7] 复制应用代码..."
cp -f app_bridge.py jdy_client.py field_mapper.py "${DEPLOY_DIR}/"
[ -d static ] && cp -rf static/* "${DEPLOY_DIR}/static/" || true
[ -f field_mapping.json ] && cp -f field_mapping.json "${DEPLOY_DIR}/" || true

# 5. 配置 systemd
echo "[5/7] 配置 systemd 服务..."
sudo tee "/etc/systemd/system/${SERVICE_NAME}.service" > /dev/null <<EOF
[Unit]
Description=${PROJECT_NAME} Bridge Service
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=${DEPLOY_DIR}
Environment=PORT=${PORT}
Environment=JDY_API_KEY=\${JDY_API_KEY}
ExecStart=${VENV_DIR}/bin/gunicorn -w 2 -b 0.0.0.0:${PORT} app_bridge:app
Restart=always
RestartSec=5
StandardOutput=append:${DEPLOY_DIR}/logs/stdout.log
StandardError=append:${DEPLOY_DIR}/logs/stderr.log

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload

# 6. 启动服务
echo "[6/7] 启动服务..."
sudo systemctl enable "${SERVICE_NAME}"
sudo systemctl restart "${SERVICE_NAME}"

# 7. 健康检查
echo "[7/7] 健康检查..."
for i in $(seq 1 10); do
    if curl -sf "${HEALTH_URL}" > /dev/null 2>&1; then
        echo "✅ ${PROJECT_NAME} 部署成功! 健康检查通过 (${HEALTH_URL})"
        exit 0
    fi
    sleep 2
done

echo "❌ 健康检查失败，请查看日志: journalctl -u ${SERVICE_NAME} -n 50"
exit 1
