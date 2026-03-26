#!/bin/bash
# 记忆保护守护脚本
# 每小时执行：检查并备份关键记忆文件

WORKSPACE="/Users/carson/.openclaw/workspace"
BACKUP_DIR="$WORKSPACE/memory/backup"
LOG_FILE="$WORKSPACE/memory/heartbeat-state.json"

# 关键文件列表
CRITICAL_FILES=(
    "MEMORY.md"
    "USER.md"
    "AGENTS.md"
    "SOUL.md"
    "IDENTITY.md"
    "TOOLS.md"
)

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份关键文件
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$WORKSPACE/$file" ]; then
        cp "$WORKSPACE/$file" "$BACKUP_DIR/${file}.$TIMESTAMP.bak"
    fi
done

# 更新心跳状态
if [ -f "$LOG_FILE" ]; then
    # 使用临时文件更新JSON
    TMP_FILE=$(mktemp)
    cat "$LOG_FILE" | sed "s/\"memory\": [0-9]*/\"memory\": $(date +%s)/" > "$TMP_FILE"
    mv "$TMP_FILE" "$LOG_FILE"
fi

# 保留最近7天的备份，删除旧备份
find "$BACKUP_DIR" -name "*.bak" -mtime +7 -delete

echo "$(date '+%Y-%m-%d %H:%M:%S') 记忆保护检查完成"
