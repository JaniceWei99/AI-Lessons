# AI 探索之旅 / AI Explorer

> 面向青少年的人工智能入门课程，五大版本，纯前端网页交付，支持中英双语切换。

---

## 项目概览

| 属性 | 说明 |
|:-----|:----|
| 版本 | v1.4.0 |
| 受众 | 10-16 岁青少年，零基础或有少量编程经验 |
| 技术栈 | HTML5 + CSS3 + Vanilla JS (ES6+) |
| 外部依赖 | Google Fonts CDN — 仅此一个 |
| 浏览器 | Chrome / Edge / Firefox / Safari 最新两个主版本 |

---

## 五大版本

### 精简版 (standard-5) — 5 课时

| 课号 | 中文标题 | English Title |
|:----:|:--------|:-------------|
| 1 | 走进 AI 的世界 | Welcome to the World of AI |
| 2 | 机器是怎么"学习"的 | How Do Machines Learn? |
| 3 | 神经网络与深度学习 | Neural Networks & Deep Learning |
| 4 | 大语言模型与 AIGC | LLMs & AI-Generated Content |
| 5 | AI 的未来与责任 | The Future & Ethics of AI |

### 完整版 (standard-15) — 15 课时

| 课号 | 中文标题 | English Title |
|:----:|:--------|:-------------|
| 1 | 走进 AI 的世界 | Welcome to the World of AI |
| 2 | 机器是怎么"学习"的 | How Do Machines Learn? |
| 3 | 数据：AI 的燃料 | Data: The Fuel of AI |
| 4 | 监督学习实战 | Supervised Learning in Practice |
| 5 | 神经网络基础 | Neural Network Fundamentals |
| 6 | 深度学习与CNN | Deep Learning & CNNs |
| 7 | 自然语言处理 | Natural Language Processing |
| 8 | 大语言模型揭秘 | Inside Large Language Models |
| 9 | Prompt工程与应用 | Prompt Engineering & Applications |
| 10 | AIGC创意工坊 | AIGC Creative Workshop |
| 11 | 计算机视觉 | Computer Vision |
| 12 | 强化学习与游戏AI | Reinforcement Learning & Game AI |
| 13 | AI伦理与偏见 | AI Ethics & Bias |
| 14 | AI安全与隐私 | AI Safety & Privacy |
| 15 | AI的未来与你 | The Future of AI & You |

### 实验版 (lab-10) — 10 个动手实验

| 实验 | 中文标题 | English Title |
|:----:|:--------|:-------------|
| 1 | AI实验入门 | Getting Started with AI Labs |
| 2 | 图像识别实验 | Image Recognition Lab |
| 3 | 文本分析实验 | Text Analysis Lab |
| 4 | 聊天机器人实验 | Chatbot Lab |
| 5 | AI绘画实验 | AI Art Lab |
| 6 | 语音识别实验 | Speech Recognition Lab |
| 7 | 推荐系统实验 | Recommendation System Lab |
| 8 | 数据可视化实验 | Data Visualization Lab |
| 9 | AI游戏实验 | AI Game Lab |
| 10 | 综合项目展示 | Final Project Showcase |

### AI App 创造营 (app-inventor-10) — 10 课时

| 课号 | 中文标题 | English Title |
|:----:|:--------|:-------------|
| 1 | App Inventor 快速入门（上） | App Inventor Quick Start (Part 1) |
| 2 | App Inventor 快速入门（下） | App Inventor Quick Start (Part 2) |
| 3 | 天气 API 实战 | Weather API in Action |
| 4 | AI 聊天助手（上） | AI Chat Assistant (Part 1) |
| 5 | AI 聊天助手（下） | AI Chat Assistant (Part 2) |
| 6 | AI 图像识别 | AI Image Recognition |
| 7 | AI 语音助手 | AI Voice Assistant |
| 8 | 设计工作坊 | Design Workshop |
| 9 | 构建与调试 | Build & Debug |
| 10 | Demo Day — 展示你的 App | Demo Day — Show Your App |

### AI 网站工坊 (web-ai-12) — 12 课时

| 课号 | 中文标题 | English Title |
|:----:|:--------|:-------------|
| 1 | HTML 基础（上） | HTML Basics (Part 1) |
| 2 | HTML 基础（下） | HTML Basics (Part 2) |
| 3 | CSS 美化（上） | CSS Styling (Part 1) |
| 4 | CSS 美化（下） | CSS Styling (Part 2) |
| 5 | JavaScript 入门（上） | JavaScript Intro (Part 1) |
| 6 | JavaScript 入门（下） | JavaScript Intro (Part 2) |
| 7 | API 调用基础 | API Basics — The Magic of fetch() |
| 8 | 接入 AI（上） | AI Integration (Part 1) |
| 9 | 接入 AI（下） | AI Integration (Part 2) |
| 10 | AI 图像生成 | AI Image Generation |
| 11 | 部署上线 | Deploy — Go Live |
| 12 | Demo Day — 分享你的 AI 网站 | Demo Day — Share Your AI Website |

---

## 主要特性

- **教师讲解文本** — 52 份教师讲稿 (Markdown)，覆盖全部课程每一课
- **中英双语** — 一键切换，偏好自动保存
- **暗色模式** — 亮色 / 暗色主题，默认跟随系统偏好
- **丰富交互** — 时间线、决策树、AI 鉴别挑战、Prompt 工程练习
- **即时测验** — 选择题 + 正确率统计 + 智能反馈 + 部分提交支持
- **进度保存** — localStorage 自动记录完成状态与测验分数
- **响应式布局** — 手机 / 平板 / 桌面三端自适应
- **打印友好** — `@media print` 样式，可直接打印为讲义
- **零构建依赖** — 纯 HTML / CSS / JS，双击即可打开

---

## 目录结构

```
AI-Class/
├── index.html                  # 门户页面 (版本选择器)
├── css/style.css               # 共享全局样式 (1,491 行, 25 个模块)
├── js/main.js                  # 共享全局脚本 (486 行, 12 个功能模块)
├── standard-5/                 # 精简版 (5 课时)
│   ├── index.html
│   ├── lessons/                # lesson1-5.html
│   └── scripts/                # 第1-5课-讲解文本.md
├── standard-15/                # 完整版 (15 课时)
│   ├── index.html
│   ├── lessons/                # lesson1-15.html
│   └── scripts/                # 第1-15课-讲解文本.md
├── lab-10/                     # 实验版 (10 实验)
│   ├── index.html
│   ├── lessons/                # lesson1-10.html
│   └── scripts/                # 第1-10课-讲解文本.md
├── app-inventor-10/            # AI App 创造营 (10 课时)
│   ├── index.html
│   ├── lessons/                # lesson1-10.html
│   └── scripts/                # 第1-10课-讲解文本.md
├── web-ai-12/                  # AI 网站工坊 (12 课时)
│   ├── index.html
│   ├── lessons/                # lesson1-12.html
│   └── scripts/                # 第1-12课-讲解文本.md
├── test/                       # 测试套件 (7 套件, 6,277 用例)
│   ├── run_all.py
│   └── test_*.py
├── docs/                       # 项目文档
└── serve.py                    # 本地开发服务器 (端口 4200)
```

---

## 快速开始

### 方式一：直接打开

```bash
open index.html        # macOS
xdg-open index.html    # Linux
start index.html       # Windows
```

### 方式二：本地服务器（推荐）

```bash
python3 serve.py
# 访问 http://localhost:4200
```

---

## 运行测试

```bash
# 需要 uv (Python 包管理器)
# 安装: curl -LsSf https://astral.sh/uv/install.sh | sh

# 运行全部测试 (7 个套件, 6,277 个用例)
uv run test/run_all.py

# 运行单个套件
uv run test/test_html_structure.py
```

测试报告自动生成到 `test/reports/`：
- `report.html` — 浏览器可视化报告
- `summary.json` — 机器可读汇总

---

## 技术亮点

| 特性 | 实现方式 |
|:----|:--------|
| 双语切换 | `data-lang` 属性 + CSS 可见性切换，无页面刷新 |
| 暗色模式 | CSS 自定义属性 + `data-theme`，跟随 `prefers-color-scheme` |
| 进度持久化 | localStorage 存储完成状态和测验分数 |
| 滚动动画 | IntersectionObserver API |
| 响应式布局 | CSS Grid + Flexbox + 3 个断点 |
| 零依赖 | 无框架、无构建工具 |
| 交互组件 | Quiz、决策树、时间线、AI 鉴别、Prompt 挑战 — 全部原生 JS |
| 打印优化 | `@media print` 隐藏交互、显示答案、强制白底黑字 |

---

## 文档

| 文档 | 说明 |
|:----|:----|
| [SPEC.md](SPEC.md) | 课程规格文档 |
| [docs/architecture.md](docs/architecture.md) | 技术架构 |
| [docs/deployment.md](docs/deployment.md) | 部署指南 |
| [docs/user-guide.md](docs/user-guide.md) | 用户使用指南 |
| [docs/changelog.md](docs/changelog.md) | 变更日志 |
| [docs/status-report.md](docs/status-report.md) | 状态报告 |

---

## 教师讲解文本

每个版本的 `scripts/` 目录中包含按课编号的教师讲稿（Markdown 格式），共 52 份，供授课教师备课参考。

| 版本 | 文件数 | 路径示例 |
|:----|:------:|:--------|
| 精简版 standard-5 | 5 份 | `standard-5/scripts/第1课-讲解文本.md` |
| 完整版 standard-15 | 15 份 | `standard-15/scripts/第1课-讲解文本.md` |
| 实验版 lab-10 | 10 份 | `lab-10/scripts/第1课-讲解文本.md` |
| 创造营 app-inventor-10 | 10 份 | `app-inventor-10/scripts/第1课-讲解文本.md` |
| 网站工坊 web-ai-12 | 12 份 | `web-ai-12/scripts/第1课-讲解文本.md` |

每份讲稿包含：教学目标、课时建议、教学流程（含时间分配）、导入环节、核心概念讲解（含类比/故事/例子）、互动/实操环节指导、常见学生提问与应答建议、总结与回顾、课后延伸。

---

## 许可证

[MIT License](LICENSE)
