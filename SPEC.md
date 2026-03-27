# AI 探索之旅 / AI Explorer — 课程规格文档

> 面向 13-15 岁初中生的人工智能入门课程，共 5 课时，网页形式交付。**支持中英双语切换。**

---

## 1. 课程概览

### 1.1 目标受众
- 13-15 岁初中生
- 无编程基础或有少量 Scratch/Python 经验
- 对 AI 好奇，日常接触过 ChatGPT、AI 绘画等工具

### 1.2 教学目标
完成课程后，学生应能：
1. 用自己的话解释什么是人工智能、机器学习、深度学习
2. 理解 AI 的核心工作原理（数据 → 训练 → 预测）
3. 阅读并修改简单的 Python AI 代码片段
4. 掌握基础 Prompt Engineering 技巧
5. 辨识 AI 的能力边界和伦理问题

### 1.3 课时安排
| 课号 | 中文标题 | English Title | 时长 | 核心关键词 |
|------|---------|---------------|------|-----------|
| 1 | 走进 AI 的世界 | Welcome to the World of AI | 45 min | 定义、历史、生活中的 AI |
| 2 | 机器是怎么"学习"的 | How Do Machines Learn? | 45 min | 数据、监督学习、特征、模型 |
| 3 | 神经网络与深度学习 | Neural Networks & Deep Learning | 45 min | 神经元、层、CNN、可视化 |
| 4 | 大语言模型与 AIGC | LLMs & AI-Generated Content | 45 min | Token、Transformer、Prompt、生成式 AI |
| 5 | AI 的未来与责任 | The Future & Ethics of AI | 45 min | 偏见、安全、隐私、职业展望 |

---

## 2. 内容大纲

### 第 1 课：走进 AI 的世界

**学习目标：** 理解 AI 的定义、发展历史，识别生活中的 AI 应用。

| 节 | 内容 | 形式 |
|----|------|------|
| 1.1 开场：你今天用了哪些 AI？ | 列举日常 AI 场景（推荐算法、人脸解锁、语音助手、AI 翻译），引发思考 | 图文 + 图标卡片 |
| 1.2 什么是人工智能？ | 给出直白定义：让机器模拟人类智能（感知、推理、学习、决策）。对比"弱 AI"（专用）和"强 AI"（通用）。 | 文字 + 对比卡片 |
| 1.3 AI 发展简史 | 时间线：1950 图灵测试 → 1997 深蓝 → 2012 ImageNet → 2016 AlphaGo → 2022 ChatGPT → 2024 Sora | 交互式时间线组件 |
| 1.4 AI 的三大能力 | 感知（看/听）、思考（推理/规划）、创造（生成文字/图片/代码） | 三列图文卡片 |
| 1.5 互动：AI 还是人类？ | 展示 5 组内容（画作、文章、音乐片段），学生判断是 AI 还是人类创作 | 互动投票组件 |
| 1.6 小测验 | 5 道选择题，巩固本课知识点 | Quiz 组件 |

---

### 第 2 课：机器是怎么"学习"的

**学习目标：** 理解机器学习的核心流程（数据→特征→模型→预测），区分三种学习方式。

| 节 | 内容 | 形式 |
|----|------|------|
| 2.1 人类学习 vs 机器学习 | 类比：小孩认猫 = 看很多猫的照片 → 总结特征 → 遇到新猫也能认出。机器学习一样，只是用数学。 | 图文对比 |
| 2.2 数据：AI 的"食物" | 数据集概念、标签、训练集/测试集。举例：猫狗图片数据集。强调"垃圾进垃圾出"。 | 图文 + 数据表格示例 |
| 2.3 三种学习方式 | 监督学习（有老师，给答案）、无监督学习（自己找规律）、强化学习（试错奖惩，如打游戏） | 三列对比卡片 + 生活类比 |
| 2.4 互动：做一棵决策树 | 用"猜动物"游戏演示决策树：通过回答是/否问题分类。学生点击选择，看到树是怎么"生长"的。 | 交互式决策树组件 |
| 2.5 动手试试：线性回归 | 展示一段简单 Python 代码（sklearn），根据学习时间预测考试分数。展示散点图和拟合直线。 | 代码块 + 可视化图表 |
| 2.6 小测验 | 5 道选择题 | Quiz 组件 |

---

### 第 3 课：神经网络与深度学习

**学习目标：** 理解神经网络的基本结构，知道深度学习如何处理图像。

| 节 | 内容 | 形式 |
|----|------|------|
| 3.1 从大脑到人工神经元 | 生物神经元结构 → 人工神经元（输入×权重 → 求和 → 激活函数 → 输出）。类比：投票表决。 | 图文 + SVG 神经元示意图 |
| 3.2 神经网络的结构 | 输入层 → 隐藏层 → 输出层。深度学习 = 更多隐藏层。类比：流水线加工。 | SVG 网络结构动画 |
| 3.3 AI 怎么"看"东西 | 图片 = 像素数字矩阵。卷积神经网络(CNN)：用小窗口扫描提取特征（边缘→纹理→部件→整体）。 | 图文 + 像素网格可视化 |
| 3.4 训练的秘密 | 前向传播 → 计算误差 → 反向传播 → 调整权重。类比：考试→对答案→纠错→进步。 | 流程图 |
| 3.5 互动：体验神经网络 | 引导学生访问 TensorFlow Playground（外部链接），调整层数和神经元，观察分类边界变化。 | 外链引导 + 任务卡片 |
| 3.6 动手试试：Teachable Machine | 引导学生用 Google Teachable Machine 训练一个图像分类器（石头剪刀布）。 | 外链引导 + 步骤卡片 |
| 3.7 小测验 | 5 道选择题 | Quiz 组件 |

---

### 第 4 课：大语言模型与 AIGC

**学习目标：** 理解大语言模型的工作原理，掌握 Prompt 技巧，了解 AIGC 生态。

| 节 | 内容 | 形式 |
|----|------|------|
| 4.1 从文字到数字：Token | 文字 → Token 化 → 向量。演示 "我喜欢人工智能" 如何被切分成 Token。 | 图文 + Token 可视化 |
| 4.2 语言模型：预测下一个词 | 核心原理就是"猜下一个词"。给前文 → 计算所有可能词的概率 → 选最可能的。 | 图文 + 概率分布条形图 |
| 4.3 Transformer 简介 | 注意力机制（Attention）：不是逐字阅读，而是关注最相关的词。类比：看一段话时眼睛会跳到关键词。 | 图文 + 注意力热力图示意 |
| 4.4 ChatGPT 是怎么炼成的 | 预训练（阅读互联网）→ 微调（学习对话格式）→ RLHF（人类反馈强化学习）。三阶段图。 | 流程图 |
| 4.5 Prompt 工程技巧 | 5 个实用技巧：①明确角色 ②给出示例 ③分步指令 ④限定格式 ⑤迭代优化。每条配示例。 | 技巧卡片 + 对比示例 |
| 4.6 AIGC 全景 | AI 写作、AI 绘画（Stable Diffusion/Midjourney）、AI 音乐、AI 视频（Sora）、AI 编程。 | 网格展示卡片 |
| 4.7 互动：Prompt 挑战 | 给定 3 个任务场景，学生写出最佳 Prompt（提供参考答案可对照） | 互动输入 + 参考答案展开 |
| 4.8 小测验 | 5 道选择题 | Quiz 组件 |

---

### 第 5 课：AI 的未来与责任

**学习目标：** 理解 AI 的局限性和伦理挑战，思考如何与 AI 共处。

| 节 | 内容 | 形式 |
|----|------|------|
| 5.1 AI 能做什么？不能做什么？ | 擅长：模式识别、快速计算、处理海量数据。不擅长：常识推理、情感理解、创意、道德判断。 | 双列对比 |
| 5.2 AI 偏见与公平 | 案例：招聘 AI 歧视女性、人脸识别对深色皮肤准确率低。原因：训练数据的偏见。 | 案例卡片 |
| 5.3 深度伪造与信息安全 | Deepfake 换脸视频、AI 生成假新闻。如何辨别：来源核实、细节检查、工具检测。 | 图文 + 检查清单 |
| 5.4 隐私与数据保护 | 人脸数据、对话数据、行为数据。思考：你愿意用多少隐私换便利？ | 图文 + 思考题 |
| 5.5 AI 时代需要什么能力？ | 批判性思维、创造力、协作、终身学习、AI 素养。AI 不会取代人，但会用 AI 的人会取代不会用的人。 | 能力卡片 |
| 5.6 互动：设计你的 AI 产品 | 思考题：如果你可以设计一个 AI 产品解决生活中的问题，你会做什么？框架引导。 | 引导式思考卡片 |
| 5.7 课程总结 | 回顾 5 课核心知识点，推荐后续学习资源。 | 总结卡片 + 资源链接列表 |
| 5.8 结业测验 | 10 道综合选择题（涵盖全部 5 课内容） | Quiz 组件 |

---

## 3. 技术方案

### 3.1 技术栈
| 层面 | 选择 | 理由 |
|------|------|------|
| 标记语言 | HTML5 | 原生支持，无构建依赖 |
| 样式 | CSS3（自定义，不引入框架） | 减少依赖，完全可控 |
| 交互 | 原生 JavaScript（ES6+） | 零依赖，便于离线使用 |
| 字体 | Google Fonts CDN（Noto Sans SC） | 中文排版优化 |
| 图标 | 内联 SVG | 零请求，矢量清晰 |
| 代码高亮 | 自定义 CSS 类（手动着色） | 代码量少，无需引入库 |

### 3.2 中英双语实现方案

**方案：同页内联双语，CSS 切换可见性**

- `<html>` 标签通过 `data-lang="zh"` / `data-lang="en"` 控制当前语言
- 所有文本内容用 `<span class="zh">` 和 `<span class="en">` 包裹
- CSS 规则：当 `data-lang="zh"` 时隐藏 `.en`，反之亦然
- 导航栏放置语言切换按钮 `中 / EN`，点击即时切换，无需刷新
- 语言偏好保存到 localStorage（key: `ai-class-lang`，值: `"zh"` / `"en"`）
- 默认语言：中文

**CSS 实现：**
```css
[data-lang="zh"] .en { display: none; }
[data-lang="en"] .zh { display: none; }
```

**HTML 内容标注示例：**
```html
<h2>
  <span class="zh">什么是人工智能？</span>
  <span class="en">What is Artificial Intelligence?</span>
</h2>
<p>
  <span class="zh">人工智能是让机器模拟人类智能的技术。</span>
  <span class="en">AI is the technology that enables machines to simulate human intelligence.</span>
</p>
```

**Quiz 双语示例：**
```html
<div class="quiz-question" data-correct="B">
  <p class="quiz-prompt">
    <span class="zh">以下哪个是人工智能的应用？</span>
    <span class="en">Which of the following is an AI application?</span>
  </p>
  <div class="quiz-options">
    <button class="quiz-option" data-value="A">
      <span class="zh">A. 计算器</span>
      <span class="en">A. Calculator</span>
    </button>
    ...
  </div>
</div>
```

**导航栏语言切换按钮：**
```html
<button class="lang-toggle" aria-label="Switch language">
  <span class="zh">EN</span>
  <span class="en">中文</span>
</button>
```
> 显示的文字是"切换到的目标语言"，便于用户理解。

### 3.3 文件结构
```
AI-Class/
├── SPEC.md                  # 本规格文档
├── index.html               # 课程首页（课程介绍 + 课时导航）
├── css/
│   └── style.css            # 全局样式（设计系统 + 组件 + 布局）
├── js/
│   └── main.js              # 全局脚本（Quiz、动画、交互组件）
├── standard-5/              # 精简版 (5 课)
│   ├── index.html           # 版本首页
│   └── lessons/
│       ├── lesson1.html     # 第 1 课
│       ├── lesson2.html     # 第 2 课
│       ├── lesson3.html     # 第 3 课
│       ├── lesson4.html     # 第 4 课
│       └── lesson5.html     # 第 5 课
├── standard-15/             # 完整版 (15 课)
│   ├── index.html
│   └── lessons/             # lesson1-15.html
├── lab-10/                  # 实验版 (10 实验)
│   ├── index.html
│   └── lessons/             # lesson1-10.html
└── assets/
    └── images/              # 课程图片（如有必要）
```

### 3.3 页面结构（每个 lesson 页面）
```
┌─────────────────────────────────────────┐
│  顶部导航栏（Logo + 课时链接 + 当前课高亮 + 语言切换 + 暗色模式） │
├─────────────────────────────────────────┤
│  课程 Hero 区域                           │
│  ┌─────────────────────────────────────┐│
│  │ 课号标签  /  课名标题  /  副标题描述   ││
│  └─────────────────────────────────────┘│
├─────────────────────────────────────────┤
│  内容区域                                 │
│  ┌─ Section 1 ─────────────────────────┐│
│  │ h2 标题                              ││
│  │ 正文 / 卡片 / 图表 / 代码块          ││
│  └─────────────────────────────────────┘│
│  ┌─ Section 2 ─────────────────────────┐│
│  │ ...                                  ││
│  └─────────────────────────────────────┘│
│  ...                                     │
│  ┌─ Quiz Section ──────────────────────┐│
│  │ 小测验题目                            ││
│  └─────────────────────────────────────┘│
├─────────────────────────────────────────┤
│  底部导航（上一课 / 下一课）               │
├─────────────────────────────────────────┤
│  页脚                                    │
└─────────────────────────────────────────┘
```

### 3.4 响应式断点
| 断点 | 目标设备 |
|------|---------|
| ≥ 1024px | 桌面 / 笔记本 |
| 768px - 1023px | 平板 |
| < 768px | 手机 |

---

## 4. 设计系统

### 4.1 色彩
```
主色（Primary）      : #6366f1  (Indigo 500)  — 标题、按钮、强调
主色浅（Primary Light）: #a5b4fc  (Indigo 300)  — 悬停、背景点缀
次要色（Secondary）   : #06b6d4  (Cyan 500)    — 链接、辅助标记
强调色（Accent）      : #f59e0b  (Amber 500)   — 重点提示、徽章
成功色（Success）     : #22c55e  (Green 500)   — 正确答案
错误色（Error）       : #ef4444  (Red 500)     — 错误答案
背景色（BG）          : #f8fafc  (Slate 50)    — 页面背景
卡片背景             : #ffffff                  — 卡片
文字色（Text）        : #1e293b  (Slate 800)   — 正文
次要文字             : #64748b  (Slate 500)   — 副标题、说明
```

### 4.2 字体
```
正文字体 : "Noto Sans SC", system-ui, sans-serif
代码字体 : "JetBrains Mono", "Fira Code", monospace
标题字重 : 700
正文字重 : 400
```

### 4.3 字号（Desktop / Mobile）
| 层级 | 桌面 | 移动 |
|------|------|------|
| Hero 标题 | 3rem (48px) | 2rem (32px) |
| h2 章节标题 | 2rem (32px) | 1.5rem (24px) |
| h3 子标题 | 1.5rem (24px) | 1.25rem (20px) |
| 正文 | 1.125rem (18px) | 1rem (16px) |
| 小字 / 标签 | 0.875rem (14px) | 0.875rem (14px) |

### 4.4 间距
```
基础单位       : 0.5rem (8px)
组件内 padding  : 1.5rem (24px)
Section 间距    : 4rem (64px)
卡片圆角       : 1rem (16px)
卡片阴影       : 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1)
```

### 4.5 动画
```
默认过渡   : all 0.3s ease
滚动入场   : translateY(30px) + opacity 0→1, duration 0.6s, 使用 IntersectionObserver
悬停效果   : translateY(-4px) + shadow 加深
```

---

## 5. 交互组件规格

### 5.1 Quiz 组件
```
行为：
- 每题显示题目 + 4 个选项（A/B/C/D）
- 选中后立即高亮（绿色=正确，红色=错误）
- 错误时显示正确答案和简短解释
- 每题只能作答一次
- 答题后出现"提交测验"按钮，支持部分答题提交
- 全部答完或点击提交后显示：得分、正确率百分比、智能反馈
  - 100% 全对 → 绿色鼓励："太棒了！全部答对，你已经完全掌握了这节课的内容！"
  - < 60% → 红色建议："正确率较低，建议重新学习本课内容后再试一次哦！"
  - 60%-99% → 普通提示："完成测验！继续学习下一课吧。"
- 未作答题目按错误计分，并显示橙色提示

HTML 结构：
<div class="quiz" data-quiz-id="lesson1">
  <div class="quiz-question" data-correct="B">
    <p class="quiz-prompt">题目文字</p>
    <div class="quiz-options">
      <button class="quiz-option" data-value="A">A. 选项文字</button>
      <button class="quiz-option" data-value="B">B. 选项文字</button>
      <button class="quiz-option" data-value="C">C. 选项文字</button>
      <button class="quiz-option" data-value="D">D. 选项文字</button>
    </div>
    <p class="quiz-explanation hidden">解释文字</p>
  </div>
  ...
  <button class="quiz-submit-btn hidden">提交测验</button>
  <div class="quiz-result hidden">
    <!-- 内容由 JS 动态生成：得分、正确率、反馈消息 -->
  </div>
</div>
```

### 5.2 交互式时间线（第 1 课）
```
行为：
- 垂直时间线，左侧年份，右侧事件卡片
- 滚动时卡片依次淡入
- 点击卡片可展开查看更多详情

HTML 结构：
<div class="timeline">
  <div class="timeline-item">
    <div class="timeline-year">1950</div>
    <div class="timeline-card">
      <h3>图灵测试</h3>
      <p>简述...</p>
      <div class="timeline-detail hidden">详细内容...</div>
    </div>
  </div>
  ...
</div>
```

### 5.3 决策树互动（第 2 课）
```
行为：
- 显示一个问题（如 "它有毛吗？"）
- 学生点击"是"或"否"
- 根据选择展示下一个问题节点，直到到达叶节点（动物名称）
- 完成后显示完整决策树路径

HTML 结构：
<div class="decision-tree" data-tree-id="animals">
  <div class="tree-node active" data-node-id="root">
    <p class="tree-question">这个动物有毛发吗？</p>
    <div class="tree-choices">
      <button class="tree-btn" data-next="node-fur-yes">是</button>
      <button class="tree-btn" data-next="node-fur-no">否</button>
    </div>
  </div>
  <div class="tree-node" data-node-id="node-fur-yes">
    <p class="tree-question">它会飞吗？</p>
    ...
  </div>
  ...
  <div class="tree-node tree-leaf" data-node-id="leaf-cat">
    <p class="tree-result">🐱 猫！</p>
  </div>
</div>
```

### 5.4 AI 鉴别互动（第 1 课）
```
行为：
- 展示一组内容（文字/描述），学生猜是 AI 生成还是人类创作
- 点击"AI"或"人类"按钮后揭示答案
- 记录答对数量，最终显示总分

HTML 结构：
<div class="ai-or-human">
  <div class="aoh-item" data-answer="ai">
    <div class="aoh-content">
      <p>（展示内容描述）</p>
    </div>
    <div class="aoh-buttons">
      <button class="aoh-btn" data-choice="ai">AI 生成</button>
      <button class="aoh-btn" data-choice="human">人类创作</button>
    </div>
    <div class="aoh-reveal hidden">
      <p>答案：AI 生成 — 解释...</p>
    </div>
  </div>
  ...
</div>
```

### 5.5 Prompt 挑战（第 4 课）
```
行为：
- 展示一个任务场景描述
- 提供文本输入框，学生写自己的 Prompt
- 点击"查看参考答案"展开显示优秀 Prompt 示例
- 不做自动评分，鼓励对比和反思

HTML 结构：
<div class="prompt-challenge">
  <div class="pc-task">
    <h3>任务场景</h3>
    <p>场景描述...</p>
  </div>
  <textarea class="pc-input" placeholder="在这里写你的 Prompt..."></textarea>
  <button class="pc-reveal-btn">查看参考答案</button>
  <div class="pc-reference hidden">
    <p class="pc-ref-prompt">参考 Prompt 内容...</p>
    <p class="pc-ref-explain">为什么这个 Prompt 更好：...</p>
  </div>
</div>
```

### 5.6 可展开卡片（通用）
```
行为：
- 显示标题和摘要
- 点击可展开显示完整内容
- 再次点击收起

HTML 结构：
<div class="expandable-card">
  <div class="ec-header">
    <h3>标题</h3>
    <span class="ec-toggle">+</span>
  </div>
  <div class="ec-body hidden">
    <p>详细内容...</p>
  </div>
</div>
```

### 5.7 代码展示块
```
行为：
- 显示代码，带行号和语法着色
- 有"复制代码"按钮
- 可选的输出展示区域

HTML 结构：
<div class="code-block">
  <div class="code-header">
    <span class="code-lang">Python</span>
    <button class="code-copy-btn">复制</button>
  </div>
  <pre class="code-pre"><code>...</code></pre>
  <div class="code-output">
    <span class="code-output-label">输出：</span>
    <pre>...</pre>
  </div>
</div>
```

---

## 6. 首页规格 (index.html)

### 布局
```
┌──────────────────────────────────────────┐
│  顶部导航（Logo: "AI 探索之旅"）          │
├──────────────────────────────────────────┤
│  Hero 区域                                │
│  ┌──────────────────────────────────────┐│
│  │  大标题：AI 探索之旅                   ││
│  │  副标题：写给 00 后的人工智能入门课     ││
│  │  CTA 按钮：开始学习 →                  ││
│  └──────────────────────────────────────┘│
├──────────────────────────────────────────┤
│  课程亮点（3-4 个图标 + 短文字）           │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    │
│  │5 课时 │ │零基础 │ │互动式 │ │有趣味 │    │
│  └──────┘ └──────┘ └──────┘ └──────┘    │
├──────────────────────────────────────────┤
│  课时列表（5 张卡片，每张含课号+标题+摘要） │
│  ┌─────────────┐ ┌─────────────┐        │
│  │  第 1 课     │ │  第 2 课     │        │
│  │  走进AI的世界│ │  机器怎么学习│        │
│  │  摘要文字... │ │  摘要文字... │        │
│  │  [开始] 按钮 │ │  [开始] 按钮 │        │
│  └─────────────┘ └─────────────┘        │
│  ...                                     │
├──────────────────────────────────────────┤
│  页脚                                     │
└──────────────────────────────────────────┘
```

---

## 7. 验收标准

- [ ] 所有 HTML 文件通过 W3C 验证，无 error
- [ ] 在 Chrome、Firefox 最新版正常显示
- [ ] 响应式布局在 375px（手机）、768px（平板）、1440px（桌面）均正常
- [ ] 所有 Quiz 组件可正常作答并显示得分
- [ ] 所有交互组件（时间线、决策树、AI鉴别、Prompt挑战）可正常使用
- [ ] 页面间导航正确（上一课/下一课/首页）
- [ ] 可离线使用（除 Google Fonts CDN 外无外部依赖）
- [ ] 无 JavaScript 控制台错误

---

## 8. 已确认事项

1. **打印友好样式** — 需要。`@media print` 隐藏导航/交互，优化排版。
2. **暗色模式** — 需要。顶部导航放置切换按钮，偏好保存到 localStorage，默认跟随系统 `prefers-color-scheme`。
3. **进度保存** — 需要。用 localStorage 记录：已完成课时、每课 Quiz 得分。首页课时卡片显示完成状态。
4. **外部工具** — 可访问。Teachable Machine、TensorFlow Playground 等外链正常引用。

### 8.1 暗色模式色彩补充
```
暗色背景（BG）       : #0f172a  (Slate 900)
暗色卡片背景         : #1e293b  (Slate 800)
暗色文字             : #e2e8f0  (Slate 200)
暗色次要文字         : #94a3b8  (Slate 400)
暗色边框             : #334155  (Slate 700)
主色/次要色/强调色保持不变，可适当提高亮度。
```

### 8.2 进度保存 localStorage 结构
```json
{
  "ai-class-progress": {
    "lesson1": { "completed": true, "quizScore": 4, "quizTotal": 5 },
    "lesson2": { "completed": false, "quizScore": null, "quizTotal": null }
  },
  "ai-class-theme": "dark",
  "ai-class-lang": "zh"
}
```

### 8.3 打印样式规则
- 隐藏：导航栏、暗色模式切换、Quiz 按钮交互、底部课时导航
- 显示：Quiz 题目+正确答案（文字形式）
- 强制白色背景 + 黑色文字
- 去除阴影、圆角
- 分页：每个 `content-section` 允许 `break-inside: avoid`

---

*文档版本：v1.2.1 | 已确认（含双语支持 + 测验增强），开始实施*
