#!/bin/bash
# OKR Bridge 重启脚本
set -e

echo ">>> 停止旧进程..."
ps aux | grep 'gunicorn.*okr' | grep -v grep | awk '{print $2}' | xargs -r kill 2>/dev/null || true
sleep 1

echo ">>> 启动服务..."
cd ~/apps/okr-bridge
source venv/bin/activate
set -a && source .env && set +a
nohup gunicorn -w 2 -b 0.0.0.0:8200 --timeout 120 app:app > ~/logs/okr-bridge.log 2>&1 &
sleep 2

echo ">>> 健康检查..."
curl -s http://localhost:8200/health
echo ""
echo ">>> 重启完成"
