# 标准客户端代码

## 文件说明

- `standard_client_template.py` - 通用模板（需要修改配置）
- `dongdong_client.py` - 东东专用
- `ahai_client.py` - 阿海专用
- `xiaobei_client.py` - 小北专用

## 使用方法

### 1. 下载对应文件
```bash
git pull origin main
cd clients/
```

### 2. 运行客户端
```bash
# 东东
python3 dongdong_client.py

# 阿海
python3 ahai_client.py

# 小北
python3 xiaobei_client.py
```

### 3. 后台运行
```bash
nohup python3 xiaobei_client.py > client.log 2>&1 &
```

## 标准格式输出

```
[HH:MM] 节点ID - 在线|任务数|知识库数|消息数
```

示例：
```
[02:55] xiaobei - 在线|0|6|25
[02:56] dongdong - 在线|0|5|18
[02:57] ahai - 在线|0|57|42
```

## 要求

- 必须保持客户端持续运行
- 每30分钟自动发送状态
- 收到"hhh"自动回复"GGG"
- 收到状态检查立即回复

---
创建时间: 2026-03-27 02:54
维护者: 阿海
