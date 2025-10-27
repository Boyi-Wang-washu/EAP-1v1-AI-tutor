# BNBU EAP Teaching Assistant

基于Flask和Coze API的英语教学辅助应用，支持1v1辅导对话和学习记录保存。

## 功能特性

- 🤖 集成Coze AI API，提供智能英语教学辅导
- 💾 JSON格式保存学习记录，支持多用户会话
- 🎨 现代化响应式Web界面，基于Tailwind CSS
- ⚡ 实时流式对话，提供流畅的学习体验
- 📱 移动端友好的响应式设计
- 🔒 用户认证和会话隔离，每个用户独立的学习记录
- 🎓 专为英语学习设计的1v1辅导界面

## 技术栈

- **后端**: Flask (Python Web框架)
deng- **前端**: Jinja2模板 + Tailwind CSS + JavaScript
- **AI API**: Coze API (字节跳动扣子平台)
- **数据存储**: SQLite + JSON文件存储
- **样式**: Tailwind CSS + FontAwesome Icons

## 安装和运行

### 1. 环境要求

- Python 3.7 或更高版本
- pip 包管理器

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

在 `app.py` 文件中修改以下配置：

```python
# 替换为您的Coze API Token
COZE_API_TOKEN = 'your_coze_api_token_here'

# 替换为您的Bot ID
BOT_ID = 'your_bot_id_here'

# 修改应用密钥（用于会话管理）
app.secret_key = 'your-secret-key-here'
```

### 4. 运行应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

## 项目结构

```
memorized/
├── app.py                 # Flask主应用文件
├── requirements.txt       # Python依赖包列表
├── README.md             # 项目说明文档
├── chat_history.json     # 聊天记录存储文件（运行时自动生成）
├── templates/            # Jinja2模板目录
│   └── index.html        # 主页面模板
└── static/               # 静态资源目录
    ├── css/
    │   └── style.css     # 样式文件
    └── js/
        └── chat.js       # 前端交互脚本
```

## API接口

### 聊天接口
- **URL**: `/chat`
- **方法**: POST
- **参数**: `{"message": "用户消息"}`
- **返回**: `{"success": true, "response": "AI回复", "token_usage": 数量}`

### 历史记录接口
- **URL**: `/history`
- **方法**: GET
- **返回**: `{"messages": [消息列表]}`

### 清除历史接口
- **URL**: `/clear_history`
- **方法**: POST
- **返回**: `{"success": true}`

## 聊天记录格式

聊天记录以JSON格式存储在 `chat_history.json` 文件中：

```json
{
  "用户ID": [
    {
      "id": "消息唯一ID",
      "type": "user|bot",
      "content": "消息内容",
      "timestamp": "2024-01-01T12:00:00",
      "token_usage": 100
    }
  ]
}
```

## 获取Coze API密钥

1. 访问 [Coze开放平台](https://www.coze.cn/open/oauth/pats)
2. 创建个人访问令牌(PAT)
3. 设置令牌名称、过期时间和权限
4. 复制生成的令牌到 `app.py` 中

## 创建Coze机器人

1. 登录 [Coze平台](https://www.coze.cn/)
2. 创建新的机器人
3. 配置机器人的人设和能力
4. 从机器人URL中获取Bot ID（URL末尾的数字）

## 自定义配置

### 修改端口和主机
在 `app.py` 文件末尾修改：
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### 修改样式
编辑 `static/css/style.css` 文件来自定义界面样式。

### 添加新功能
在 `app.py` 中添加新的路由和功能，在 `static/js/chat.js` 中添加前端交互逻辑。

## 注意事项

- 请妥善保管您的API密钥，不要提交到版本控制系统
- 聊天记录文件会随着使用增长，建议定期备份和清理
- 在生产环境中，建议使用更安全的会话管理和数据存储方案
- Token使用量会影响API调用成本，请合理使用

## 许可证

本项目仅供学习和研究使用。