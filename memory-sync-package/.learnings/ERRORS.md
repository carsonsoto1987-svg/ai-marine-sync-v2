# ERRORS.md - 错误日志

**用途：** 记录执行过程中的错误和失败  
**维护者：** 东东 🐱  
**审查周期：** 每周日

---

## 错误记录格式

```markdown
## [ERR-YYYYMMDD-XXX] 错误类型

**记录时间：** ISO-8601 时间戳  
**优先级：** critical | high | medium | low  
**状态：** pending | in_progress | resolved | wont_fix  
**领域：** frontend | backend | infra | tools | knowledge | behavior

### 摘要
一句话描述错误

### 错误详情
```
错误信息或输出
```

### 上下文
- 执行的命令/操作
- 输入参数
- 环境信息

### 建议修复
如何解决这个问题

### 元数据
- 可复现性：yes | no | unknown
- 相关文件：路径
- 关联记录：ERR-YYYYMMDD-XXX

---
```

---

## 待处理错误

*暂无记录*

---

## 已解决错误

*暂无记录*

---

*最后更新：2026-03-25*
