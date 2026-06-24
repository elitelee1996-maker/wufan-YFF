#!/bin/bash
# OKR Bridge 部署脚本
set -e

echo "=== OKR Bridge 部署开始 ==="

# 创建目录
mkdir -p /home/deploy/apps/okr-bridge
cd /home/deploy/apps/okr-bridge

# 创建虚拟环境
echo ">>> 创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装依赖
echo ">>> 安装依赖..."
pip install --upgrade pip
pip install flask==2.0.3 flask-cors==3.0.10 requests==2.27.1 gunicorn==20.1.0

# 启动服务
echo ">>> 启动服务..."
nohup gunicorn -w 2 -b 0.0.0.0:8200 app:app > /home/deploy/logs/okr-bridge.log 2>&1 &

echo "=== 部署完成 ==="
echo "服务地址: http://47.98.192.245:8200"
echo "健康检查: curl http://47.98.192.245:8200/health"
