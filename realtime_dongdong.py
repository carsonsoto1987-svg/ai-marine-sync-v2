#!/usr/bin/env python3
"""
东东 实时客户端 - GGG握手版本
IP: 182.8.65.120
连接: ws://150.158.28.54:8765
"""
import asyncio
import websockets
import json
import time

SERVER = "ws://150.158.28.54:8765"
NODE_ID = "dongdong"
NODE_NAME = "东东"

async def main():
    while True:
        try:
            print(f"[{time.strftime('%H:%M:%S')}] 连接中...", flush=True)
            async with websockets.connect(SERVER) as ws:
                await ws.send(json.dumps({
                    "type": "register",
                    "node_id": NODE_ID,
                    "name": NODE_NAME
                }))
                print(f"[{time.strftime('%H:%M:%S')}] ✅ 已连接", flush=True)

                async for raw_msg in ws:
                    try:
                        data = json.loads(raw_msg)
                        if data.get("type") == "chat" and data.get("from") != NODE_ID:
                            content = data.get("content", "").strip().lower()
                            sender = data.get("from")
                            
                            # 握手信号：收到"hhh"回复"GGG"
                            if content == "hhh":
                                await ws.send(json.dumps({
                                    "type": "chat",
                                    "from": NODE_ID,
                                    "content": "GGG"
                                }))
                                print(f"[{time.strftime('%H:%M:%S')}] 握手成功!")
                            
                            # 其他消息打印
                            else:
                                print(f"[{sender}]: {data.get('content', '')}")

                    except:
                        pass

        except Exception as e:
            print(f"断开: {e}", flush=True)
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())