# 课程维护指南 / Course Maintenance Guide

> 最后更新: 2026-04-01 12:00 +0800

本文档面向需要**手动编辑课程内容**的维护人员，详细说明如何修改现有课程、新增课程、删减课程，以及 HTML 页面的编写规范。

---

## 目录

1. [快速概览：文件与影响范围](#1-快速概览文件与影响范围)
2. [场景一：修改现有课程内容](#2-场景一修改现有课程内容)
3. [场景二：新增一课](#3-场景二新增一课)
4. [场景三：删减一课](#4-场景三删减一课)
5. [HTML 编写规范](#5-html-编写规范)
6. [双语系统](#6-双语系统)
7. [页面整体结构](#7-页面整体结构)
8. [可用组件参考](#8-可用组件参考)
9. [版本首页（edition index）编辑](#9-版本首页edition-index编辑)
10. [导航与链接规则](#10-导航与链接规则)
11. [讲稿编辑](#11-讲稿编辑)
12. [修改后的验证清单](#12-修改后的验证清单)
13. [提交与发布](#13-提交与发布)

---

## 1. 快速概览：文件与影响范围

### 1.1 每个版本的文件布局

以 `standard-5` 为例（其他版本结构完全相同）：

```
standard-5/
├── index.html              ← 版本首页（课程列表）
├── lessons/
│   ├── lesson1.html        ← 第 1 课页面
│   ├── lesson2.html
│   ├── lesson3.html
│   ├── lesson4.html
│   └── lesson5.html        ← 最后一课
└── scripts/
    ├── 第1课-讲解文本.md    ← 第 1 课教师讲稿
    ├── 第2课-讲解文本.md
    ├── 第3课-讲解文本.md
    ├── 第4课-讲解文本.md
    └── 第5课-讲解文本.md
```

### 1.2 三种操作的影响范围

| 操作 | 需要修改的文件 | 需要更新的文档 |
|:-----|:-------------|:-------------|
| **改内容**（只改某课的文字/图片） | `lessons/lessonX.html`、`scripts/第X课-讲解文本.md` | 小改动无需更新；大改动建议更新 `docs/changelog.md` |
| **新增一课** | 见 [第 3 节](#3-场景二新增一课)，共 5~8 个文件 | `README.md`、`docs/changelog.md`、`docs/status-report.md` |
| **删减一课** | 见 [第 4 节](#4-场景三删减一课)，共 4~7 个文件 | `README.md`、`docs/changelog.md`、`docs/status-report.md` |

### 1.3 全局共享文件（一般不需要修改）

| 文件 | 作用 | 何时需要改 |
|:-----|:----|:----------|
| `css/style.css` | 所有页面的样式 | 需要新的视觉组件或改配色时 |
| `js/main.js` | 所有页面的交互逻辑 | 需要新的交互组件类型时 |
| `index.html`（根目录） | 门户首页（版本选择器） | 新增/删除整个版本时 |

---

## 2. 场景一：修改现有课程内容

这是最常见的操作——修改某课的文字、替换例子、调整措辞等。

### 2.1 需要改的文件

| # | 文件 | 说明 |
|:-:|:-----|:----|
| 1 | `{版本}/lessons/lessonX.html` | 课程页面 — 改中英文内容 |
| 2 | `{版本}/scripts/第X课-讲解文本.md` | 教师讲稿 — 同步更新 |

### 2.2 操作步骤

1. **打开目标 HTML 文件**，找到要修改的 `<section>`
2. **同时修改中文和英文**（每段文字都有 `<span class="zh">` 和 `<span class="en">`，两个都要改）
3. **同步更新讲稿**（`scripts/第X课-讲解文本.md`）中对应的内容
4. **在浏览器中预览**（`python3 serve.py` 然后访问 `http://localhost:4200`）
5. 切换中/英文、亮/暗模式确认显示正常

### 2.3 示例：修改一段文字

**改之前：**
```html
<p>
  <span class="zh">抖音、B站、小红书为你推荐喜欢的内容</span>
  <span class="en">TikTok, YouTube, and Instagram recommend content you'll love</span>
</p>
```

**改之后：**
```html
<p>
  <span class="zh">抖音、B站、小红书、YouTube 为你推荐喜欢的内容</span>
  <span class="en">TikTok, YouTube, Instagram, and Bilibili recommend content you'll love</span>
</p>
```

> **注意：** 只改 `<span>` 里面的文字，不要动外面的标签和 class。

---

## 3. 场景二：新增一课

以「给 `standard-5` 新增第 6 课」为例，说明完整步骤。

### 3.1 需要创建的文件

| # | 文件 | 来源 |
|:-:|:-----|:----|
| 1 | `standard-5/lessons/lesson6.html` | 复制 `lesson5.html`，修改内容 |
| 2 | `standard-5/scripts/第6课-讲解文本.md` | 复制第 5 课讲稿，修改内容 |

### 3.2 需要修改的文件

| # | 文件 | 修改内容 |
|:-:|:-----|:--------|
| 3 | `standard-5/index.html` | 在导航栏和课程列表中添加第 6 课 |
| 4 | `standard-5/lessons/lesson5.html` | 原最后一课：底部导航改为指向 `lesson6.html` |
| 5 | `standard-5/lessons/lesson6.html` | 新最后一课：底部导航指向首页 |
| 6 | **所有课程页面** `lesson1~5.html` | 顶部导航栏 `<nav>` 中添加第 6 课链接 |

### 3.3 需要更新的文档

| # | 文件 | 修改内容 |
|:-:|:-----|:--------|
| 7 | `README.md` | 课程列表加一行、目录结构中课数更新 |
| 8 | `docs/changelog.md` | 新增版本记录 |
| 9 | `docs/status-report.md` | 文件统计更新 |

### 3.4 详细步骤

#### 步骤 1：创建新课程页面

复制最后一课作为模板：

```bash
cp standard-5/lessons/lesson5.html standard-5/lessons/lesson6.html
```

打开 `lesson6.html`，修改以下区域：

**a) `<head>` 中的标题和描述：**
```html
<meta name="description" content="第6课：新课标题 | Lesson 6: New Lesson Title">
<title>第6课：新课标题 | Lesson 6: New Lesson Title</title>
```

**b) 顶部导航栏 — 添加第 6 课并标记为 active：**
```html
<div class="nav-lessons">
  <a href="lesson1.html"><span class="zh">第1课</span><span class="en">L1</span></a>
  <a href="lesson2.html"><span class="zh">第2课</span><span class="en">L2</span></a>
  <a href="lesson3.html"><span class="zh">第3课</span><span class="en">L3</span></a>
  <a href="lesson4.html"><span class="zh">第4课</span><span class="en">L4</span></a>
  <a href="lesson5.html"><span class="zh">第5课</span><span class="en">L5</span></a>
  <a href="lesson6.html" class="active"><span class="zh">第6课</span><span class="en">L6</span></a>
</div>
```

**c) Hero 区域：**
```html
<section class="hero">
  <div class="hero-inner">
    <span class="lesson-tag">
      <span class="zh">第 6 课</span>
      <span class="en">Lesson 6</span>
    </span>
    <h1>
      <span class="zh">新课标题</span>
      <span class="en">New Lesson Title</span>
    </h1>
    <p class="subtitle">
      <span class="zh">副标题描述</span>
      <span class="en">Subtitle description</span>
    </p>
  </div>
</section>
```

**d) 正文内容：** 替换所有 `<section>` 的内容（section id 改为 `section-6-1`、`section-6-2` 等）

**e) 底部导航（新的最后一课）：**
```html
<div class="lesson-nav-footer">
  <a href="lesson5.html">
    <span class="zh">← 上一课：AI 的未来与责任</span>
    <span class="en">← Previous: The Future & Ethics of AI</span>
  </a>
  <a href="../index.html">
    <span class="zh">回到首页 →</span>
    <span class="en">Back to Home →</span>
  </a>
</div>
```

#### 步骤 2：修改原最后一课 (lesson5.html)

将 `lesson5.html` 底部导航从"回到首页"改为"下一课"：

```html
<!-- 改之前 -->
<div class="lesson-nav-footer">
  <a href="lesson4.html">
    <span class="zh">← 上一课：大语言模型与AIGC</span>
    <span class="en">← Previous: LLMs &amp; AI-Generated Content</span>
  </a>
  <a href="../index.html">
    <span class="zh">回到首页 →</span>
    <span class="en">Back to Home →</span>
  </a>
</div>

<!-- 改之后 -->
<div class="lesson-nav-footer">
  <a href="lesson4.html">
    <span class="zh">← 上一课：大语言模型与AIGC</span>
    <span class="en">← Previous: LLMs &amp; AI-Generated Content</span>
  </a>
  <a href="lesson6.html">
    <span class="zh">下一课：新课标题 →</span>
    <span class="en">Next: New Lesson Title →</span>
  </a>
</div>
```

同时，如果 `lesson5.html` 的 footer 中有"恭喜完成课程"的文字，将其移除（挪到新的最后一课）。

#### 步骤 3：更新所有课程的顶部导航栏

**每一个** `lesson1.html` ~ `lesson5.html` 的 `<nav>` 部分都需要添加第 6 课的链接：

```html
<div class="nav-lessons">
  <a href="lesson1.html" class="active">...</a>  <!-- 当前课加 class="active" -->
  <a href="lesson2.html">...</a>
  <a href="lesson3.html">...</a>
  <a href="lesson4.html">...</a>
  <a href="lesson5.html">...</a>
  <a href="lesson6.html"><span class="zh">第6课</span><span class="en">L6</span></a>  <!-- 新增 -->
</div>
```

> **重要：** 只有当前课程的链接带 `class="active"`，其他课程不带。

#### 步骤 4：更新版本首页 (standard-5/index.html)

**a) 导航栏添加链接：**
```html
<div class="nav-lessons">
  <!-- ...现有课程... -->
  <a href="lessons/lesson6.html"><span class="zh">第6课</span><span class="en">L6</span></a>
</div>
```

**b) 课程列表添加卡片：**
```html
<!-- Lesson 6 -->
<div class="lesson-card" data-lesson="lesson6">
  <span class="lesson-number">06</span>
  <h3 class="lesson-title">
    <span class="zh">新课标题</span>
    <span class="en">New Lesson Title</span>
  </h3>
  <p class="lesson-desc">
    <span class="zh">这一课你将学到什么</span>
    <span class="en">What you'll learn in this lesson</span>
  </p>
  <span class="lesson-status hidden"><span class="zh"></span><span class="en"></span></span>
  <a href="lessons/lesson6.html" class="lesson-btn">
    <span class="zh">开始学习</span>
    <span class="en">Start</span>
  </a>
</div>
```

#### 步骤 5：创建讲稿

```bash
cp standard-5/scripts/第5课-讲解文本.md standard-5/scripts/第6课-讲解文本.md
```

修改讲稿内容，保持格式一致：课程标题、教学目标、课时建议、教学流程、导入环节、核心概念讲解、互动环节、常见提问与应答、总结与回顾、课后延伸。

---

## 4. 场景三：删减一课

以「从 `standard-5` 删除第 3 课」为例。

### 4.1 需要删除的文件

| # | 文件 |
|:-:|:-----|
| 1 | `standard-5/lessons/lesson3.html` |
| 2 | `standard-5/scripts/第3课-讲解文本.md` |

### 4.2 需要修改的文件

| # | 文件 | 修改内容 |
|:-:|:-----|:--------|
| 3 | `standard-5/index.html` | 从导航栏和课程列表中移除第 3 课 |
| 4 | 被删课**前面**的课 (`lesson2.html`) | 底部"下一课"链接从 `lesson3.html` 改为 `lesson4.html` |
| 5 | 被删课**后面**的课 (`lesson4.html`) | 底部"上一课"链接从 `lesson3.html` 改为 `lesson2.html` |
| 6 | **所有剩余课程** `lesson1/2/4/5.html` | 顶部导航栏移除第 3 课链接 |

### 4.3 需要更新的文档

同新增课程：`README.md`、`docs/changelog.md`、`docs/status-report.md`

### 4.4 重要提示

- **是否重新编号**：建议保持原有文件名（`lesson1, lesson2, lesson4, lesson5`），避免大范围重命名导致链接混乱。如果确实需要重新编号（改为连续的 1-4），则所有文件的文件名、导航链接、section id、quiz id 都需要同步修改。
- **重新编号的工作量**很大，一般不推荐，除非课程还处于开发初期。

---

## 5. HTML 编写规范

### 5.1 基本规则

| 规则 | 说明 |
|:-----|:----|
| **双语必须成对** | 每个文字元素都必须同时包含 `<span class="zh">` 和 `<span class="en">` |
| **保留 CSS class** | 不要修改或删除组件上的 class 名，否则样式会丢失 |
| **section id 不重复** | 格式为 `section-{课号}-{节号}`，例如 `section-3-2` |
| **quiz id 不重复** | 格式为 `data-quiz-id="lesson{课号}"`，例如 `lesson3` |
| **使用相对路径** | 课程文件引用 CSS/JS：`../../css/style.css`、`../../js/main.js` |
| **SVG 图标来源** | 统一使用 [Heroicons](https://heroicons.com/)（stroke 风格，`stroke-width="1.5"`） |
| **不要内联样式** | 所有样式通过 CSS class 控制，不要写 `style="..."` |

### 5.2 缩进与格式

- 使用 **2 个空格**缩进（不要用 Tab）
- HTML 标签小写
- 属性值用双引号

---

## 6. 双语系统

### 6.1 工作原理

```
用户点击 "EN" 按钮
  → JS 设置 <html data-lang="en">
  → CSS 规则 [data-lang="en"] .zh { display: none }
  → 所有 .zh 的 span 隐藏，所有 .en 的 span 显示
  → 偏好保存到 localStorage('ai-class-lang')
```

### 6.2 编写规则

**所有用户可见的文字**都必须用双语 span 包裹：

```html
<!-- 段落 -->
<p>
  <span class="zh">这是中文内容</span>
  <span class="en">This is English content</span>
</p>

<!-- 标题 -->
<h2>
  <span class="zh">1.1 章节标题</span>
  <span class="en">1.1 Section Title</span>
</h2>

<!-- 列表项 -->
<li>
  <span class="zh">列表内容</span>
  <span class="en">List item content</span>
</li>

<!-- 按钮 -->
<button>
  <span class="zh">点击我</span>
  <span class="en">Click Me</span>
</button>

<!-- 带格式的文字 -->
<p>
  <span class="zh"><strong>加粗</strong>和普通文字混合</span>
  <span class="en"><strong>Bold</strong> and normal text mixed</span>
</p>
```

### 6.3 常见错误

```html
<!-- 错误：缺少英文 -->
<p>
  <span class="zh">只写了中文</span>
</p>

<!-- 错误：span 嵌套在错误位置 -->
<p>
  <span class="zh">中文</span>
  <span class="en">English</span>
  多余的没有包裹的文字    <!-- 这行切换语言后会一直显示 -->
</p>

<!-- 正确 -->
<p>
  <span class="zh">中文内容</span>
  <span class="en">English content</span>
</p>
```

---

## 7. 页面整体结构

每个课程 HTML 文件由以下 6 个部分组成，必须按顺序排列：

```html
<!DOCTYPE html>
<html lang="zh-CN" data-lang="zh" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="第X课：标题 | Lesson X: Title">
  <title>第X课：标题 | Lesson X: Title</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../css/style.css">
</head>
<body>

  <!-- ① 无障碍跳转链接 -->
  <a href="#main-content" class="skip-link">
    <span class="zh">跳到主要内容</span>
    <span class="en">Skip to main content</span>
  </a>

  <!-- ② 顶部导航栏 -->
  <nav class="nav">
    <!-- 门户链接 -->
    <a href="../../index.html" class="nav-portal" title="All Courses">
      <svg>...</svg>
      <span class="zh">全部课程</span>
      <span class="en">Courses</span>
    </a>
    <!-- 版本 Logo -->
    <a href="../index.html" class="nav-logo">
      <span class="zh">AI 探索之旅</span>
      <span class="en">AI Explorer</span>
    </a>
    <!-- 课程列表 -->
    <div class="nav-lessons">
      <a href="lesson1.html" class="active">...</a>   <!-- 当前课带 active -->
      <a href="lesson2.html">...</a>
      <!-- ...更多课程... -->
    </div>
    <!-- 语言/主题切换 -->
    <div class="nav-actions">
      <button class="lang-toggle" aria-label="Switch language">...</button>
      <button class="theme-toggle" aria-label="Toggle theme">...</button>
    </div>
    <!-- 移动端汉堡菜单 -->
    <button class="nav-hamburger" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </nav>

  <!-- ③ Hero 区域（课程标题横幅） -->
  <section class="hero">
    <div class="hero-inner">
      <span class="lesson-tag">
        <span class="zh">第 X 课</span>
        <span class="en">Lesson X</span>
      </span>
      <h1>
        <span class="zh">课程标题</span>
        <span class="en">Lesson Title</span>
      </h1>
      <p class="subtitle">
        <span class="zh">课程副标题</span>
        <span class="en">Lesson subtitle</span>
      </p>
    </div>
  </section>

  <!-- ④ 正文内容（主要编辑区域） -->
  <div class="content" id="main-content">

    <section class="section reveal" id="section-X-1">
      <h2>...</h2>
      <p>...</p>
      <!-- 组件：卡片、对比、时间线等 -->
    </section>

    <section class="section reveal" id="section-X-2">
      <!-- ...更多章节... -->
    </section>

    <!-- ⑤ 课程底部导航 -->
    <div class="lesson-nav-footer">
      <!-- 上一课 / 下一课 链接 -->
    </div>

  </div>

  <!-- ⑥ 页脚 -->
  <footer class="footer">
    <p class="footer-text">
      <span class="zh">&copy; 2025 AI 探索之旅 &mdash; 专为青少年打造的人工智能课程</span>
      <span class="en">&copy; 2025 AI Explorer &mdash; An AI course designed for teens</span>
    </p>
  </footer>

  <script src="../../js/main.js"></script>
</body>
</html>
```

### 底部导航的三种情况

**第一课**（没有上一课）：
```html
<div class="lesson-nav-footer">
  <span></span>   <!-- 左侧留空 -->
  <a href="lesson2.html">
    <span class="zh">下一课：第二课标题 →</span>
    <span class="en">Next: Lesson 2 Title →</span>
  </a>
</div>
```

**中间课程**（有上一课和下一课）：
```html
<div class="lesson-nav-footer">
  <a href="lesson2.html">
    <span class="zh">← 上一课：第二课标题</span>
    <span class="en">← Previous: Lesson 2 Title</span>
  </a>
  <a href="lesson4.html">
    <span class="zh">下一课：第四课标题 →</span>
    <span class="en">Next: Lesson 4 Title →</span>
  </a>
</div>
```

**最后一课**（没有下一课）：
```html
<div class="lesson-nav-footer">
  <a href="lesson4.html">
    <span class="zh">← 上一课：第四课标题</span>
    <span class="en">← Previous: Lesson 4 Title</span>
  </a>
  <a href="../index.html">
    <span class="zh">回到首页 →</span>
    <span class="en">Back to Home →</span>
  </a>
</div>
```

---

## 8. 可用组件参考

以下是项目中已有的 HTML 组件，可以直接复制使用。**不需要写任何额外的 CSS 或 JS**，`style.css` 和 `main.js` 已经内置了所有组件的样式和交互。

### 8.1 卡片网格 (Card Grid)

用于展示 2~4 列的特性/知识点卡片。

```html
<div class="card-grid cols-3 reveal-stagger">

  <div class="card icon-card">
    <div class="icon">
      <!-- 从 https://heroicons.com/ 复制 SVG -->
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
           stroke-width="1.5" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" d="..."/>
      </svg>
    </div>
    <h4>
      <span class="zh">卡片标题</span>
      <span class="en">Card Title</span>
    </h4>
    <p>
      <span class="zh">卡片描述文字</span>
      <span class="en">Card description text</span>
    </p>
  </div>

  <!-- 复制更多 card 块... -->

</div>
```

**列数选项：** `cols-2`（两列）、`cols-3`（三列）、`cols-4`（四列）。移动端自动变为单列。

### 8.2 对比区块 (Compare)

用于两个概念的并排对比。

```html
<div class="compare reveal">

  <!-- 左列（正面/好） -->
  <div class="compare-col highlight-good">
    <h4>
      <span class="zh">概念 A</span>
      <span class="en">Concept A</span>
    </h4>
    <p>
      <span class="zh">描述文字</span>
      <span class="en">Description text</span>
    </p>
    <ul>
      <li><span class="zh">要点一</span><span class="en">Point one</span></li>
      <li><span class="zh">要点二</span><span class="en">Point two</span></li>
    </ul>
  </div>

  <!-- 右列（反面/差） -->
  <div class="compare-col highlight-bad">
    <h4>
      <span class="zh">概念 B</span>
      <span class="en">Concept B</span>
    </h4>
    <p>
      <span class="zh">描述文字</span>
      <span class="en">Description text</span>
    </p>
    <ul>
      <li><span class="zh">要点一</span><span class="en">Point one</span></li>
    </ul>
  </div>

</div>
```

**高亮选项：** `highlight-good`（绿色顶边）、`highlight-bad`（红色顶边），也可以不加高亮。

### 8.3 时间线 (Timeline)

用于按时间顺序展示历史事件，点击可展开详情。

```html
<div class="timeline">

  <div class="timeline-item">
    <div class="timeline-year">1950</div>
    <div class="timeline-card" role="button" tabindex="0">
      <h3>
        <span class="zh">事件名称</span>
        <span class="en">Event Name</span>
      </h3>
      <p>
        <span class="zh">简短描述（始终可见）</span>
        <span class="en">Brief description (always visible)</span>
      </p>
      <div class="timeline-detail hidden">
        <p>
          <span class="zh">详细说明（点击展开后可见）</span>
          <span class="en">Detailed explanation (visible after clicking)</span>
        </p>
      </div>
    </div>
  </div>

  <!-- 更多 timeline-item... -->

</div>
```

### 8.4 选择题测验 (Quiz)

每道题有 A/B/C/D 四个选项，选择后立即显示对错和解析。

```html
<div class="quiz" data-quiz-id="lesson3">

  <!-- 第 1 题 -->
  <div class="quiz-question" data-correct="B">
    <p class="quiz-prompt">
      <span class="zh"><strong>Q1.</strong> 题目内容？</span>
      <span class="en"><strong>Q1.</strong> Question text?</span>
    </p>
    <div class="quiz-options">
      <button class="quiz-option" data-value="A">
        <span class="zh">A. 选项 A</span>
        <span class="en">A. Option A</span>
      </button>
      <button class="quiz-option" data-value="B">
        <span class="zh">B. 选项 B</span>
        <span class="en">B. Option B</span>
      </button>
      <button class="quiz-option" data-value="C">
        <span class="zh">C. 选项 C</span>
        <span class="en">C. Option C</span>
      </button>
      <button class="quiz-option" data-value="D">
        <span class="zh">D. 选项 D</span>
        <span class="en">D. Option D</span>
      </button>
    </div>
    <p class="quiz-explanation hidden">
      <span class="zh">解析：正确答案是 B，因为...</span>
      <span class="en">Explanation: The correct answer is B, because...</span>
    </p>
  </div>

  <!-- 更多 quiz-question... -->

  <!-- 得分统计 -->
  <div class="quiz-result hidden">
    <p>
      <span class="zh">你的得分：<span class="score"><span class="quiz-score">0</span> / <span class="quiz-total">5</span></span></span>
      <span class="en">Your score: <span class="score"><span class="quiz-score">0</span> / <span class="quiz-total">5</span></span></span>
    </p>
  </div>

</div>
```

**关键属性：**
- `data-quiz-id`：测验唯一标识（用于进度保存），建议用 `lesson{课号}`
- `data-correct`：正确答案字母（A/B/C/D）
- `data-value`：选项对应的字母
- `quiz-total`：总题数，需要手动写对

### 8.5 AI 鉴别测验 (AI or Human)

让学生判断某段内容是 AI 生成还是人类创作。

```html
<div class="ai-or-human">

  <div class="aoh-item" data-answer="ai">
    <div class="aoh-content">
      <p>
        <span class="zh">一段待判断的内容...</span>
        <span class="en">Content to judge...</span>
      </p>
    </div>
    <div class="aoh-buttons">
      <button class="aoh-btn" data-choice="ai">
        <span class="zh">🤖 AI 生成</span>
        <span class="en">🤖 AI Generated</span>
      </button>
      <button class="aoh-btn" data-choice="human">
        <span class="zh">👤 人类创作</span>
        <span class="en">👤 Human Created</span>
      </button>
    </div>
    <div class="aoh-reveal hidden">
      <p>
        <span class="zh">答案揭晓：这是 AI 生成的，因为...</span>
        <span class="en">Answer: This was AI generated, because...</span>
      </p>
    </div>
  </div>

  <!-- 更多 aoh-item... -->

</div>

<div class="aoh-score hidden">
  <span class="zh">你答对了 <span class="aoh-correct">0</span> / <span class="aoh-total">5</span> 题！</span>
  <span class="en">You got <span class="aoh-correct">0</span> / <span class="aoh-total">5</span> correct!</span>
</div>
```

**关键属性：**
- `data-answer`：`"ai"` 或 `"human"`
- `data-choice`：按钮对应的选择

### 8.6 信息/提示/警告框 (Info Box)

```html
<!-- 提示框（绿色） -->
<div class="info-box tip">
  <span class="box-icon">💡</span>
  <p>
    <span class="zh">提示内容...</span>
    <span class="en">Tip content...</span>
  </p>
</div>

<!-- 信息框（蓝色） -->
<div class="info-box info">
  <span class="box-icon">ℹ️</span>
  <p>
    <span class="zh">补充信息...</span>
    <span class="en">Additional info...</span>
  </p>
</div>

<!-- 警告框（橙色） -->
<div class="info-box warning">
  <span class="box-icon">⚠️</span>
  <p>
    <span class="zh">注意事项...</span>
    <span class="en">Warning content...</span>
  </p>
</div>
```

### 8.7 步骤列表 (Steps)

```html
<div class="steps">
  <div class="step-item">
    <div class="step-num">1</div>
    <div class="step-content">
      <h4>
        <span class="zh">步骤标题</span>
        <span class="en">Step Title</span>
      </h4>
      <p>
        <span class="zh">步骤描述...</span>
        <span class="en">Step description...</span>
      </p>
    </div>
  </div>
  <!-- 更多 step-item... -->
</div>
```

### 8.8 可展开卡片 (Expandable Card)

```html
<div class="expandable-card">
  <div class="ec-header" role="button" tabindex="0">
    <h4>
      <span class="zh">点击展开标题</span>
      <span class="en">Click to Expand Title</span>
    </h4>
    <span class="ec-toggle">+</span>
  </div>
  <div class="ec-body hidden">
    <p>
      <span class="zh">展开后显示的内容...</span>
      <span class="en">Content shown after expanding...</span>
    </p>
  </div>
</div>
```

### 8.9 代码块 (Code Block)

```html
<div class="code-block">
  <div class="code-header">
    <span>Python</span>
    <button class="code-copy-btn">
      <span class="zh">复制</span>
      <span class="en">Copy</span>
    </button>
  </div>
  <pre><code>print("Hello, AI!")</code></pre>
</div>
```

### 8.10 组件速查表

| 组件 | 外层 class | 用途 | 交互 |
|:----|:----------|:----|:-----|
| 卡片网格 | `.card-grid.cols-{2,3,4}` | 特性展示 | 无（纯展示） |
| 对比区块 | `.compare` | 概念对比 | 无（纯展示） |
| 时间线 | `.timeline` | 历史事件 | 点击展开详情 |
| 选择题 | `.quiz` | 知识检测 | 点击选项、显示解析 |
| AI 鉴别 | `.ai-or-human` | 互动判断 | 点击按钮、揭晓答案 |
| 信息框 | `.info-box.{tip,info,warning}` | 补充说明 | 无（纯展示） |
| 步骤列表 | `.steps` | 操作步骤 | 无（纯展示） |
| 可展开卡片 | `.expandable-card` | 折叠内容 | 点击展开/收起 |
| 代码块 | `.code-block` | 展示代码 | 复制按钮 |
| 滚动动画 | `.reveal` / `.reveal-stagger` | 入场动画 | 滚动到视口时触发 |

---

## 9. 版本首页（edition index）编辑

每个版本的 `index.html`（如 `standard-5/index.html`）是课程入口页面。

### 9.1 课程卡片模板

```html
<div class="lesson-card" data-lesson="lesson1">
  <span class="lesson-number">01</span>
  <h3 class="lesson-title">
    <span class="zh">走进 AI 的世界</span>
    <span class="en">Welcome to the World of AI</span>
  </h3>
  <p class="lesson-desc">
    <span class="zh">了解AI的定义、发展历史和日常应用</span>
    <span class="en">Learn the definition, history, and daily applications of AI</span>
  </p>
  <span class="lesson-status hidden"><span class="zh"></span><span class="en"></span></span>
  <a href="lessons/lesson1.html" class="lesson-btn">
    <span class="zh">开始学习</span>
    <span class="en">Start</span>
  </a>
</div>
```

**关键属性：**
- `data-lesson="lesson1"` — JS 用于跟踪进度，必须与文件名一致
- `lesson-number` — 显示的编号（`01`、`02` 等），纯展示用
- `lesson-btn` 链接 — 指向 `lessons/lessonX.html`

### 9.2 添加新卡片

在 `<div class="lessons-grid">` 的末尾、`</div>` 之前粘贴新卡片即可。

### 9.3 版本首页的路径

| 元素 | 路径 |
|:-----|:----|
| CSS | `../css/style.css` |
| JS | `../js/main.js` |
| 门户首页 | `../index.html` |
| 课程文件 | `lessons/lesson1.html` |

---

## 10. 导航与链接规则

### 10.1 路径约定

| 页面位置 | CSS 路径 | JS 路径 | 门户首页 | 版本首页 |
|:---------|:---------|:--------|:---------|:---------|
| 根目录 `index.html` | `css/style.css` | `js/main.js` | — | `standard-5/index.html` |
| 版本首页 `{版本}/index.html` | `../css/style.css` | `../js/main.js` | `../index.html` | — |
| 课程文件 `{版本}/lessons/lessonX.html` | `../../css/style.css` | `../../js/main.js` | `../../index.html` | `../index.html` |

### 10.2 导航栏中当前课的标记

```html
<!-- lesson3.html 中，第 3 课带 class="active" -->
<div class="nav-lessons">
  <a href="lesson1.html"><span class="zh">第1课</span><span class="en">L1</span></a>
  <a href="lesson2.html"><span class="zh">第2课</span><span class="en">L2</span></a>
  <a href="lesson3.html" class="active"><span class="zh">第3课</span><span class="en">L3</span></a>
  <a href="lesson4.html"><span class="zh">第4课</span><span class="en">L4</span></a>
  <a href="lesson5.html"><span class="zh">第5课</span><span class="en">L5</span></a>
</div>
```

> 只有**当前页面对应的课程链接**才加 `class="active"`。

---

## 11. 讲稿编辑

### 11.1 文件位置

```
{版本}/scripts/第{X}课-讲解文本.md
```

### 11.2 讲稿结构模板

每份讲稿应包含以下章节（可参照已有讲稿）：

```markdown
# 第 X 课：课程标题

## 教学目标
- 目标 1
- 目标 2
- 目标 3

## 课时建议
约 45 分钟（或 1.5 小时，视版本而定）

## 教学流程

| 环节 | 时间 | 内容 |
|:-----|:----:|:-----|
| 导入 | 5 min | ... |
| 讲解 | 20 min | ... |
| 互动 | 10 min | ... |
| 总结 | 5 min | ... |

## 导入环节
（引入话题的方式、提问、小故事等）

## 核心概念讲解
（详细讲解要点，含类比、例子、故事）

## 互动/实操环节
（学生活动指导）

## 常见提问与应答
（预设学生可能的问题和参考回答）

## 总结与回顾
（本课要点复述）

## 课后延伸
（推荐阅读、视频、思考题等）
```

### 11.3 注意事项

- 讲稿是**纯中文**的（面向教师使用）
- 格式为 Markdown，可用任何 Markdown 编辑器打开
- 讲稿内容应与对应 HTML 课程页面的知识点保持一致

---

## 12. 修改后的验证清单

每次修改后，请按以下清单逐项检查：

### 12.1 基础检查

- [ ] 启动服务器：`python3 serve.py`
- [ ] 访问 `http://localhost:4200`，从门户首页进入对应版本
- [ ] 打开修改过的课程页面，确认内容正确显示

### 12.2 双语检查

- [ ] 点击右上角 "EN" 按钮切换到英文，确认所有文字都切换了
- [ ] 切回中文，确认没有残留的英文

### 12.3 主题检查

- [ ] 点击主题切换按钮（太阳/月亮图标），确认暗色模式显示正常
- [ ] 文字、卡片、背景的对比度是否清晰可读

### 12.4 导航检查

- [ ] 顶部导航栏的课程列表是否完整、编号正确
- [ ] 当前课是否高亮（`active` 状态）
- [ ] 底部"上一课/下一课"链接是否指向正确的页面
- [ ] 点击链接确认能正常跳转

### 12.5 交互组件检查

- [ ] 如果有测验（Quiz）：每道题都能正常选择、显示对错和解析
- [ ] 如果有时间线：点击能展开/收起详情
- [ ] 如果有 AI 鉴别：按钮能正常工作

### 12.6 响应式检查

- [ ] 浏览器窗口缩小到手机宽度（< 768px），确认布局自适应
- [ ] 汉堡菜单按钮能正常打开/关闭

### 12.7 运行自动化测试

```bash
uv run test/run_all.py
```

确认所有测试通过。

---

## 13. 提交与发布

### 13.1 Git 提交

```bash
# 查看改了哪些文件
git status

# 添加所有修改
git add .

# 提交（写明改了什么）
git commit -m "update standard-5 lesson 3: 更新机器学习案例"

# 推送
git push origin main
```

### 13.2 版本号规则

| 改动类型 | 版本号变化 | 示例 |
|:---------|:----------|:-----|
| 修复错别字、小调整 | 补丁号 +1 | v1.4.0 → v1.4.1 |
| 新增/删减课程 | 次版本号 +1 | v1.4.0 → v1.5.0 |
| 重大重构、新增版本 | 主版本号 +1 | v1.4.0 → v2.0.0 |

### 13.3 打 Tag（可选）

```bash
git tag -a v1.5.0 -m "v1.5.0 — 新增 standard-5 第 6 课"
git push origin main --tags
```

---

> **如有疑问，可参考已有课程文件作为模板。** 最可靠的学习方式是打开一个现有的 `lessonX.html`，对照本文档理解每一部分的作用，然后按同样的模式编写或修改。
