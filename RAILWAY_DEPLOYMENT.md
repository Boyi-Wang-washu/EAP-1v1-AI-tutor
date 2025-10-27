# 🚂 Railway 部署完整指南

## 📋 前置准备

- [x] Flask 代码已准备好
- [x] 已创建部署配置文件（.gitignore, railway.json, Procfile）
- [ ] GitHub 账号
- [ ] Railway 账号（用 GitHub 登录即可）

---

## 🎯 部署步骤（10分钟）

### **Step 1：创建 GitHub 仓库**

#### 1.1 在 GitHub 创建新仓库

1. 访问 https://github.com/new
2. 仓库名：`cansolve-eap-chat-api`
3. 描述：`Flask API for EAP Teaching Assistant`
4. 选择 Public 或 Private
5. **不要**勾选 Initialize with README
6. 点击 **Create repository**

#### 1.2 推送代码到 GitHub

在当前窗口（memorized 文件夹）运行：

```bash
# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Flask Chat API"

# 连接远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/cansolve-eap-chat-api.git

# 推送
git branch -M main
git push -u origin main
```

---

### **Step 2：部署到 Railway**

#### 2.1 注册/登录 Railway

1. 访问 https://railway.app
2. 点击 **Login**
3. 选择 **Login with GitHub**
4. 授权 Railway 访问你的 GitHub

#### 2.2 创建新项目

1. 点击 **New Project**
2. 选择 **Deploy from GitHub repo**
3. 找到并选择 `cansolve-eap-chat-api` 仓库
4. 点击 **Deploy Now**

#### 2.3 等待部署

Railway 会自动：
- ✅ 检测到 Python 项目
- ✅ 安装 requirements.txt 中的依赖
- ✅ 运行 app.py
- ✅ 生成公网域名

大约 2-3 分钟完成。

#### 2.4 配置环境变量（重要！）

在 Railway 项目中：

1. 点击 **Variables** 标签
2. 添加环境变量：
   ```
   COZE_API_TOKEN=sat_G9soTeMGzMr6oOmfwSdx80P1mGNCPJ3c7pFOLIyqPvajlvJyOFp5UyBedtgzXQ7s
   BOT_ID=7565215004040527912
   FLASK_SECRET_KEY=your-random-secret-key-here
   ```
3. 点击 **Save**
4. Railway 会自动重新部署

#### 2.5 获取公网地址

1. 点击 **Settings** 标签
2. 找到 **Domains** 部分
3. 点击 **Generate Domain**
4. 获得地址，例如：`https://cansolve-eap-chat-api.railway.app`

---

### **Step 3：更新 Next.js 环境变量**

#### 3.1 本地测试

在 Next.js 项目的 `.env.local`：
```env
# 改为 Railway 地址
NEXT_PUBLIC_CHAT_API_URL=https://cansolve-eap-chat-api.railway.app
```

重启 Next.js：
```bash
npm run dev
```

测试：访问 `http://localhost:3000/tutor/chat`

#### 3.2 Vercel 生产环境

1. 访问 https://vercel.com/dashboard
2. 找到你的项目 `cansolve-eap-agent-web`
3. 点击 **Settings** → **Environment Variables**
4. 添加变量：
   ```
   Name: NEXT_PUBLIC_CHAT_API_URL
   Value: https://cansolve-eap-chat-api.railway.app
   ```
5. 点击 **Save**
6. 重新部署（或等待下次自动部署）

---

### **Step 4：更新 Flask CORS 配置**

需要添加 Railway 的域名到 CORS 允许列表。

修改 `app.py`（我来帮你）：
```python
CORS(app, 
     resources={r"/api/*": {"origins": [
         "http://localhost:3000",
         "http://127.0.0.1:3000",
         "https://cansolve-eap-agent-web.vercel.app",
         "https://cansolve-eap-chat-api.railway.app"  # Railway 域名
     ]}},
     ...
)
```

然后推送更新：
```bash
git add app.py
git commit -m "Update CORS for Railway"
git push
```

Railway 会自动重新部署。

---

## ✅ 部署完成检查清单

- [ ] GitHub 仓库已创建
- [ ] 代码已推送到 GitHub
- [ ] Railway 项目已创建
- [ ] Railway 环境变量已配置
- [ ] Railway 部署成功
- [ ] 获得 Railway 公网域名
- [ ] Next.js 本地环境变量已更新
- [ ] Vercel 环境变量已更新
- [ ] CORS 配置已更新
- [ ] 测试通过

---

## 🧪 测试

### 测试 Railway API
```bash
# 健康检查
curl https://your-app.railway.app/api/health
```

应该返回：
```json
{"status": "ok", "message": "EAP Teaching Assistant API is running"}
```

### 测试 Vercel 网站
```
访问：https://cansolve-eap-agent-web.vercel.app/tutor/chat
应该可以正常聊天
```

---

## 💡 Railway 免费额度

```
免费计划包括：
✅ 每月 $5 使用额度
✅ 512MB RAM
✅ 1GB 磁盘空间
✅ 每月 100GB 流量

足够你的聊天 API 使用！
```

---

## 🐛 常见问题

### Q: Railway 部署失败
**A**: 查看 Railway 的 **Deployments** 标签，查看错误日志

### Q: API 调用 404
**A**: 检查 Railway 域名是否正确，是否加了 `/api/chat`

### Q: CORS 错误
**A**: 确保 Railway 的 CORS 配置包含你的 Vercel 域名

---

## 🎊 完成后的架构

```
用户访问 Vercel 网站
    ↓
https://cansolve-eap-agent-web.vercel.app
    ↓
Next.js 渲染聊天界面
    ↓
调用 Railway API
    ↓
https://cansolve-eap-chat-api.railway.app/api/chat
    ↓
返回 AI 回复
    ↓
显示在界面上
```

**完全云端部署！** ✨

---

## 📝 需要我帮你做什么？

1. **现在就开始**：我帮你创建 Git 命令并推送到 GitHub
2. **提供详细指导**：一步步教你操作 Railway
3. **帮你调试**：如果部署遇到问题

**准备好开始了吗？** 🚀

