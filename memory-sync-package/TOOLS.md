# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## 🌐 Agent Browser

已安装：`agent-browser@0.21.4`

**用途：** 无头浏览器自动化，用于网页抓取、截图、自动化操作

**常用命令：**
```bash
# 基础操作
npx agent-browser open https://example.com
npx agent-browser snapshot              # 获取页面结构
npx agent-browser screenshot ./img.png  # 截图

# 交互操作
npx agent-browser click "button"
npx agent-browser type "input" "hello"
npx agent-browser press Enter
```

**备注：** 全局可用，无需额外配置

---

## 📚 Ship-Learn-Next Skill

已安装：`~/.openclaw/skills/ship-learn-next/`

**用途：** 将学习内容（视频、文章、教程）转化为可执行的行动计划

**框架：** Ship → Learn → Next 循环
- **SHIP** - 创建实际产出（代码、内容、产品）
- **LEARN** - 诚实反思发生了什么
- **NEXT** - 基于学习规划下一次迭代

**使用场景：**
- 看完教程后想付诸实践
- 把建议转化为具体行动步骤
- 将大目标拆解为可迭代的小任务

**原理：** 100次实践 > 100小时理论学习
