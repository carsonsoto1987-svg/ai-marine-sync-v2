#!/usr/bin/env python3
"""阿海标准客户端"""
import asyncio
import websockets
import json
from datetime import datetime

NODE_ID = "ahai"
NODE_NAME = "阿海"
SERVER = "ws://127.0.0.1:8765"  # 阿海是本机

async def main():
    print(f"🌊 {NODE_NAME}标准客户端启动")
    while True:
        try:
            async with websockets.connect(SERVER) as ws:
                await ws.send(json.dumps({"type": "register", "node_id": NODE_ID, "name": NODE_NAME}))
                print("✅ 已连接")
                
                await send_status(ws, "首次连接")
                
                async for raw in ws:
                    data = json.loads(raw)
                    sender = data.get("from")
                    content = data.get("content", "").lower()
                    
                    if sender == NODE_ID:
                        continue
                    
                    if content == "hhh":
                        await ws.send(json.dumps({"type": "chat", "from": NODE_ID, "content": "GGG"}))
                    elif "ping" in content or "状态" in content:
                        await send_status(ws, "状态响应")
                        
        except Exception as e:
            print(f"断开: {e}, 5秒后重连...")
            await asyncio.sleep(5)

async def send_status(ws, reason=""):
    now = datetime.now().strftime('%H:%M')
    tasks = 1  # 阿海有爬虫任务
    kb = 57    # 阿海知识库数
    msgs = 0
    
    status = f"[{now}] {NODE_ID} - 在线|{tasks}|{kb}|{msgs}"
    if reason:
        status += f" ({reason})"
    
    await ws.send(json.dumps({"type": "chat", "from": NODE_ID, "content": status}))
    print(f"📤 {status}")

if __name__ == "__main__":
    asyncio.run(main())
