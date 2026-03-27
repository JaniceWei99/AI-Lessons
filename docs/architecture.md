# 技术架构文档 / Architecture

> 最后更新: 2026-03-27 12:00 +0800

---

## 目录

1. [架构概览](#1-架构概览)
2. [技术选型](#2-技术选型)
3. [文件架构](#3-文件架构)
4. [页面结构](#4-页面结构)
5. [CSS 架构](#5-css-架构)
6. [JavaScript 架构](#6-javascript-架构)
7. [双语系统](#7-双语系统)
8. [主题系统](#8-主题系统)
9. [数据持久化](#9-数据持久化)
10. [交互组件架构](#10-交互组件架构)
11. [响应式设计](#11-响应式设计)
12. [性能优化](#12-性能优化)
13. [测试架构](#13-测试架构)

---

## 1. 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                        浏览器 (Client)                       │
│                                                             │
│  ┌──────────┐   ┌───────────┐   ┌────────────────────────┐ │
│  │ HTML x 34│   │ CSS x 1   │   │ JavaScript x 1         │ │
│  │          │   │           │   │                        │ │
│  │ index    │   │ style.css │   │ main.js                │ │
│  │ lesson1  │   │ 25 模块   │   │ 12 功能模块 + Quiz 增强  │ │
│  │ lesson2  │   │ 1491 行   │   │ 486 行                 │ │
│  │ lesson3  │   │           │   │                        │ │
│  │ lesson4  │   │           │   │ ┌────────────────────┐ │ │
│  │ lesson5  │   │           │   │ │   localStorage     │ │ │
│  └──────────┘   └───────────┘   │ │  - theme           │ │ │
│                                  │ │  - lang            │ │ │
│                                  │ │  - progress        │ │ │
│                                  │ └────────────────────┘ │ │
│                                  └────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │               Google Fonts CDN (唯一外部依赖)            ││
│  │               fonts.googleapis.com                      ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**核心设计原则**:
- **零构建** — 纯静态文件，无 Node.js / Webpack / Vite
- **零框架** — 不依赖 React / Vue / Angular
- **单样式表** — 所有样式集中在 `style.css`
- **单脚本** — 所有逻辑集中在 `main.js`
- **数据驻留客户端** — localStorage，无服务端

---

## 2. 技术选型

| 层面           | 选择                                 | 选择理由                                  |
|:--------------|:------------------------------------|:-----------------------------------------|
| 标记语言       | HTML5                               | 原生支持，无构建依赖                        |
| 样式           | CSS3 (自定义属性 + Grid + Flexbox)    | 完全可控，零依赖                            |
| 交互           | Vanilla JavaScript (ES6+)            | 零依赖，便于离线使用                        |
| 字体           | Google Fonts CDN (Noto Sans SC)      | 中文排版优化，回退到 system-ui              |
| 代码字体       | JetBrains Mono / Fira Code           | 等宽字体，代码展示                          |
| 图标           | 内联 SVG                             | 零 HTTP 请求，矢量清晰                     |
| 代码高亮       | 自定义 CSS 类                         | 代码量少，无需引入 Prism / Highlight.js    |
| 数据持久化     | localStorage                         | 浏览器原生 API，简单可靠                    |
| 滚动动画       | IntersectionObserver API             | 原生 API，性能优于 scroll 事件监听           |

### 未采用的方案

| 方案               | 未采用原因                                                |
|:-------------------|:---------------------------------------------------------|
| React / Vue        | 初中生课程无需 SPA，增加复杂度和体积                        |
| Tailwind CSS       | 增加构建步骤，HTML 类名冗长                                |
| Bootstrap          | 体积过大，自定义程度不足                                    |
| Markdown → HTML    | 需要构建步骤，交互组件无法用 Markdown 表达                   |
| 数据库             | 无服务端，localStorage 足够存储个人进度                      |

---

## 3. 文件架构

```
AI-Class/                           # 项目根目录
│
├── index.html                      # [入口] 门户页面 (版本选择器)
│
├── css/
│   └── style.css                   # [唯一样式表] 25 个模块
│
├── js/
│   └── main.js                     # [唯一脚本] IIFE 封装, 12 个功能模块
│
├── standard-5/                     # 精简版 (5 课时)
│   ├── index.html                  # 版本首页
│   └── lessons/                    # lesson1-5.html
│
├── standard-15/                    # 完整版 (15 课时)
│   ├── index.html                  # 版本首页
│   └── lessons/                    # lesson1-15.html
│
├── lab-10/                         # 实验版 (10 实验)
│   ├── index.html                  # 版本首页
│   └── lessons/                    # lesson1-10.html
│
├── assets/images/                  # 图片资源 (可选)
│
├── test/                           # 测试套件
│   ├── run_all.py                  # 测试运行器
│   ├── test_*.py                   # 7 个测试模块
│   └── reports/                    # 自动生成的测试报告
│
└── docs/                           # 项目文档
```

### 代码量统计

| 文件             | 行数    | 说明                          |
|:----------------|:-------:|:------------------------------|
| style.css       | 1,491   | 全局样式，25 个模块             |
| main.js         |   486   | 全局脚本，12 个功能模块          |
| index.html      |   382   | 门户页面 (版本选择器)            |
| standard-5/     | 4,190   | 精简版 5 课 + 版本首页           |
| standard-15/    | 4,371   | 完整版 15 课 + 版本首页          |
| lab-10/         | 4,888   | 实验版 10 课 + 版本首页          |
| **总计**        | **~15,800** | **不含测试和文档**           |

---

## 4. 页面结构

### 通用页面骨架

```html
<!DOCTYPE html>
<html lang="zh-CN" data-lang="zh" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>...</title>
  <link href="https://fonts.googleapis.com/..." rel="stylesheet">
  <link rel="stylesheet" href="[../]css/style.css">
</head>
<body>
  <nav class="nav">        <!-- 固定顶部导航栏 -->
  <section class="hero">   <!-- 课程标题区域 -->
  <div class="content">    <!-- 主内容区域 -->
    <div class="section">  <!-- 各教学段落 -->
    <div class="quiz">     <!-- 小测验 -->
  </div>
  <div class="lesson-nav-footer"> <!-- 上/下一课 -->
  <footer class="footer">  <!-- 页脚 -->
  <script src="[../]js/main.js"></script>
</body>
</html>
```

### 组件嵌套关系

```
page
├── nav
│   ├── nav-logo
│   ├── nav-lessons (课程链接)
│   ├── nav-actions
│   │   ├── lang-toggle
│   │   └── theme-toggle
│   └── nav-hamburger (移动端)
├── hero
│   ├── lesson-tag
│   ├── h1 (标题)
│   └── subtitle
├── content
│   ├── section (×N)
│   │   ├── h2
│   │   ├── p / card-grid / compare / timeline / ...
│   │   └── info-box (可选)
│   └── quiz
│       ├── quiz-question (×N)
│       │   ├── quiz-prompt
│       │   ├── quiz-options > quiz-option (×4)
│       │   └── quiz-explanation
│       └── quiz-result
├── lesson-nav-footer
└── footer
```

---

## 5. CSS 架构

### 设计 Token 体系

所有视觉值通过 CSS 自定义属性 (CSS Variables) 管理，在 `:root` 中定义。

```
:root
├── 颜色 Token
│   ├── --c-primary:       #6366f1   (Indigo 500)
│   ├── --c-primary-light: #a5b4fc   (Indigo 300)
│   ├── --c-primary-dark:  #4f46e5   (Indigo 600)
│   ├── --c-secondary:     #06b6d4   (Cyan 500)
│   ├── --c-accent:        #f59e0b   (Amber 500)
│   ├── --c-success:       #22c55e   (Green 500)
│   ├── --c-error:         #ef4444   (Red 500)
│   ├── --c-bg:            #f8fafc   (Slate 50)
│   ├── --c-card:          #ffffff
│   ├── --c-text:          #1e293b   (Slate 800)
│   └── --c-text-secondary: #64748b  (Slate 500)
│
├── 字体 Token
│   ├── --ff-body: "Noto Sans SC", system-ui, sans-serif
│   └── --ff-code: "JetBrains Mono", "Fira Code", monospace
│
├── 字号 Token (--fs-hero, --fs-h2, --fs-h3, --fs-body, --fs-small)
├── 间距 Token (--sp-xs → --sp-3xl)
├── 圆角 Token (--radius-sm, --radius-md, --radius-lg)
├── 阴影 Token (--shadow-sm, --shadow-md, --shadow-lg)
└── 过渡 Token (--tr-fast, --tr-base, --tr-slow)
```

### CSS 模块列表

| 序号 | 模块名                 | 职责                                    |
|:----:|:----------------------|:----------------------------------------|
|   0  | CSS Custom Properties  | 设计 Token 定义                          |
|   1  | Bilingual Toggle       | `[data-lang] .zh / .en` 切换            |
|   2  | Reset & Base           | 全局重置和基础排版                        |
|   3  | Navigation             | 固定顶部导航栏 + 移动端汉堡菜单            |
|   4  | Hero                   | 课程标题横幅区域                          |
|   5  | Content Layout         | `.content` / `.section` 布局             |
|   6  | Cards                  | 通用卡片 / 课程卡片 / 图标卡片 / 对比卡片   |
|   7  | Timeline               | 垂直交互时间线                            |
|   8  | Quiz                   | 测验题目 / 选项 / 反馈 / 得分              |
|   9  | Decision Tree          | 决策树节点 / 按钮 / 路径                   |
|  10  | AI or Human            | AI 鉴别互动卡片                           |
|  11  | Prompt Challenge       | Prompt 输入 / 参考答案                    |
|  12  | Expandable Card        | 折叠/展开卡片                             |
|  13  | Code Block             | 代码展示 + 语法着色 + 复制按钮             |
|  14  | Steps                  | 步骤编号列表                              |
|  15  | Info/Tip/Warning Boxes | 信息提示框                                |
|  16  | Lesson Footer Nav      | 上/下一课导航                             |
|  17  | Footer                 | 页脚                                     |
|  18  | Feature Grid           | 首页特性卡片网格                           |
|  19  | Scroll Animation       | `.reveal` 滚动入场                        |
|  20  | Utility                | `.hidden`, `.text-center`, 间距工具类      |
|  21  | Responsive             | 768px / 1024px 断点                       |
|  22  | Homepage Aliases       | 首页特定样式                              |
|  23  | Print                  | `@media print` 打印优化                   |

---

## 6. JavaScript 架构

### 整体结构

```javascript
(function () {
  'use strict';

  // 0. Constants (STORAGE_KEYS)
  // 1. Theme        — initTheme() / applyTheme()
  // 2. Language     — initLang() / applyLang()
  // 3. Progress     — getProgress() / saveProgress() / markLessonQuiz() / updateProgressUI()
  // 4. Quiz         — initQuizzes() / showQuizResult() + 提交按钮 + 正确率反馈
  // 5. Decision Tree — initDecisionTrees() / showTreePath()
  // 6. AI or Human  — initAIorHuman()
  // 7. Prompt       — initPromptChallenge()
  // 8. Expandable   — initExpandableCards()
  // 9. Code Copy    — initCodeCopy()
  // 10. Scroll      — initScrollReveal()
  // 11. Mobile Nav  — initMobileNav()
  // 12. Timeline    — initTimeline()

  function init() { /* 调用所有 initXxx() */ }

  // DOM Ready 后执行 init()
})();
```

### 设计决策

| 决策                     | 理由                                              |
|:------------------------|:--------------------------------------------------|
| IIFE 封装               | 避免全局变量污染                                    |
| `'use strict'`          | 启用严格模式，捕获隐式错误                           |
| 无 ES Module            | 兼容直接打开 HTML（file:// 协议不支持 module）        |
| `document.querySelectorAll` | 无 jQuery 依赖，原生 API 足够                   |
| IntersectionObserver    | 比 scroll 事件监听性能更好                           |
| navigator.clipboard     | 现代剪贴板 API，比 `document.execCommand` 更可靠     |
| localStorage            | 简单键值存储，无需后端                               |

### 函数清单

| 函数                      | 职责                                              |
|:-------------------------|:--------------------------------------------------|
| `initTheme()`            | 初始化主题，绑定切换按钮，读取 localStorage           |
| `applyTheme(theme)`      | 设置 `data-theme`，切换太阳/月亮图标                 |
| `initLang()`             | 初始化语言，绑定切换按钮                             |
| `applyLang(lang)`        | 设置 `data-lang` 属性                              |
| `getProgress()`          | 从 localStorage 读取进度对象                        |
| `saveProgress(data)`     | 写入进度到 localStorage                             |
| `markLessonQuiz(id,s,t)` | 记录某课测验分数并标记完成                           |
| `updateProgressUI()`     | 更新首页卡片上的完成状态显示                          |
| `initQuizzes()`          | 绑定所有 `.quiz` 组件的点击事件                      |
| `showQuizResult(q,s,t,u)` | 显示测验得分面板（含正确率、智能反馈、漏答提示）|
| `initDecisionTrees()`    | 绑定决策树节点切换                                  |
| `initAIorHuman()`        | 绑定 AI 鉴别游戏点击逻辑                            |
| `initPromptChallenge()`  | 绑定参考答案展开/收起                               |
| `initExpandableCards()`  | 绑定折叠卡片的 open/close                          |
| `initCodeCopy()`         | 绑定代码复制按钮，调用 Clipboard API                 |
| `initScrollReveal()`     | 创建 IntersectionObserver，监听 `.reveal` 元素      |
| `initMobileNav()`        | 绑定汉堡菜单展开/收起                               |
| `initTimeline()`         | 绑定时间线卡片详情展开                               |

---

## 7. 双语系统

### 实现原理

```
HTML:   <h2><span class="zh">标题</span><span class="en">Title</span></h2>
CSS:    [data-lang="zh"] .en { display: none !important; }
        [data-lang="en"] .zh { display: none !important; }
JS:     document.documentElement.setAttribute('data-lang', 'en');
存储:   localStorage.setItem('ai-class-lang', 'en');
```

### 数据流

```
用户点击 "EN" 按钮
  → JS: applyLang('en')
    → 设置 html[data-lang="en"]
    → CSS 自动隐藏 .zh, 显示 .en
  → JS: localStorage.setItem('ai-class-lang', 'en')
    → 下次加载自动读取
```

---

## 8. 主题系统

### 实现原理

```
CSS:    :root          { --c-bg: #f8fafc; --c-text: #1e293b; ... }
        [data-theme="dark"] { --c-bg: #0f172a; --c-text: #e2e8f0; ... }
JS:     document.documentElement.setAttribute('data-theme', 'dark');
首次:   读取 prefers-color-scheme → 设为默认
存储:   localStorage.setItem('ai-class-theme', 'dark');
```

### 优先级

```
localStorage 已保存  →  使用保存的值
localStorage 未保存  →  读取 prefers-color-scheme
系统无偏好          →  默认 light
```

---

## 9. 数据持久化

### localStorage 结构

```json
{
  "ai-class-lang": "zh",
  "ai-class-theme": "dark",
  "ai-class-progress": {
    "lesson1": { "completed": true,  "quizScore": 4, "quizTotal": 5  },
    "lesson2": { "completed": true,  "quizScore": 5, "quizTotal": 5  },
    "lesson3": { "completed": false, "quizScore": null, "quizTotal": null }
  }
}
```

| Key                   | 类型   | 说明                     |
|:----------------------|:------:|:------------------------|
| `ai-class-lang`       | string | 当前语言 (`"zh"` / `"en"`) |
| `ai-class-theme`      | string | 当前主题 (`"light"` / `"dark"`) |
| `ai-class-progress`   | JSON   | 各课完成状态和测验分数     |

---

## 10. 交互组件架构

| 组件              | HTML 入口类          | JS 初始化函数              | 事件                     |
|:-----------------|:-------------------|:-------------------------|:------------------------|
| Quiz             | `.quiz`            | `initQuizzes()`          | click on `.quiz-option`, `.quiz-submit-btn` |
| Decision Tree    | `.decision-tree`   | `initDecisionTrees()`    | click on `.tree-btn`     |
| AI or Human      | `.ai-or-human`     | `initAIorHuman()`        | click on `.aoh-btn`      |
| Prompt Challenge | `.prompt-challenge` | `initPromptChallenge()`  | click on `.pc-reveal-btn` |
| Expandable Card  | `.expandable-card` | `initExpandableCards()`  | click on `.ec-header`    |
| Code Copy        | `.code-block`      | `initCodeCopy()`         | click on `.code-copy-btn` |
| Timeline         | `.timeline-card`   | `initTimeline()`         | click on card            |
| Scroll Reveal    | `.reveal`          | `initScrollReveal()`     | IntersectionObserver     |

所有组件遵循统一模式：
1. HTML 中通过 CSS class 和 `data-*` 属性声明结构和数据
2. JS 中通过 `querySelectorAll` 查找所有实例
3. 为每个实例绑定 `click` 事件
4. 通过 `classList.add/remove/toggle` 控制状态

---

## 11. 响应式设计

### 断点策略

| 断点              | 目标设备     | 主要变化                                  |
|:-----------------|:------------|:-----------------------------------------|
| >= 1024px        | 桌面/笔记本  | 完整导航栏、多列网格、标准字号              |
| 768px – 1023px   | 平板         | 4 列 → 2 列、字号缩小                     |
| < 768px          | 手机         | 单列布局、汉堡菜单、底部导航竖排            |

### 移动端自适应清单

| 组件            | 桌面              | 移动端                   |
|:---------------|:-----------------|:------------------------|
| 导航栏课程链接   | 水平排列           | 汉堡菜单下拉              |
| 卡片网格        | 2–4 列            | 1 列                    |
| 对比卡片        | 左右并排           | 上下堆叠                 |
| 决策树按钮      | 水平排列           | 垂直排列                 |
| AI 鉴别按钮     | 水平排列           | 垂直排列                 |
| 底部课程导航    | 左右两端           | 垂直居中                 |

---

## 12. 性能优化

| 优化策略                  | 实现方式                                           |
|:------------------------|:--------------------------------------------------|
| 零 JavaScript 依赖      | 不引入 jQuery / React / lodash，原生实现              |
| 零 CSS 框架             | 不引入 Bootstrap / Tailwind，手写精简 CSS             |
| 内联 SVG 图标           | 零额外 HTTP 请求                                    |
| IntersectionObserver    | 替代 scroll 事件，减少主线程负担                       |
| CSS 过渡优先于 JS 动画   | 利用 GPU 加速的 CSS transform / opacity              |
| 字体 preconnect         | `<link rel="preconnect">` 加速 Google Fonts 连接     |
| 手动语法着色             | 不引入 Prism.js / Highlight.js，节省 ~30 KB          |

---

## 13. 测试架构

### 测试栈

| 工具                 | 用途                              |
|:--------------------|:---------------------------------|
| Python 3.10+        | 测试脚本运行环境                   |
| uv                  | 依赖管理和脚本运行                  |
| beautifulsoup4      | HTML 解析和结构检查                 |
| lxml                | BS4 的 HTML 解析引擎               |

### 测试套件

| 套件                      | 测试数 | 检查内容                                |
|:-------------------------|:------:|:---------------------------------------|
| HTML Structure            |   646  | DOCTYPE、meta、nav、footer、data 属性   |
| Content Completeness      |   224  | 章节数、Quiz 题数、交互组件、关键词        |
| Navigation & Links        |   754  | 内部链接有效性、上下课导航                |
| Bilingual Coverage        | 1,343  | 标题/按钮/Quiz/导航/页脚双语覆盖          |
| CSS Component Coverage    |    69  | 设计 Token、暗色模式、响应式、打印样式     |
| JavaScript Functionality  |    63  | 函数存在性、IIFE、事件绑定、存储键         |
| Accessibility             |   608  | ARIA 标签、语义 HTML、键盘可访问性        |
| **总计**                  | **3,707** |                                     |

### 运行与报告

```bash
uv run test/run_all.py
# 输出: test/reports/report.html  (可视化报告)
#       test/reports/summary.json (机器可读汇总)
#       test/reports/*.json       (各套件详细报告)
```

---

*文档版本: v1.1 | 最后更新: 2026-03-27 12:00 +0800*
