# 变更日志 / Changelog

> 最后更新: 2026-04-01 11:00 +0800

本文件记录项目的所有重要变更，格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

---

## [v1.4.0] — 2026-04-01

### 新增 (Added)

#### 教师讲解文本 (Teaching Scripts) — 52 份

为全部五个版本的每一课添加了教师讲解文本（Markdown 格式），放置在各版本的 `scripts/` 目录中：

| 版本 | 文件数 | 目录 | 总大小 |
|:----|:------:|:-----|:------:|
| 精简版 standard-5 | 5 份 | `standard-5/scripts/` | 76 KB |
| 完整版 standard-15 | 15 份 | `standard-15/scripts/` | 124 KB |
| 实验版 lab-10 | 10 份 | `lab-10/scripts/` | 100 KB |
| 创造营 app-inventor-10 | 10 份 | `app-inventor-10/scripts/` | 84 KB |
| 网站工坊 web-ai-12 | 12 份 | `web-ai-12/scripts/` | 128 KB |

每份讲稿内容结构：
- 课程标题与教学目标
- 课时建议与教学流程（含时间分配表）
- 导入环节（开场白与引入方式）
- 核心概念讲解（含类比、故事、例子、过渡语）
- 互动/实操环节指导（含引导提问与学生活动）
- 常见学生提问与应答建议
- 总结与回顾、课后延伸

#### 文档对齐
- README.md 新增"教师讲解文本"章节，目录结构添加 scripts/ 目录
- AGENTS.md 项目结构添加 scripts/ 目录
- user-guide.md 新增教师讲稿使用指南
- architecture.md 更新文件结构与代码量统计
- status-report.md 更新至 v1.4.0 统计数据
- changelog.md 补充 v1.4.0 变更记录

---

## [v1.3.0] — 2026-03-31

### 新增 (Added)

#### AI 网站工坊 (web-ai-12) — 12 课时新版本
- 全新 12 课 Web 开发 + AI 集成课程，适合 12–16 岁
- 技术栈: HTML / CSS / JavaScript + OpenAI / Claude API
- 课程内容: HTML 基础 → CSS 美化 → JavaScript 入门 → API 调用 → AI 聊天助手 → AI 图像生成 → 部署上线 → Demo Day
- 每课 5 道测验题（共 60 题），全部支持中英双语
- 门户页面新增第 5 张版本卡片（粉色 badge）
- 网格布局升级为 5 列，响应式断点调整（1300px / 900px / 600px）

#### 文档对齐
- README.md 更新为五大版本，新增 app-inventor-10 和 web-ai-12 课表
- user-guide.md 新增两个版本的简介
- status-report.md 更新至最新统计数据（58 HTML / 52 课 / 6,277 测试）
- architecture.md 更新文件结构、代码量统计、测试套件数据
- changelog.md 补充 v1.2.2 和 v1.3.0 变更记录

#### 测试
- 5 个测试文件新增 web-ai-12 版本覆盖
- test_html_structure.py 新增 app-inventor-10 和 web-ai-12 文件存在性测试
- test_content_completeness.py 新增 web-ai-12 课时数验证（12 课）
- 测试总数: 3,707 → 6,277（+67%）

---

## [v1.2.2] — 2026-03-31

### 新增 (Added)

#### AI App 创造营 (app-inventor-10) — 10 课时新版本
- 全新 10 课 MIT App Inventor + AI API 课程，适合 10–14 岁
- 课程内容: App Inventor 入门 → 天气 API → ChatGPT/Gemini 聊天助手 → 图像识别 → 语音 AI → 设计工作坊 → 构建调试 → Demo Day
- 每课 5 道测验题（共 50 题），全部支持中英双语
- 门户页面新增第 4 张版本卡片（琥珀色 badge）
- 网格布局从 3 列升级为 4 列

#### 测试
- 5 个测试文件新增 app-inventor-10 版本覆盖
- test_content_completeness.py 新增课时数验证（10 课）

---

## [v1.2.1] — 2026-03-27

### 新增 (Added)

#### 测验系统增强
- **正确率统计** — 答题完成后显示正确率百分比（如"正确率：80%"）
- **智能反馈** — 根据正确率显示不同反馈消息：
  - 100% 全对 → 绿色鼓励："太棒了！全部答对，你已经完全掌握了这节课的内容！"
  - 60%–99% → 普通提示："完成测验！继续学习下一课吧。"
  - < 60% → 红色建议："正确率较低，建议重新学习本课内容后再试一次哦！"
- **提交按钮** — 答第一题后出现"提交测验"按钮，支持部分答题后提交
- **漏答提示** — 未作答的题目按错误计分，提交时显示橙色警告："你有 X 道题未作答，未作答的题目按错误计分。"
- 所有反馈消息支持中英双语

#### CSS
- 新增 `.quiz-accuracy`、`.quiz-feedback`、`.quiz-feedback.feedback-perfect`、`.quiz-feedback.feedback-low`、`.quiz-submit-btn`、`.quiz-unanswered-warning` 样式

#### 文档
- 全部文档更新至 v1.2.1 状态，对齐当前项目实际情况

---

## [v1.1.0] — 2026-03-26

### 新增 (Added)

#### 可访问性改进 (UI/UX Audit)
- **Skip Link** — 全站 34 个页面添加 "跳到主要内容" 链接，Tab 聚焦时显示
- **`:focus-visible` 样式** — 统一 2px indigo 轮廓 + 按钮额外 glow 阴影
- **`:active` 触摸反馈** — 卡片 `scale(0.98)`、按钮 `scale(0.96)`，触屏设备有按压反馈
- **`prefers-reduced-motion`** — 尊重系统动效偏好，禁用所有动画、过渡和 hover 位移
- **ARIA 属性** — expandable-card 添加 `role="button"` / `tabindex="0"` / `aria-expanded`；timeline-card 添加 `role="button"` / `tabindex="0"`
- **键盘交互** — expandable-card 和 timeline-card 支持 Enter/Space 键操作
- **nav-portal 暗色模式** — 深蓝硬编码颜色改为暗色模式适配 (`#93c5fd`)
- **暗色模式对比度提升** — `--c-text-secondary` 从 `#94a3b8` 提升至 `#a1b5cc`
- **SVG 笔触统一** — 全站 theme-toggle 图标 `stroke-width` 从 `2` 统一为 `1.5`
- **UI/UX 审查报告** — `docs/ui-ux-audit.md`，基于 ui-ux-pro-max skill 生成

#### 工具链
- **ui-ux-pro-max skill** — 安装于 `.devin/skills/ui-ux-pro-max/`，提供设计智能搜索（67 种风格、96 配色、57 字体、99 UX 规则、25 图表类型）

#### 测试
- 新增 skip-link、`:focus-visible`、`prefers-reduced-motion`、ARIA 属性、`:active` 状态、暗色模式 nav-portal、SVG stroke-width 统一性等测试用例

#### 导航
- 全站 30 个课程页 + 3 个版本主页添加 "全部课程" portal 导航按钮（深蓝色系，12px 图标 + 12px 文字）

### 修复 (Fixed)
- lab-10 lessons 1-8 代码块结构修复（从 `<pre><code>` 改为正确的 `.code-block` 组件结构）
- lab-10 lessons 1-8 quiz-result 空盒子修复（添加 `hidden` class）
- serve.py 端口改为 4200 并添加 no-cache headers

---

## [v1.0.0] — 2026-03-26

### 新增 (Added)

#### 课程内容
| 课程   | 章节数 | 测验题数 | 交互组件                                       |
|:------|:------:|:-------:|:----------------------------------------------|
| 第 1 课 |   6    |    5    | 交互式时间线、AI 还是人类鉴别游戏                 |
| 第 2 课 |   6    |    5    | 决策树互动、Python 代码展示                      |
| 第 3 课 |   7    |    5    | 可展开卡片、TF Playground / Teachable Machine   |
| 第 4 课 |   8    |    5    | Prompt 挑战练习、AIGC 全景卡片                   |
| 第 5 课 |   8    |   10    | 案例展开卡片、AI 产品设计练习、课程总结            |

#### 基础架构
- 项目规格文档 `SPEC.md` (v1.2, 544 行)
- 课程首页 `index.html` — Hero 区域 + 特性卡片 + 5 课导航
- 全局样式 `css/style.css` — 1,319 行, 23 个 CSS 模块
- 全局脚本 `js/main.js` — 385 行, 12 个功能模块, IIFE 封装

#### 功能特性
- 中英双语切换 (`data-lang` + CSS 可见性)
- 暗色/亮色主题切换 (CSS 自定义属性 + `data-theme`)
- 系统主题偏好检测 (`prefers-color-scheme`)
- 学习进度保存 (localStorage)
- 首页进度状态显示
- 响应式布局 (375px / 768px / 1024px / 1440px)
- 移动端汉堡菜单
- 滚动入场动画 (IntersectionObserver)
- 代码块一键复制 (Clipboard API)
- 打印友好样式 (`@media print`)

#### 交互组件 (7 种)
- Quiz 测验系统 — 单选、即时反馈、解释、计分
- 交互式时间线 — 滚动淡入、点击展开详情
- 决策树 — 是/否问题分类、路径显示、重新开始
- AI 鉴别游戏 — 猜测 AI/人类、揭示答案、总分
- Prompt 挑战 — 文本输入、参考答案展开
- 可展开卡片 — 折叠/展开详细内容
- 代码展示块 — 语法高亮、复制、输出展示

#### 测试体系
- 7 个测试套件, 744 个测试用例
- 测试总运行器 `test/run_all.py`
- HTML 可视化报告 `test/reports/report.html`
- JSON 汇总报告 `test/reports/summary.json`

| 测试套件                    | 测试数 | 状态   |
|:--------------------------|:------:|:------:|
| HTML Structure             |   102  | PASS   |
| Content Completeness       |   118  | PASS   |
| Navigation & Links         |    96  | PASS   |
| Bilingual Coverage         |   229  | PASS   |
| CSS Component Coverage     |    63  | PASS   |
| JavaScript Functionality   |    63  | PASS   |
| Accessibility              |    73  | PASS   |

#### 文档
- `README.md` — 项目说明
- `docs/deployment.md` — 部署指南
- `docs/user-guide.md` — 用户使用指南
- `docs/architecture.md` — 技术架构文档
- `docs/project-intro.html` — 项目介绍幻灯片 (12 页)
- `docs/changelog.md` — 变更日志 (本文件)
- `docs/chat-history.md` — 开发对话记录
- `docs/status-report.md` — 当前状态报告

### 修复 (Fixed)

- 修复 lesson2.html / lesson4.html / lesson5.html 中 `lang-toggle` 按钮缺失 `aria-label` 属性的问题

---

## [v0.1.0] — 2026-03-25

### 新增 (Added)

- 初始项目结构搭建
- SPEC.md 规格文档 v1.0
- 基础 HTML 骨架
- CSS 设计系统 (设计 Token、颜色、字体、间距)
- JavaScript 核心功能框架

---

## 版本规划

| 版本   | 计划时间      | 主要内容                                              |
|:------|:------------|:-----------------------------------------------------|
| v1.0  | 2026-03-26  | 全部 5 课内容、交互组件、测试套件、文档                    |
| v1.1  | 2026-03-26  | 多版本架构、UI/UX 审查改进、可访问性增强                   |
| v1.2.1| 2026-03-27  | 测验系统增强（正确率、智能反馈、提交按钮、漏答提示）         |
| v1.2.2| 2026-03-31  | AI App 创造营 (app-inventor-10) 10 课时新版本            |
| v1.3.0| 2026-03-31  | AI 网站工坊 (web-ai-12) 12 课时新版本 + 文档测试对齐 |
| v1.4.0| 2026-04-01  | 教师讲解文本 52 份 + 文档对齐 (当前版本)              |
| v2.0  | 待定        | W3C 验证、跨浏览器测试、课程图片资源、SEO 优化            |
| v3.0  | 待定        | 嵌入 Python 运行环境、教师管理面板、数据分析仪表盘         |

---

*文档版本: v1.4 | 最后更新: 2026-04-01 11:00 +0800*
