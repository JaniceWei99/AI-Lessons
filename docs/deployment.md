# 部署指南 / Deployment Guide

> 最后更新: 2026-03-31 23:00 +0800

---

## 目录

1. [部署要求](#1-部署要求)
2. [部署方式一览](#2-部署方式一览)
3. [静态文件部署](#3-静态文件部署)
4. [GitHub Pages 部署](#4-github-pages-部署)
5. [Nginx 部署](#5-nginx-部署)
6. [Vercel / Netlify 一键部署](#6-vercel--netlify-一键部署)
7. [Docker 部署](#7-docker-部署)
8. [离线 / 局域网部署](#8-离线--局域网部署)
9. [部署检查清单](#9-部署检查清单)
10. [常见问题](#10-常见问题)

---

## 1. 部署要求

| 要求               | 说明                                                       |
|:-------------------|:----------------------------------------------------------|
| 服务器类型          | 任意静态文件服务器                                          |
| 构建步骤            | **无** — 纯静态文件，直接部署                                |
| 外部依赖            | Google Fonts CDN (fonts.googleapis.com) — 可选              |
| 最低带宽            | 首页约 50 KB (gzip)，单课约 30 KB (gzip)                    |
| HTTPS              | 推荐但非必须                                                |
| 数据库              | **无** — 所有数据存储于用户浏览器 localStorage               |
| 服务端语言          | **无** — 纯前端项目                                         |

---

## 2. 部署方式一览

| 方式                 | 难度   | 费用   | 适合场景                         |
|:--------------------|:------:|:------:|:--------------------------------|
| 直接打开 HTML        | 零     | 免费   | 个人本地使用、演示                |
| GitHub Pages         | 低     | 免费   | 开源项目、长期托管                |
| Vercel / Netlify     | 低     | 免费   | 快速部署、自动 CI/CD             |
| Nginx / Apache       | 中     | 低     | 学校内网、企业自建服务器           |
| Docker               | 中     | 低     | 容器化环境、统一部署              |
| U 盘 / 局域网        | 零     | 免费   | 无网络环境、教室课堂              |

---

## 3. 静态文件部署

项目是纯静态 HTML，不需要任何构建步骤。

```bash
# 将以下文件/目录上传到 Web 服务器即可：
AI-Class/
├── index.html              # 门户页面 (版本选择器)
├── css/
│   └── style.css
├── js/
│   └── main.js
├── standard-5/             # 精简版 (5 课)
│   ├── index.html
│   └── lessons/
├── standard-15/            # 完整版 (15 课)
│   ├── index.html
│   └── lessons/
├── lab-10/                 # 实验版 (10 课)
│   ├── index.html
│   └── lessons/
├── app-inventor-10/        # AI App 创造营 (10 课)
│   ├── index.html
│   └── lessons/
├── web-ai-12/              # AI 网站工坊 (12 课)
│   ├── index.html
│   └── lessons/
└── assets/
    └── images/
```

> **注意**: `SPEC.md`、`test/`、`docs/` 目录不需要部署到生产环境。

---

## 4. GitHub Pages 部署

### 步骤

```bash
# 1. 初始化 Git 仓库 (如果尚未初始化)
cd AI-Class
git init
git add .
git commit -m "Initial commit"

# 2. 推送到 GitHub
git remote add origin https://github.com/<username>/AI-Class.git
git branch -M main
git push -u origin main
```

### 在 GitHub 上启用 Pages

1. 进入仓库 → **Settings** → **Pages**
2. Source 选择 **Deploy from a branch**
3. Branch 选择 `main`，目录选择 `/ (root)`
4. 点击 **Save**
5. 等待 1–2 分钟，访问 `https://<username>.github.io/AI-Class/`

### 自定义域名 (可选)

```bash
# 在项目根目录创建 CNAME 文件
echo "ai-class.example.com" > CNAME
git add CNAME && git commit -m "Add custom domain" && git push
```

在域名 DNS 中添加 CNAME 记录指向 `<username>.github.io`。

---

## 5. Nginx 部署

### 安装 Nginx

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install nginx -y

# CentOS / RHEL
sudo yum install nginx -y
```

### 配置文件

```nginx
# /etc/nginx/sites-available/ai-class
server {
    listen       80;
    server_name  ai-class.example.com;
    root         /var/www/ai-class;
    index        index.html;

    # 开启 gzip 压缩
    gzip             on;
    gzip_types       text/html text/css application/javascript;
    gzip_min_length  256;

    # 静态资源缓存
    location ~* \.(css|js|svg|png|jpg|jpeg|gif|ico|woff2)$ {
        expires    30d;
        add_header Cache-Control "public, immutable";
    }

    # SPA 回退 (本项目非 SPA，但保险起见)
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### 部署步骤

```bash
# 1. 复制文件
sudo mkdir -p /var/www/ai-class
sudo cp -r index.html css/ js/ standard-5/ standard-15/ lab-10/ app-inventor-10/ web-ai-12/ assets/ /var/www/ai-class/

# 2. 启用配置
sudo ln -s /etc/nginx/sites-available/ai-class /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### HTTPS (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d ai-class.example.com
```

---

## 6. Vercel / Netlify 一键部署

### Vercel

1. 访问 [vercel.com](https://vercel.com)，使用 GitHub 登录
2. 点击 **New Project** → 导入 GitHub 仓库
3. Framework Preset 选择 **Other**
4. Build Command 留空，Output Directory 填 `.`
5. 点击 **Deploy**

### Netlify

1. 访问 [netlify.com](https://netlify.com)，使用 GitHub 登录
2. 点击 **Add new site** → **Import an existing project**
3. 选择 GitHub 仓库
4. Build Command 留空，Publish Directory 填 `.`
5. 点击 **Deploy site**

### 或者用 CLI 拖拽部署

```bash
# Netlify CLI
npm install -g netlify-cli
cd AI-Class
netlify deploy --prod --dir .
```

---

## 7. Docker 部署

### Dockerfile

在项目根目录创建 `Dockerfile`：

```dockerfile
FROM nginx:alpine
COPY index.html     /usr/share/nginx/html/
COPY css/           /usr/share/nginx/html/css/
COPY js/            /usr/share/nginx/html/js/
COPY standard-5/    /usr/share/nginx/html/standard-5/
COPY standard-15/   /usr/share/nginx/html/standard-15/
COPY lab-10/        /usr/share/nginx/html/lab-10/
COPY app-inventor-10/ /usr/share/nginx/html/app-inventor-10/
COPY web-ai-12/     /usr/share/nginx/html/web-ai-12/
COPY assets/        /usr/share/nginx/html/assets/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 构建与运行

```bash
docker build -t ai-class .
docker run -d -p 8080:80 --name ai-class ai-class
# 访问 http://localhost:8080
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3'
services:
  web:
    build: .
    ports:
      - "8080:80"
    restart: unless-stopped
```

```bash
docker-compose up -d
```

---

## 8. 离线 / 局域网部署

### U 盘直接使用

1. 将整个 `AI-Class/` 目录拷贝到 U 盘
2. 在目标电脑上双击 `index.html` 即可在浏览器中打开
3. 所有功能均可离线使用（仅 Google Fonts 字体回退到系统字体）

### 局域网 Python 服务器

```bash
# 在课程目录下启动简易 HTTP 服务器
cd AI-Class
python -m http.server 8000 --bind 0.0.0.0

# 局域网内其他设备通过 http://<教师IP>:8000 访问
```

### 离线字体处理

如需完全离线（含中文字体），可下载 Noto Sans SC：

```bash
# 下载字体文件
mkdir -p assets/fonts
curl -o assets/fonts/NotoSansSC.woff2 \
  "https://fonts.gstatic.com/s/notosanssc/v36/k3kCo84MPvpLmixcA63oeAL7Iqp5IZJF9bmaG9_FnYw.woff2"
```

然后修改 `css/style.css` 顶部，将 Google Fonts 链接替换为本地 `@font-face`。

---

## 9. 部署检查清单

| #  | 检查项                                  | 状态 |
|:--:|:---------------------------------------|:----:|
| 1  | `index.html` 可正常访问                 | [ ]  |
| 2  | 五个版本 (standard-5/standard-15/lab-10/app-inventor-10/web-ai-12) 页面均可从门户导航进入 | [ ]  |
| 3  | CSS 样式正常加载（检查控制台无 404）       | [ ]  |
| 4  | JS 脚本正常加载（检查控制台无错误）        | [ ]  |
| 5  | 中英双语切换正常                         | [ ]  |
| 6  | 暗色 / 亮色模式切换正常                  | [ ]  |
| 7  | Quiz 答题功能正常                        | [ ]  |
| 8  | 移动端响应式布局正常 (375px 宽度测试)      | [ ]  |
| 9  | 页面间上/下一课导航正确                   | [ ]  |
| 10 | Google Fonts 加载或字体回退正常           | [ ]  |

---

## 10. 常见问题

### Q: 部署后 CSS/JS 加载 404？

A: 检查文件路径。所有 HTML 中使用相对路径引用 CSS/JS：
- `index.html` (门户) → `css/style.css`, `js/main.js`
- `*/index.html` (版本首页) → `../css/style.css`, `../js/main.js`
- `*/lessons/*.html` (课程页) → `../../css/style.css`, `../../js/main.js`

确保目录结构完整上传。

### Q: 离线打开字体不显示？

A: 项目使用 Google Fonts CDN 加载 Noto Sans SC。离线时会自动回退到系统字体 (`system-ui, sans-serif`)，不影响功能使用。如需离线字体，参见 [第 8 节](#8-离线--局域网部署)。

### Q: 多人同时使用会冲突吗？

A: 不会。所有数据（进度、主题偏好、语言设置）存储在各用户浏览器的 localStorage 中，互不影响。

### Q: 需要后端服务吗？

A: 不需要。本项目是纯前端静态网站，任何能托管 HTML 文件的服务器都可以。

---

*文档版本: v1.3 | 最后更新: 2026-03-31 23:00 +0800*
