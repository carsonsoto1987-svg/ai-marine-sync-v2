#!/usr/bin/env python3
"""东东标准客户端"""
import asyncio
import websockets
import json
from datetime import datetime

NODE_ID = "dongdong"
NODE_NAME = "东东"
SERVER = "ws://150.158.28.54:8765"

async def main():
    print(f"🐱 {NODE_NAME}标准客户端启动")
    while True:
        try:
            async with websockets.connect(SERVER) as ws:
                await ws.send(json.dumps({"type": "register", "node_id": NODE_ID, "name": NODE_NAME}))
                print("✅ 已连接")
                
                # 首次状态
                await send_status(ws, "首次连接")
                
                async for raw in ws:
                    data = json.loads(raw)
                    sender = data.get("from")
                    content = data.get("content", "").lower()
                    
                    if sender == NODE_ID:
                        continue
                    
                    # 握手
                    if content == "hhh":
                        await ws.send(json.dumps({"type": "chat", "from": NODE_ID, "content": "GGG"}))
                    
                    # 状态检查
                    elif "ping" in content or "状态" in content:
                        await send_status(ws, "状态响应")
                        
        except Exception as e:
            print(f"断开: {e}, 5秒后重连...")
            await asyncio.sleep(5)

async def send_status(ws, reason=""):
    now = datetime.now().strftime('%H:%M')
    tasks = 0
    kb = 5  # 东东知识库数
    msgs = 0
    
    status = f"[{now}] {NODE_ID} - 在线|{tasks}|{kb}|{msgs}"
    if reason:
        status += f" ({reason})"
    
    await ws.send(json.dumps({"type": "chat", "from": NODE_ID, "content": status}))
    print(f"📤 {status}")

if __name__ == "__main__":
    asyncio.run(main())
