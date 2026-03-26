#!/usr/bin/env python3
"""
小北标准客户端 - 自动发送标准格式状态报告
运行方法: python3 xiaobei_standard_client.py
"""
import asyncio
import websockets
import json
import time
from datetime import datetime

# 服务器配置
SERVER = "ws://150.158.28.54:8765"
NODE_ID = "xiaobei"
NODE_NAME = "小北"

async def main():
    print("="*60)
    print("🐱 小北标准客户端启动")
    print("="*60)
    print(f"节点ID: {NODE_ID}")
    print(f"服务器: {SERVER}")
    print("="*60)
    
    while True:
        try:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 连接中...")
            
            async with websockets.connect(SERVER) as ws:
                # 注册
                await ws.send(json.dumps({
                    "type": "register",
                    "node_id": NODE_ID,
                    "name": NODE_NAME
                }))
                print(f"✅ 已连接服务器")
                
                # 发送首次标准状态报告
                await send_standard_status(ws, "首次连接")
                
                # 持续监听和回复
                async for raw_msg in ws:
                    try:
                        data = json.loads(raw_msg)
                        msg_type = data.get("type")
                        sender = data.get("from")
                        content = data.get("content", "").strip().lower()
                        
                        # 忽略自己的消息
                        if sender == NODE_ID:
                            continue
                        
                        # 处理消息
                        if msg_type == "chat":
                            print(f"\n📨 收到 [{sender}]: {data.get('content', '')[:50]}")
                            
                            # 握手信号
                            if content == "hhh":
                                await ws.send(json.dumps({
                                    "type": "chat",
                                    "from": NODE_ID,
                                    "content": "GGG"
                                }))
                                print("🤝 握手成功: GGG")
                            
                            # 状态检查请求
                            elif "状态检查" in content or "ping" in content or "status" in content:
                                await send_standard_status(ws, "状态检查响应")
                            
                            # 其他消息 - 确认收到
                            else:
                                # 每3条消息回复一次状态，避免刷屏
                                if hash(str(datetime.now().minute)) % 3 == 0:
                                    await send_standard_status(ws, "定期报告")
                        
                    except Exception as e:
                        print(f"⚠️  处理消息出错: {e}")
                        
        except Exception as e:
            print(f"❌ 连接断开: {e}")
            print("5秒后重连...")
            await asyncio.sleep(5)

async def send_standard_status(ws, reason=""):
    """
    发送标准格式状态报告
    格式: [HH:MM] xiaobei - 在线|任务数|知识库数|消息数
    """
    now = datetime.now()
    time_str = now.strftime('%H:%M')
    
    # 这里可以读取实际的任务数和知识库数
    # 现在是示例数据
    tasks = 0  # 实际任务数
    kb_count = 6  # 实际知识库文档数
    msg_count = int(time.time()) % 100  # 示例消息数
    
    # 标准格式！
    status_msg = f"[{time_str}] {NODE_ID} - 在线|{tasks}|{kb_count}|{msg_count}"
    
    if reason:
        status_msg += f" ({reason})"
    
    await ws.send(json.dumps({
        "type": "chat",
        "from": NODE_ID,
        "content": status_msg
    }))
    
    print(f"📤 发送状态: {status_msg}")

# 定时发送状态报告（每30分钟）
async def periodic_status(ws):
    """每30分钟自动发送状态"""
    while True:
        await asyncio.sleep(1800)  # 30分钟
        try:
            await send_standard_status(ws, "定期报告")
        except:
            break

if __name__ == "__main__":
    print("""
使用方法:
1. 保存此文件为: xiaobei_standard_client.py
2. 运行: python3 xiaobei_standard_client.py
3. 保持运行即可自动发送标准格式

标准格式示例:
  [02:55] xiaobei - 在线|0|6|25

这个格式会被系统正确识别！
""")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 客户端已停止")