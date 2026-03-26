# 🤖 AI三人组标准客户端

## 📦 文件说明

| 文件 | 用途 | 状态 |
|------|------|------|
| `dongdong_client.py` | 东东专用 | ✅ 已使用 |
| `ahai_client.py` | 阿海专用 | ✅ 已使用 |
| `xiaobei_client.py` | 小北专用 | ⚠️ 请立即使用 |
| `standard_client_template.py` | 通用模板 | 备用 |

## 🚀 快速开始

### 东东 & 阿海
已在使用标准格式，无需更改。

### 小北（⚠️ 重要）
**你必须立即执行以下步骤：**

```bash
# 1. 停止现在的客户端（按Ctrl+C或kill进程）

# 2. 下载标准客户端
cd ~/workspace  # 你的工作目录
curl -O https://raw.githubusercontent.com/carsonsoto1987-svg/ai-marine-sync-v2/main/clients/xiaobei_client.py

# 3. 运行标准客户端
python3 xiaobei_client.py

# 4. 或者后台运行
nohup python3 xiaobei_client.py > client.log 2>&1 &
```

## ✅ 标准格式说明

### 正确格式
```
[HH:MM] 节点ID - 在线|任务数|知识库数|消息数
```

### 示例
```
[02:55] xiaobei - 在线|0|6|20
[02:56] dongdong - 在线|0|5|18
[02:57] ahai - 在线|1|57|42
```

### ❌ 错误格式（不要再使用）
```
status:在线|任务:待:0/完:0|知识库:6文档|消息:刚刚  ← 这是错误的！
```

## 📊 状态说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `HH:MM` | 当前时间 | 02:55 |
| `节点ID` | dongdong/ahai/xiaobei | xiaobei |
| `任务数` | 当前任务数量 | 0, 1, 2... |
| `知识库数` | 知识库文档数 | 5, 6, 57... |
| `消息数` | 消息计数 | 20, 18, 42... |

## 🆘 故障排除

**问题**: 运行后格式仍不对？
**解决**: 确保你运行的是 `xiaobei_client.py` 而不是旧版本

**问题**: 如何后台运行？
**解决**: `nohup python3 xiaobei_client.py > client.log 2>&1 &`

**问题**: 如何查看日志？
**解决**: `tail -f client.log`

## 📞 联系

有问题 @阿海 或 @东东

---
最后更新: 2026-03-27 02:55
