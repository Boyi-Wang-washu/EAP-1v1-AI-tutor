# 🚂 Railway 部署步骤（跟着做）

## ✅ **GitHub 已完成**

代码已推送到：
```
https://github.com/Boyi-Wang-washu/EAP-1v1-AI-tutor
```

---

## 🎯 **现在开始部署到 Railway**

### **Step 1：访问 Railway**

在浏览器打开：
```
https://railway.app
```

---

### **Step 2：登录 Railway**

1. 点击右上角 **Login**
2. 选择 **Login with GitHub**
3. 输入 GitHub 账号密码（如果未登录）
4. 授权 Railway 访问你的 GitHub

---

### **Step 3：创建新项目**

1. 登录后，点击 **New Project**
2. 选择 **Deploy from GitHub repo**
3. 搜索并选择 `EAP-1v1-AI-tutor`
4. 点击该仓库

---

### **Step 4：等待自动部署**

Railway 会自动：
- ✅ 检测到 Python 项目
- ✅ 读取 `requirements.txt`
- ✅ 安装所有依赖
- ✅ 运行 `python app.py`

**等待时间**：2-3 分钟

你会看到部署日志滚动...

---

### **Step 5：配置环境变量**

⚠️ **重要！必须配置这些变量**

在 Railway 项目页面：

1. 点击 **Variables** 标签
2. 点击 **+ New Variable**
3. 添加以下变量：

```
变量 1:
Name:  COZE_API_TOKEN
Value: sat_G9soTeMGzMr6oOmfwSdx80P1mGNCPJ3c7pFOLIyqPvajlvJyOFp5UyBedtgzXQ7s

变量 2:
Name:  BOT_ID  
Value: 7565215004040527912

变量 3:
Name:  FLASK_SECRET_KEY
Value: your-super-secret-random-key-12345
```

4. 点击 **Save** 或 **Add**

**Railway 会自动重新部署！**

---

### **Step 6：生成公网域名**

1. 点击 **Settings** 标签
2. 找到 **Networking** 或 **Domains** 部分
3. 点击 **Generate Domain**
4. 系统会生成一个域名，例如：
   ```
   https://eap-1v1-ai-tutor-production.up.railway.app
   ```
5. **复制这个域名！**

---

### **Step 7：测试 API**

在浏览器访问：
```
https://你的域名.railway.app/api/health
```

应该看到：
```json
{
  "status": "ok",
  "message": "EAP Teaching Assistant API is running"
}
```

✅ 如果看到这个，说明部署成功！

---

## 🌐 **Step 8：更新 Vercel 环境变量**

### 8.1 访问 Vercel Dashboard

```
https://vercel.com/dashboard
```

### 8.2 配置环境变量

1. 找到你的项目 `cansolve-eap-agent-web`
2. 点击 **Settings**
3. 点击左侧 **Environment Variables**
4. 点击 **Add New**
5. 添加变量：
   ```
   Name:  NEXT_PUBLIC_CHAT_API_URL
   Value: https://你的域名.railway.app
   ```
6. 选择 **Production**, **Preview**, **Development** 都勾选
7. 点击 **Save**

### 8.3 重新部署

1. 回到项目主页
2. 点击 **Deployments**
3. 点击最新部署右侧的 **...** 按钮
4. 选择 **Redeploy**

或者：直接推送代码到 GitHub，会自动触发部署。

---

## ✅ **完成！测试上线功能**

### **测试线上聊天功能**

访问：
```
https://cansolve-eap-agent-web.vercel.app/tutor/chat
```

应该可以：
- ✅ 看到聊天界面
- ✅ 发送消息
- ✅ 收到 AI 回复
- ✅ 历史记录保存

---

## 🎊 **部署完成架构**

```
用户访问
    ↓
https://cansolve-eap-agent-web.vercel.app (Vercel)
    ↓
Next.js 渲染界面
    ↓
调用 API
    ↓
https://xxx.railway.app/api/chat (Railway)
    ↓
Flask 处理 + Coze AI
    ↓
返回回复
    ↓
显示在网页上
```

**完全云端部署！全球可访问！** 🌍

---

## 📝 **环境变量总结**

### **Railway (Flask API)**
```
COZE_API_TOKEN = sat_G9soTeMGzMr6oOmfwSdx80P1mGNCPJ3c7pFOLIyqPvajlvJyOFp5UyBedtgzXQ7s
BOT_ID = 7565215004040527912
FLASK_SECRET_KEY = your-random-secret-key
```

### **Vercel (Next.js)**
```
NEXT_PUBLIC_CHAT_API_URL = https://你的域名.railway.app
```

---

## 🐛 常见问题

### Q: Railway 部署失败
**A**: 
1. 查看 Deployments → Logs
2. 检查 requirements.txt 是否正确
3. 检查环境变量是否配置

### Q: API 调用 500 错误
**A**:
1. 检查 Railway 环境变量是否配置
2. 查看 Railway Logs
3. 确认 Coze API Token 有效

### Q: CORS 错误
**A**:
需要更新 app.py 的 CORS 配置（我待会帮你）

---

**现在开始部署吧！跟着步骤做，遇到问题随时告诉我！** 🚀

