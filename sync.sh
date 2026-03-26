#!/bin/bash
# 三方去中心化同步脚本

REPO_DIR="/root/.openclaw/workspace/ai-marine-sync"
LOG="/root/.openclaw/workspace/shared/audit.log"

cd $REPO

hostname=$(hostname)
echo "[$(date +%Y-%m-%d\ %H:%M:%S)] [AHAI] 开始同步" >> $LOG

# 拉取最新
git pull origin master >> $LOG 2>&1

# 复制本地知识库到同步目录
cp -r /root/.openclaw/workspace/knowledge/marine-aquarium/* $REPO/knowledge/ 2>/dev/null

# 如果有变更，推送
if [[ -n $(git status --porcelain) ]]; then
    git add -A
    git commit -m "auto: ahei $(date +%Y-%m-%d\ %H:%M)" >> $LOG 2>&1
    git push origin master >> $LOG 2>&1
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] [AHAI] 推送完成" >> $LOG
fi

echo "[$(date +%Y-%m-%d\ %H:%M:%S)] [AHAI] 同步结束" >> $LOG
