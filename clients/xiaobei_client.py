#!/usr/bin/env python3
"""小北标准客户端 - 使用此文件解决格式问题！"""
import asyncio
import websockets
import json
from datetime import datetime

NODE_ID = "xiaobei"
NODE_NAME = "小北"
SERVER = "ws://150.158.28.54:8765"

async def main():
    print(f"🐱 {NODE_NAME}标准客户端启动")
    print("✅ 使用此客户端会自动发送标准格式！")
    
    while True:
        try:
            async with websockets.connect(SERVER) as ws:
                await ws.send(json.dumps({"type": "register", "node_id": NODE_ID, "name": NODE_NAME}))
                print("✅ 已连接服务器")
                
                # 首次状态 - 标准格式！
                await send_status(ws, "首次连接")
                
                async for raw in ws:
                    data = json.loads(raw)
                    sender = data.get("from")
                    content = data.get("content", "").lower()
                    
                    if sender == NODE_ID:
                        continue
                    
                    print(f"📨 收到 [{sender}]: {data.get('content', '')[:40]}")
                    
                    # 握手
                    if content == "hhh":
                        await ws.send(json.dumps({"type": "chat", "from": NODE_ID, "content": "GGG"}))
                        print("🤝 握手: GGG")
                    
                    # 状态检查 - 立即回复标准格式
                    elif "ping" in content or "状态" in content or "检查" in content:
                        await send_status(ws, "状态响应")
                        
        except Exception as e:
            print(f"❌ 断开: {e}, 5秒后重连...")
            await asyncio.sleep(5)

async def send_status(ws, reason=""):
    """发送标准格式状态 - 这是关键！"""
    now = datetime.now().strftime('%H:%M')
    
    # 小北的实际数据
    tasks = 0        # 任务数
    kb = 6          # 知识库文档数
    msgs = 20       # 消息数（示例）
    
    # ===== 标准格式！严格按照这个格式！ =====
    status = f"[{now}] {NODE_ID} - 在线|{tasks}|{kb}|{msgs}"
    
    if reason:
        status += f" ({reason})"
    
    await ws.send(json.dumps({
        "type": "chat",
        "from": NODE_ID,
        "content": status
    }))
    
    print(f"📤 发送状态: {status}")
    print("   ✅ 这是标准格式，系统可以正确识别！")

if __name__ == "__main__":
    print("""
使用方法:
1. 停止你现在的客户端
2. 运行: python3 xiaobei_client.py
3. 或者后台运行: nohup python3 xiaobei_client.py > client.log 2>&1 &
4. 完成！格式会自动正确

标准格式示例:
  [02:55] xiaobei - 在线|0|6|20
  [02:56] xiaobei - 在线|0|6|21 (状态响应)
    """)
    
    asyncio.run(main())
