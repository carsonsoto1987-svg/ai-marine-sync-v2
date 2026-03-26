#!/bin/bash
# 记忆系统安装脚本 - 阿海/小北使用

WORKSPACE="$HOME/.openclaw/workspace"

echo "=== 安装记忆系统 ==="

# 创建目录
mkdir -p "$WORKSPACE/scripts"
mkdir -p "$WORKSPACE/memory/backup"
mkdir -p "$WORKSPACE/.learnings"
mkdir -p "$WORKSPACE/logs"

# 复制核心文件
cp MEMORY.md AGENTS.md SOUL.md USER.md IDENTITY.md TOOLS.md "$WORKSPACE/" 2>/dev/null || true

# 复制脚本
cp memory-guard.sh "$WORKSPACE/scripts/" 2>/dev/null || chmod +x "$WORKSPACE/scripts/memory-guard.sh"

# 复制记忆目录
cp -r memory/* "$WORKSPACE/memory/" 2>/dev/null || true
cp -r .learnings/* "$WORKSPACE/.learnings/" 2>/dev/null || true

# 设置cron任务
(crontab -l 2>/dev/null | grep -v "memory-guard.sh"; echo "0 * * * * $WORKSPACE/scripts/memory-guard.sh >> $WORKSPACE/memory/backup/guard.log 2>&1") | crontab -

echo "✅ 记忆系统安装完成"
echo "⚠️ 请根据身份修改 IDENTITY.md 和 SOUL.md"
