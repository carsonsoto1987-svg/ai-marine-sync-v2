#!/bin/bash
# 检查系统状态
CPU_THRESHOLD=80
MEMORY_THRESHOLD=90
DISK_THRESHOLD=95

ALERT_THRESHOLD=90

# 检查服务
services=("websocket", "http_sync", "http_relay", "database")
for service in "${services[@]}"; do
    case $service in
        "websocket")
            # 检查端口和进程
            systemctl is-active --quiet openclaw-gateway || echo "❌ WebSocket服务异常"
            ;;
        ;;
        "http_sync")
            # 检查HTTP服务
            curl -s -o /dev/null http://127.0.0.1:14427/health || echo "❌ HTTP同步服务异常"
            ;;
        ;;
        "http_relay")
            # 检查HTTP中继服务
            curl -s -o /dev/null http://127.0.0.1:14429/health || echo "❌ HTTP中继服务异常"
            ;;
        ;;
        "database")
            # 检查数据库连接
            sudo -u postgres psql -d marine_species -c "SELECT 1" || echo "❌ 数据库服务异常"
            ;;
    esac
done

