# 记忆系统同步包

## 文件清单

### 核心文件
- `MEMORY.md` - 长期记忆
- `AGENTS.md` - 工作流程定义
- `SOUL.md` - 人格定义（需要修改为自己的身份）
- `USER.md` - 用户档案
- `IDENTITY.md` - 身份定义（需要修改）
- `TOOLS.md` - 工具配置

### 脚本
- `memory-guard.sh` - 记忆保护脚本
- `broadcast_command.py` - 命令广播系统
- `install.sh` - 安装脚本

### 目录
- `memory/` - 每日记忆
- `.learnings/` - 学习记录

## 安装方法

```bash
cd memory-sync-package
./install.sh
```

## 安装后必做

1. 修改 `IDENTITY.md` - 改为自己的名字和身份
   - 阿海: name="阿海", emoji=🤖, role=COO
   - 小北: name="小北", emoji=🐻, role=CMO

2. 修改 `SOUL.md` - 调整人格描述

3. 启动广播客户端（如果需要群聊）：
   ```bash
   python3 ~/openclaw/workspace/scripts/broadcast_command.py &
   ```

## 记忆保护机制

- 每小时自动备份核心文件
- 保留最近7天备份
- 日志位置: `memory/backup/guard.log`
