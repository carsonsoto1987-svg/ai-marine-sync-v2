#!/usr/bin/env python3
"""
三人组命令广播系统 - 支持同时执行命令
命令格式: /run <命令>
"""
import asyncio
import websockets
import json
import time
import subprocess
import os
import sys

SERVER = "ws://150.158.28.54:8765"
NODE_ID = "dongdong"
NODE_NAME = "东东"

# 命令日志
CMD_LOG = os.path.expanduser("~/.openclaw/workspace/logs/commands.log")

def log(msg):
    ts = time.strftime('%H:%M:%S')
    print(f"[{ts}] {msg}", flush=True)
    with open(CMD_LOG, 'a') as f:
        f.write(f"[{ts}] {msg}\n")

async def execute_command(cmd):
    """执行命令并返回结果"""
    log(f"执行命令: {cmd}")
    try:
        # 判断命令类型
        if cmd.startswith("python3 ") or cmd.startswith("pip") or cmd.startswith("cd "):
            # Shell命令
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            output = result.stdout if result.stdout else result.stderr
        elif cmd.startswith("echo ") or cmd.startswith("mkdir ") or cmd.startswith("chmod ") or cmd.startswith("nohup "):
            # Shell命令
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
            output = result.stdout if result.stdout else result.stderr
        else:
            output = "未知命令类型"
        
        return output[:500] if output else "执行完成"
    except Exception as e:
        return f"错误: {e}"

async def main():
    while True:
        try:
            log("连接中...")
            async with websockets.connect(SERVER) as ws:
                await ws.send(json.dumps({
                    "type": "register",
                    "node_id": NODE_ID,
                    "name": NODE_NAME
                }))
                log("✅ 已连接")
                
                async for raw_msg in ws:
                    try:
                        data = json.loads(raw_msg)
                        if data.get("type") == "chat" and data.get("from") != NODE_ID:
                            content = data.get("content", "").strip()
                            sender = data.get("from")
                            
                            # 握手信号
                            if content.lower() == "hhh":
                                await ws.send(json.dumps({
                                    "type": "chat",
                                    "from": NODE_ID,
                                    "content": "GGG"
                                }))
                                log("握手成功")
                            
                            # 命令广播：以 /run 开头
                            elif content.startswith("/run "):
                                cmd = content[5:]  # 去掉 /run 
                                log(f"收到命令: {cmd}")
                                
                                # 执行命令
                                result = await execute_command(cmd)
                                
                                # 返回结果
                                await ws.send(json.dumps({
                                    "type": "chat",
                                    "from": NODE_ID,
                                    "content": f"✅ 执行: {cmd[:30]}... \n结果: {result[:200]}"
                                }))
                                log(f"结果: {result[:100]}")
                            
                            else:
                                log(f"[{sender}]: {content}")

                    except:
                        pass

        except Exception as e:
            log(f"断开: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
