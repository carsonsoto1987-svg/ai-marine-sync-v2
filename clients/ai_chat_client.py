#!/usr/bin/env python3
"""阿海WebSocket群聊客户端"""
import asyncio
import json
import sys
from datetime import datetime

# 东东的WebSocket服务器
WS_HOST = "182.8.65.120"
WS_PORT = 8765

async def chat():
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(WS_HOST, WS_PORT),
            timeout=5
        )
        print(f"✅ 连接到东东的群聊 ({WS_HOST}:{WS_PORT})")
        
        # 发送阿海的自我介绍
        hello = json.dumps({
            "type": "join",
            "name": "阿海",
            "time": datetime.now().isoformat()
        })
        writer.write(hello.encode() + b'\n')
        await writer.drain()
        
        # 监听消息
        while True:
            data = await reader.readline()
            if not data:
                break
            msg = json.loads(data.decode())
            print(f"[{msg.get('time','')[:8]}] {msg.get('name','?')}: {msg.get('text','')}")
            
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("原因: 网络不通(182.8.65.120无法从这边访问)")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(chat())
