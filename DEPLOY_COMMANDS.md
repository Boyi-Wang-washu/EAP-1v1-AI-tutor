# 🚀 部署命令清单（复制粘贴即可）

## 📋 前置准备

1. 在 GitHub 创建新仓库：`cansolve-eap-chat-api`
2. 复制仓库地址（例如：`https://github.com/你的用户名/cansolve-eap-chat-api.git`）

---

## 💻 Git 命令（在当前窗口执行）

### **一次性执行所有命令**

```bash
# 1. 初始化 Git
git init

# 2. 添加所有文件
git add .

# 3. 提交
git commit -m "Initial commit: Flask Chat API for EAP Teaching Assistant"

# 4. 连接远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/cansolve-eap-chat-api.git

# 5. 推送到 GitHub
git branch -M main
git push -u origin main
```

---

## 🚂 Railway 部署步骤

### **1. 访问 Railway**
```
https://railway.app
```

### **2. 登录**
- 选择 "Login with GitHub"
- 授权 Railway

### **3. 创建项目**
- 点击 "New Project"
- 选择 "Deploy from GitHub repo"
- 选择 `cansolve-eap-chat-api` 仓库
- 点击 "Deploy Now"

### **4. 配置环境变量**

在 Railway 项目中，添加这些变量：

```
COZE_API_TOKEN = sat_G9soTeMGzMr6oOmfwSdx80P1mGNCPJ3c7pFOLIyqPvajlvJyOFp5UyBedtgzXQ7s
BOT_ID = 7565215004040527912
```

### **5. 生成域名**
- Settings → Domains
- 点击 "Generate Domain"
- 复制域名（例如：`https://xxx.railway.app`）

---

## 🌐 更新 Next.js 配置

### **本地 .env.local**
```env
NEXT_PUBLIC_CHAT_API_URL=https://你的域名.railway.app
```

### **Vercel 环境变量**
1. 访问 Vercel Dashboard
2. 找到项目 → Settings → Environment Variables
3. 添加：
   ```
   NEXT_PUBLIC_CHAT_API_URL = https://你的域名.railway.app
   ```
4. 重新部署

---

## ✅ 测试

### **测试 Railway API**
```
访问：https://你的域名.railway.app/api/health

应该看到：
{"status": "ok", "message": "EAP Teaching Assistant API is running"}
```

### **测试 Vercel 网站**
```
访问：https://cansolve-eap-agent-web.vercel.app/tutor/chat
应该可以正常聊天
```

---

## 🎊 完成！

**两个服务都在云端运行！**

```
✅ Next.js → Vercel
✅ Flask API → Railway
✅ 完全可访问
```

---

## 📞 需要帮助？

**如果遇到问题**：
1. 查看 Railway Deployments 日志
2. 检查环境变量是否正确
3. 测试 API 健康检查端点
4. 随时问我！

**Good luck!** 🚀

