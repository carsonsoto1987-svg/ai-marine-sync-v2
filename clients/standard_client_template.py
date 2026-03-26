#!/usr/bin/env python3
"""
AI三人组 - 标准客户端模板
适用: 东东、阿海、小北

使用方法:
1. 修改 NODE_ID 和 NODE_NAME
2. 运行: python3 standard_client.py
3. 保持后台运行

标准格式输出:
[HH:MM] 节点ID - 在线|任务数|知识库数|消息数
"""
import asyncio
import websockets
import json
import time
from datetime import datetime

# ==================== 修改这里 ====================
NODE_ID = "your_id"      # 改为: dongdong / ahai / xiaobei
NODE_NAME = "你的名字"    # 改为: 东东 / 阿海 / 小北
# =================================================

SERVER = "ws://150.158.28.54:8765"

async def main():
    print(f"🚀 {NODE_NAME}标准客户端启动")
    print(f"节点ID: {NODE_ID}")
    
    while True:
        try:
            async with websockets.connect(SERVER) as ws:
                # 注册
                await ws.send(json.dumps({
                    "type": "register",
                    "node_id": NODE_ID,
                    "name": NODE_NAME
                }))
                print(f"✅ 已连接")
                
                # 发送首次状态
                await send_status(ws, "首次连接")
                
                # 监听消息
                async for raw in ws:
                    try:
                        data = json.loads(raw)
                        sender = data.get("from")
                        content = data.get("content", "").lower()
                        
                        if sender == NODE_ID:
                            continue
                        
                        # 握手
                        if content == "hhh":
                            await ws.send(json.dumps({
                                "type": "chat",
                                "from": NODE_ID,
                                "content": "GGG"
                            }))
                        
                        # 状态检查
                        elif "ping" in content or "状态" in content:
                            await send_status(ws, "状态响应")
                            
                    except:
                        pass
                        
        except Exception as e:
            print(f"断开: {e}, 5秒后重连...")
            await asyncio.sleep(5)

async def send_status(ws, reason=""):
    """发送标准格式状态"""
    now = datetime.now().strftime('%H:%M')
    
    # 获取实际数据（这里用示例）
    tasks = 0
    kb = 0
    msgs = 0
    
    # 标准格式！
    status = f"[{now}] {NODE_ID} - 在线|{tasks}|{kb}|{msgs}"
    if reason:
        status += f" ({reason})"
    
    await ws.send(json.dumps({
        "type": "chat",
        "from": NODE_ID,
        "content": status
    }))
    
    print(f"📤 {status}")

if __name__ == "__main__":
    asyncio.run(main())
