# 知识库共享指南 - 如何给其他 AI 访问权限

**创建日期：** 2026-03-25  
**适用对象：** DeepSeek、Claude、GPT 等其他 AI 助手

---

## 方法一：直接文件共享（推荐）

### 步骤

1. **打包知识库**
```bash
# 在终端执行
cd ~/.openclaw/workspace/knowledge
tar -czvf marine-knowledge-base.tar.gz *
```

2. **发送给其他 AI**
   - 通过邮件发送 `marine-knowledge-base.tar.gz`
   - 或上传到云盘分享链接
   - 或直接复制粘贴关键文档内容

3. **其他 AI 加载方式**
   - **DeepSeek:** 上传文件后说"请阅读这些文档并纳入你的知识库"
   - **Claude:** 上传文件或粘贴内容到对话
   - **ChatGPT:** 使用 Code Interpreter 上传文件

---

## 方法二：RAG 系统接入（技术方案）

### 架构
```
你的知识库（Markdown文件）
         ↓
   向量数据库（Vector DB）
         ↓
   API 接口
         ↓
   DeepSeek/其他 AI 调用
```

### 实施方案

#### A. 使用 OpenClaw 的 sessions 功能
```bash
# 在 DeepSeek 中配置
openclaw sessions list  # 查看当前会话
openclaw sessions send <session-key> "请读取 knowledge/ 目录下的所有文档"
```

#### B. 构建 API 服务
```python
# 简单的知识库 API（Python FastAPI）
from fastapi import FastAPI
import os

app = FastAPI()
KNOWLEDGE_DIR = "/Users/carson/.openclaw/workspace/knowledge"

@app.get("/knowledge/{topic}")
def get_knowledge(topic: str):
    file_path = os.path.join(KNOWLEDGE_DIR, f"{topic}.md")
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return {"content": f.read()}
    return {"error": "Not found"}

@app.get("/knowledge/search")
def search_knowledge(query: str):
    # 实现文档搜索逻辑
    pass
```

#### C. 使用现有知识管理平台
- **Notion** - 导出为 Markdown，导入 Notion，共享给 AI
- **GitBook** - 发布为在线文档，AI 可爬取
- **Obsidian Publish** - 发布为网站

---

## 方法三：Git 仓库共享（最佳长期方案）

### 步骤

1. **创建 Git 仓库**
```bash
cd ~/.openclaw/workspace/knowledge
git init
git add .
git commit -m "Initial knowledge base"
```

2. **推送到 GitHub/GitLab**
```bash
git remote add origin https://github.com/yourusername/marine-knowledge-base.git
git push -u origin main
```

3. **其他 AI 访问**
   - **DeepSeek:** "请从 https://github.com/.../raw/main/... 读取知识库"
   - **Claude:** 提供 GitHub 链接，它可以访问和阅读
   - **自定义 AI:** 通过 Git API 拉取

### 自动化同步
设置 cron 任务自动提交更新：
```bash
# 每天自动提交知识库更新
0 23 * * * cd ~/.openclaw/workspace/knowledge && git add . && git commit -m "Daily update $(date)" && git push
```

---

## 方法四：共享文件系统（局域网/云端）

### 方案 A：NAS/共享文件夹
```
将 knowledge/ 目录设置为共享文件夹
其他 AI 通过 SMB/NFS 挂载访问
```

### 方案 B：云同步
- **Dropbox/Google Drive/OneDrive**
- 将 knowledge/ 目录放入同步文件夹
- 在其他 AI 所在设备安装同步客户端

---

## 推荐方案（根据场景选择）

| 场景 | 推荐方案 | 原因 |
|-----|---------|------|
| **一次性分享** | 方法一：打包发送 | 简单快捷 |
| **长期协作** | 方法三：Git仓库 | 版本控制、自动同步 |
| **企业环境** | 方法二：API服务 | 安全可控 |
| **多设备访问** | 方法四：云同步 | 实时更新 |

---

## 给 DeepSeek 的具体操作步骤

### 如果你使用 DeepSeek 网页版
1. 将知识库文档复制到文本文件
2. 在 DeepSeek 对话框上传文件
3. 说："请阅读这些文档，它们包含海水观赏鱼和珊瑚的专业知识。请将内容纳入你的知识库，以后回答相关问题时会用到。"

### 如果你使用 DeepSeek API
```python
import openai

# 读取知识库
def load_knowledge():
    knowledge = {}
    for root, dirs, files in os.walk("knowledge/"):
        for file in files:
            if file.endswith('.md'):
                with open(os.path.join(root, file)) as f:
                    knowledge[file] = f.read()
    return knowledge

# 调用 DeepSeek API 时，在 system prompt 中加入知识
system_prompt = """
你是一个海水观赏鱼和珊瑚专家。请参考以下知识库内容回答问题：

{ knowledge_content }

回答问题时请基于上述知识库，如不确定请说明。
"""
```

---

## 注意事项

### 知识更新
- 建议定期同步（每周或每月）
- 使用 Git 可以追踪变更历史
- 建立版本号系统（如 v1.0, v1.1）

### 权限管理
- 敏感信息不要放入共享知识库
- 商业机密需要加密或脱敏
- 考虑使用私有仓库

### 格式兼容性
- Markdown 格式通用性最好
- 避免使用特定平台的扩展语法
- 图片使用相对路径或绝对 URL

---

## 快速行动清单

- [ ] 选择适合的共享方案
- [ ] 导出/打包知识库
- [ ] 发送给 DeepSeek/其他 AI
- [ ] 验证对方是否正确加载
- [ ] 建立定期同步机制

---

*需要我帮你实施其中某个方案吗？*
