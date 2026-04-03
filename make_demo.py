# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "Pillow>=10.0",
#     "edge-tts>=6.1",
# ]
# ///
"""
make_demo.py — 生成 AI 探索之旅 课程介绍 Demo 视频 (MP4)
Generate a demo video introducing the AI Explorer courses.

功能 / Features:
  - 中英文字幕注释 / Bilingual (CN + EN) on-screen annotations
  - 中文配音 (edge-tts) / Chinese voiceover via edge-tts
  - 真实课程截图 / Real course screenshots
  - 课堂与测验演示 / Lesson & quiz demonstration
  - 纯 Python + ffmpeg / Python + ffmpeg, no extra tools

前置步骤 / Prerequisites:
  uv run take_screenshots.py   # 先截图 / Take screenshots first

用法 / Usage:
  uv run make_demo.py
"""

import asyncio
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ─── 配置 / Configuration ───────────────────────────────────────────
WIDTH, HEIGHT = 1920, 1080          # 1080p 分辨率 / 1080p resolution
FPS = 30                            # 帧率 / Frame rate
BG_COLOR = (15, 23, 42)            # 深蓝背景 / Dark blue background
TEXT_COLOR = (255, 255, 255)        # 白色文字 / White text
ACCENT_COLOR = (99, 102, 241)      # 靛蓝强调色 / Indigo accent
SUB_COLOR = (148, 163, 184)        # 浅灰副标题 / Light gray subtitle
TTS_VOICE = "zh-CN-YunxiNeural"    # 中文男声 / Chinese male voice
OUTPUT_FILE = "demo.mp4"           # 输出文件名 / Output filename

# 字体路径 / Font paths
FONT_CN = "/home/mystic/.local/share/fonts/NotoSansCJKsc-Regular.otf"
FONT_EN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_EN_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# 截图目录 / Screenshots directory
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"

# ─── 场景数据 / Scene Data ──────────────────────────────────────────
SCENES = [
    # ── 场景 0: 片头 / Opening ──
    {
        "type": "title",            # 场景类型 / Scene type
        "cn_title": "AI 探索之旅",
        "en_title": "AI Explorer",
        "cn_desc": "写给 00 后的人工智能入门课",
        "en_desc": "An AI Intro Course for Gen Z",
        "tts": "欢迎来到 AI 探索之旅！这是一套专为青少年打造的人工智能入门课程，包含五大版本，满足不同学习需求。",
        "color": ACCENT_COLOR,
    },
    # ── 场景 1: 精简版 / Standard 5 ──
    {
        "type": "course",
        "cn_title": "5 课时精简版",
        "en_title": "5-Lesson Standard Edition",
        "cn_desc": "快速入门 AI 核心概念\n零基础友好 · 互动测验\n涵盖 AI 基础到伦理",
        "en_desc": "Quick intro to core AI concepts\nBeginner-friendly · Interactive quizzes\nFrom AI basics to ethics",
        "tts": "第一个版本是五课时精简版。适合课堂教学或自学体验，五节课带你快速了解人工智能的核心概念，从AI基础到伦理，零基础也能轻松上手。",
        "color": (99, 102, 241),
        "screenshot": "edition_standard5.png",
        "badge": "精简版 / Standard",
    },
    # ── 场景 2: 完整版 / Standard 15 ──
    {
        "type": "course",
        "cn_title": "15 课时完整版",
        "en_title": "15-Lesson Comprehensive Edition",
        "cn_desc": "深入全面探索 AI 世界\nNLP · 计算机视觉 · 强化学习\nAI 伦理与安全深度探讨",
        "en_desc": "Deep dive into the AI world\nNLP · Computer Vision · Reinforcement Learning\nIn-depth AI ethics & safety coverage",
        "tts": "第二个版本是十五课时完整版。涵盖自然语言处理、计算机视觉、强化学习等前沿技术，适合想要系统深入学习的同学。",
        "color": (37, 99, 235),
        "screenshot": "edition_standard15.png",
        "badge": "完整版 / Comprehensive",
    },
    # ── 场景 3: 实验版 / Lab 10 ──
    {
        "type": "course",
        "cn_title": "10 实验动手版",
        "en_title": "10-Lab Hands-On Edition",
        "cn_desc": "边做边学，项目驱动\n图像识别 · 聊天机器人 · AI 绘画\n每个实验产出可展示的作品",
        "en_desc": "Learn by building, project-driven\nImage recognition · Chatbots · AI Art\nBuild a portfolio project in each lab",
        "tts": "第三个版本是十个实验动手版。通过图像识别、聊天机器人、AI绘画等十个实战项目，边做边学，每个实验都能产出可展示的作品。",
        "color": (5, 150, 105),
        "screenshot": "edition_lab10.png",
        "badge": "实验版 / Lab",
    },
    # ── 场景 4: App 创造营 / App Studio ──
    {
        "type": "course",
        "cn_title": "10 课 AI App 创造营",
        "en_title": "10-Lesson AI App Studio",
        "cn_desc": "MIT App Inventor + AI API\n适合 10-14 岁，零基础\n做出真正能用的手机 App",
        "en_desc": "MIT App Inventor + AI APIs\nAges 10-14, no experience needed\nBuild real AI-powered mobile apps",
        "tts": "第四个版本是AI App创造营。用MIT App Inventor加上AI API，十节课带你从零开始，做出真正能安装到手机上的智能应用。",
        "color": (217, 119, 6),
        "screenshot": "edition_app10.png",
        "badge": "创造营 / App Studio",
    },
    # ── 场景 5: 网站工坊 / Web Studio ──
    {
        "type": "course",
        "cn_title": "12 课 AI 网站工坊",
        "en_title": "12-Lesson AI Web Studio",
        "cn_desc": "HTML/CSS/JS + AI API\n适合 12-16 岁，零基础\nGitHub Pages 部署，真正上线",
        "en_desc": "HTML/CSS/JS + AI APIs\nAges 12-16, no experience needed\nDeploy on GitHub Pages — truly live",
        "tts": "第五个版本是AI网站工坊。学习HTML、CSS和JavaScript，结合AI API，十二节课打造一个有AI功能的真网站，还能部署上线让全世界访问。",
        "color": (219, 39, 119),
        "screenshot": "edition_web12.png",
        "badge": "网站工坊 / Web Studio",
    },
    # ── 场景 6: 课堂体验 — 知识讲解 / Lesson Demo — Knowledge ──
    {
        "type": "lesson_demo",
        "cn_title": "课堂体验 — 丰富的互动内容",
        "en_title": "Lesson Experience — Rich Interactive Content",
        "cn_desc": "每节课包含图文讲解、历史时间线\n卡片式知识点、代码实战演示\n适配各种学习风格",
        "en_desc": "Each lesson features visual explanations, timelines\nCard-based knowledge points, live code demos\nDesigned for all learning styles",
        "tts": "让我们来看看课堂体验。每节课都包含丰富的互动内容：图文并茂的知识讲解、历史时间线、卡片式知识点，以及代码实战演示，适配各种学习风格。",
        "color": (99, 102, 241),
        "screenshots": [
            "lesson_s5_hero.png",
            "lesson_s5_timeline.png",
        ],
    },
    # ── 场景 7: 课堂体验 — 代码实战 / Lesson Demo — Code ──
    {
        "type": "lesson_demo",
        "cn_title": "课堂体验 — 代码实战",
        "en_title": "Lesson Experience — Hands-On Coding",
        "cn_desc": "Python 编程 · AI 库实战\nHTML/CSS/JS 网站开发\n代码高亮 · 一键复制",
        "en_desc": "Python programming · AI libraries\nHTML/CSS/JS web development\nSyntax highlighting · Copy button",
        "tts": "实验版和网站工坊都提供代码实战环节。学生可以跟着步骤编写Python程序，或者用HTML搭建网页，所有代码都有语法高亮和一键复制功能。",
        "color": (5, 150, 105),
        "screenshots": [
            "lesson_lab_code.png",
            "lesson_web_code.png",
        ],
    },
    # ── 场景 8: 互动测验 / Quiz Demo ──
    {
        "type": "quiz_demo",
        "cn_title": "互动测验 — 边学边测",
        "en_title": "Interactive Quiz — Learn & Test",
        "cn_desc": "每课结尾都有小测验\n选择题 · 即时反馈 · 答案解析\n帮助巩固所学知识",
        "en_desc": "Quiz at the end of each lesson\nMultiple choice · Instant feedback · Explanations\nReinforce what you've learned",
        "tts": "每节课结尾都设有互动测验。学生选择答案后，系统会即时给出反馈，绿色表示正确，红色表示需要再想想，还有详细的答案解析，帮助巩固所学知识。",
        "color": (37, 99, 235),
        "screenshots": [
            "quiz_before.png",
            "quiz_after.png",
        ],
    },
    # ── 场景 9: 特色 / Features ──
    {
        "type": "features",
        "cn_title": "课程特色",
        "en_title": "Course Highlights",
        "cn_desc": "零基础 · 中英双语 · 互动式学习\n专为青少年量身打造\n五大版本，自由选择你的学习路径",
        "en_desc": "No prerequisites · Bilingual · Interactive\nDesigned for teenagers\nFive editions — choose your learning path",
        "tts": "所有课程零基础即可学习，支持中英文双语切换，互动式教学设计，专为青少年量身打造。",
        "color": ACCENT_COLOR,
    },
    # ── 场景 10: 结尾 / Closing ──
    {
        "type": "title",
        "cn_title": "开始你的 AI 之旅",
        "en_title": "Start Your AI Journey",
        "cn_desc": "选择适合你的版本，今天就开始探索！",
        "en_desc": "Pick your edition and start exploring today!",
        "tts": "选择适合你的版本，今天就开始你的AI探索之旅吧！",
        "color": ACCENT_COLOR,
    },
]


def load_fonts():
    """加载字体 / Load fonts for rendering."""
    return {
        "cn_title": ImageFont.truetype(FONT_CN, 68),
        "cn_desc": ImageFont.truetype(FONT_CN, 36),
        "en_title": ImageFont.truetype(FONT_EN_BOLD, 32),
        "en_desc": ImageFont.truetype(FONT_EN, 26),
        "badge": ImageFont.truetype(FONT_CN, 22),
        "cn_big": ImageFont.truetype(FONT_CN, 96),
        "en_big": ImageFont.truetype(FONT_EN_BOLD, 44),
        "watermark": ImageFont.truetype(FONT_EN, 18),
        "label": ImageFont.truetype(FONT_CN, 28),
    }


def draw_rounded_rect(draw, xy, radius, fill):
    """绘制圆角矩形 / Draw a rounded rectangle."""
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def draw_decorative_dots(draw, x, y, color, count=5, spacing=12, size=4):
    """绘制装饰圆点 / Draw decorative dots."""
    for i in range(count):
        draw.ellipse(
            [x + i * spacing, y, x + i * spacing + size, y + size],
            fill=(*color, 180)
        )


def load_screenshot(filename, target_w, target_h):
    """
    加载并缩放截图，添加圆角和阴影效果
    Load and resize screenshot with rounded corners and shadow.
    """
    path = SCREENSHOT_DIR / filename
    if not path.exists():
        # 创建占位图 / Create placeholder
        placeholder = Image.new("RGB", (target_w, target_h), (30, 41, 59))
        d = ImageDraw.Draw(placeholder)
        d.text((target_w // 2 - 60, target_h // 2 - 10),
               f"[{filename}]", fill=(100, 116, 139))
        return placeholder

    img = Image.open(path).convert("RGB")

    # 计算缩放比例，保持纵横比 / Scale maintaining aspect ratio
    ratio = min(target_w / img.width, target_h / img.height)
    new_w = int(img.width * ratio)
    new_h = int(img.height * ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)

    # 居中裁剪到目标尺寸 / Center crop to target size
    canvas = Image.new("RGB", (target_w, target_h), BG_COLOR)
    x_off = (target_w - new_w) // 2
    y_off = (target_h - new_h) // 2
    canvas.paste(img, (x_off, y_off))

    # 添加圆角蒙版 / Apply rounded corners mask
    radius = 16
    mask = Image.new("L", (target_w, target_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, target_w, target_h],
                                radius=radius, fill=255)

    result = Image.new("RGB", (target_w, target_h), BG_COLOR)
    result.paste(canvas, mask=mask)
    return result


def add_screenshot_frame(img, screenshot, x, y, color, border_width=3):
    """
    将截图嵌入到画布上，添加边框效果
    Paste a screenshot onto the canvas with a colored border.
    """
    sw, sh = screenshot.size
    draw = ImageDraw.Draw(img)

    # 绘制边框背景 / Draw border background
    bw = border_width
    draw.rounded_rectangle(
        [x - bw, y - bw, x + sw + bw, y + sh + bw],
        radius=18, fill=(*color, 160) if len(color) >= 3 else color
    )

    # 粘贴截图 / Paste screenshot
    img.paste(screenshot, (x, y))


def render_title_scene(scene, fonts, total_scenes, scene_idx):
    """
    渲染片头/片尾场景 / Render opening/closing title scene.
    """
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    color = scene["color"]

    # 背景装饰 / Background decoration
    draw.rounded_rectangle([0, 0, WIDTH, 6], radius=0, fill=color)
    draw.ellipse([WIDTH - 350, HEIGHT - 350, WIDTH + 100, HEIGHT + 100],
                 fill=(color[0] // 6, color[1] // 6, color[2] // 6))
    draw.ellipse([-200, -200, 300, 300],
                 fill=(color[0] // 5, color[1] // 5, color[2] // 5))

    # 中文大标题 / Large Chinese title
    bbox = draw.textbbox((0, 0), scene["cn_title"], font=fonts["cn_big"])
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, HEIGHT // 2 - 100),
              scene["cn_title"], fill=TEXT_COLOR, font=fonts["cn_big"])

    # 英文标题 / English title
    bbox = draw.textbbox((0, 0), scene["en_title"], font=fonts["en_big"])
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, HEIGHT // 2 + 20),
              scene["en_title"], fill=SUB_COLOR, font=fonts["en_big"])

    # 装饰线 / Decorative line
    line_w = 120
    draw.rounded_rectangle(
        [(WIDTH - line_w) // 2, HEIGHT // 2 + 90,
         (WIDTH + line_w) // 2, HEIGHT // 2 + 96],
        radius=3, fill=color
    )

    # 描述文字 / Description
    for i, (cn_line, en_line) in enumerate(
        zip(scene["cn_desc"].split("\n"), scene["en_desc"].split("\n"))
    ):
        y_base = HEIGHT // 2 + 120 + i * 70
        bbox = draw.textbbox((0, 0), cn_line, font=fonts["cn_desc"])
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, y_base),
                  cn_line, fill=TEXT_COLOR, font=fonts["cn_desc"])
        bbox = draw.textbbox((0, 0), en_line, font=fonts["en_desc"])
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, y_base + 40),
                  en_line, fill=SUB_COLOR, font=fonts["en_desc"])

    # 底部元素 / Footer elements
    _draw_footer(draw, fonts, color, scene_idx, total_scenes)
    return img


def render_course_scene(scene, fonts, total_scenes, scene_idx):
    """
    渲染课程介绍场景（左侧截图 + 右侧文字）
    Render course scene with screenshot on the left and text on the right.
    """
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    color = scene["color"]

    # 背景装饰 / Background decoration
    draw.rounded_rectangle([0, 0, WIDTH, 6], radius=0, fill=color)
    draw.ellipse([WIDTH - 300, HEIGHT - 300, WIDTH + 100, HEIGHT + 100],
                 fill=(color[0] // 6, color[1] // 6, color[2] // 6))

    # ── 左侧：课程截图 / Left: course screenshot ──
    shot_w, shot_h = 760, 570
    screenshot = load_screenshot(scene["screenshot"], shot_w, shot_h)
    add_screenshot_frame(img, screenshot, 80, 180, color)

    # 截图下方标签 / Label below screenshot
    badge_text = scene.get("badge", "")
    if badge_text:
        draw_rounded_rect(draw, [80, 770, 80 + shot_w, 810], 20,
                          fill=(*color, 200))
        bbox = draw.textbbox((0, 0), badge_text, font=fonts["badge"])
        tw = bbox[2] - bbox[0]
        draw.text(((80 + 80 + shot_w - tw) // 2, 778),
                  badge_text, fill=(255, 255, 255), font=fonts["badge"])

    # ── 右侧：文字区 / Right: text area ──
    x_text = 920

    # 中文标题 / Chinese title
    draw.text((x_text, 200), scene["cn_title"],
              fill=TEXT_COLOR, font=fonts["cn_title"])

    # 标题下划线 / Title underline
    bbox = draw.textbbox((0, 0), scene["cn_title"], font=fonts["cn_title"])
    title_w = bbox[2] - bbox[0]
    draw.rounded_rectangle(
        [x_text, 285, x_text + min(title_w, 600), 291],
        radius=3, fill=color
    )

    # 英文标题 / English title
    draw.text((x_text, 310), scene["en_title"],
              fill=SUB_COLOR, font=fonts["en_title"])

    # 描述列表 / Description list
    cn_lines = scene["cn_desc"].split("\n")
    en_lines = scene["en_desc"].split("\n")
    for i, (cn, en) in enumerate(zip(cn_lines, en_lines)):
        y = 400 + i * 120
        draw.ellipse([x_text, y + 12, x_text + 10, y + 22], fill=color)
        draw.text((x_text + 24, y), cn,
                  fill=TEXT_COLOR, font=fonts["cn_desc"])
        draw.text((x_text + 24, y + 44), en,
                  fill=SUB_COLOR, font=fonts["en_desc"])

    _draw_footer(draw, fonts, color, scene_idx, total_scenes)
    return img


def render_lesson_demo_scene(scene, fonts, total_scenes, scene_idx):
    """
    渲染课堂体验演示场景（双截图 + 下方文字）
    Render lesson demo scene with two screenshots side by side.
    """
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    color = scene["color"]

    # 背景 / Background
    draw.rounded_rectangle([0, 0, WIDTH, 6], radius=0, fill=color)
    draw.ellipse([-200, -200, 200, 200],
                 fill=(color[0] // 5, color[1] // 5, color[2] // 5))

    # 顶部标题 / Top title
    bbox = draw.textbbox((0, 0), scene["cn_title"], font=fonts["cn_title"])
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 40),
              scene["cn_title"], fill=TEXT_COLOR, font=fonts["cn_title"])

    bbox = draw.textbbox((0, 0), scene["en_title"], font=fonts["en_title"])
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 120),
              scene["en_title"], fill=SUB_COLOR, font=fonts["en_title"])

    # ── 两张截图并排 / Two screenshots side by side ──
    screenshots = scene.get("screenshots", [])
    shot_w, shot_h = 840, 470

    if len(screenshots) >= 2:
        # 左截图 / Left screenshot
        left = load_screenshot(screenshots[0], shot_w, shot_h)
        add_screenshot_frame(img, left, 60, 180, color)

        # 右截图 / Right screenshot
        right = load_screenshot(screenshots[1], shot_w, shot_h)
        add_screenshot_frame(img, right, 1020, 180, color)
    elif len(screenshots) == 1:
        # 单张居中截图 / Single centered screenshot
        shot_w_big = 1200
        single = load_screenshot(screenshots[0], shot_w_big, shot_h)
        add_screenshot_frame(img, single, (WIDTH - shot_w_big) // 2, 180, color)

    # ── 底部描述文字 / Bottom description ──
    cn_lines = scene["cn_desc"].split("\n")
    en_lines = scene["en_desc"].split("\n")
    start_y = 690
    for i, (cn, en) in enumerate(zip(cn_lines, en_lines)):
        y = start_y + i * 90
        # 三列布局居中 / Center three columns
        bbox_cn = draw.textbbox((0, 0), cn, font=fonts["cn_desc"])
        bbox_en = draw.textbbox((0, 0), en, font=fonts["en_desc"])
        cn_tw = bbox_cn[2] - bbox_cn[0]
        en_tw = bbox_en[2] - bbox_en[0]

        cx = WIDTH // 2
        draw.ellipse([cx - cn_tw // 2 - 20, y + 12,
                       cx - cn_tw // 2 - 10, y + 22], fill=color)
        draw.text((cx - cn_tw // 2, y), cn,
                  fill=TEXT_COLOR, font=fonts["cn_desc"])
        draw.text((cx - en_tw // 2, y + 42), en,
                  fill=SUB_COLOR, font=fonts["en_desc"])

    _draw_footer(draw, fonts, color, scene_idx, total_scenes)
    return img


def render_quiz_demo_scene(scene, fonts, total_scenes, scene_idx):
    """
    渲染互动测验演示场景（左：答题前，右：答题后 + 文字说明）
    Render quiz demo scene: before/after answering side by side.
    """
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    color = scene["color"]

    # 背景 / Background
    draw.rounded_rectangle([0, 0, WIDTH, 6], radius=0, fill=color)
    draw.ellipse([WIDTH - 250, -150, WIDTH + 150, 250],
                 fill=(color[0] // 5, color[1] // 5, color[2] // 5))

    # 顶部标题 / Top title
    bbox = draw.textbbox((0, 0), scene["cn_title"], font=fonts["cn_title"])
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 40),
              scene["cn_title"], fill=TEXT_COLOR, font=fonts["cn_title"])

    bbox = draw.textbbox((0, 0), scene["en_title"], font=fonts["en_title"])
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 120),
              scene["en_title"], fill=SUB_COLOR, font=fonts["en_title"])

    # ── 两张截图：答题前 vs 答题后 / Before vs After ──
    screenshots = scene.get("screenshots", [])
    shot_w, shot_h = 840, 470

    if len(screenshots) >= 2:
        # 左截图（答题前）/ Left (before)
        left = load_screenshot(screenshots[0], shot_w, shot_h)
        add_screenshot_frame(img, left, 60, 190, color)
        # 标签 / Label
        label_before = "答题前 / Before"
        draw_rounded_rect(draw, [60, 670, 60 + shot_w, 710], 16,
                          fill=(51, 65, 85))
        bbox = draw.textbbox((0, 0), label_before, font=fonts["label"])
        lw = bbox[2] - bbox[0]
        draw.text(((60 + 60 + shot_w - lw) // 2, 676),
                  label_before, fill=SUB_COLOR, font=fonts["label"])

        # 右截图（答题后）/ Right (after)
        right = load_screenshot(screenshots[1], shot_w, shot_h)
        add_screenshot_frame(img, right, 1020, 190, color)
        # 标签 / Label
        label_after = "答题后 / After"
        draw_rounded_rect(draw, [1020, 670, 1020 + shot_w, 710], 16,
                          fill=(51, 65, 85))
        bbox = draw.textbbox((0, 0), label_after, font=fonts["label"])
        lw = bbox[2] - bbox[0]
        draw.text(((1020 + 1020 + shot_w - lw) // 2, 676),
                  label_after, fill=SUB_COLOR, font=fonts["label"])

    # ── 底部描述 / Bottom description ──
    cn_lines = scene["cn_desc"].split("\n")
    en_lines = scene["en_desc"].split("\n")
    start_y = 740
    for i, (cn, en) in enumerate(zip(cn_lines, en_lines)):
        y = start_y + i * 80
        bbox_cn = draw.textbbox((0, 0), cn, font=fonts["cn_desc"])
        bbox_en = draw.textbbox((0, 0), en, font=fonts["en_desc"])
        cn_tw = bbox_cn[2] - bbox_cn[0]
        en_tw = bbox_en[2] - bbox_en[0]
        cx = WIDTH // 2
        draw.ellipse([cx - cn_tw // 2 - 20, y + 12,
                       cx - cn_tw // 2 - 10, y + 22], fill=color)
        draw.text((cx - cn_tw // 2, y), cn,
                  fill=TEXT_COLOR, font=fonts["cn_desc"])
        draw.text((cx - en_tw // 2, y + 38), en,
                  fill=SUB_COLOR, font=fonts["en_desc"])

    _draw_footer(draw, fonts, color, scene_idx, total_scenes)
    return img


def render_features_scene(scene, fonts, total_scenes, scene_idx):
    """
    渲染课程特色场景 / Render features/highlights scene.
    """
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    color = scene["color"]

    # 背景 / Background
    draw.rounded_rectangle([0, 0, WIDTH, 6], radius=0, fill=color)
    draw.ellipse([-150, -150, 250, 250],
                 fill=(color[0] // 5, color[1] // 5, color[2] // 5))
    draw.ellipse([WIDTH - 300, HEIGHT - 300, WIDTH + 100, HEIGHT + 100],
                 fill=(color[0] // 6, color[1] // 6, color[2] // 6))

    # 标题 / Title
    bbox = draw.textbbox((0, 0), scene["cn_title"], font=fonts["cn_title"])
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 180),
              scene["cn_title"], fill=TEXT_COLOR, font=fonts["cn_title"])

    bbox = draw.textbbox((0, 0), scene["en_title"], font=fonts["en_title"])
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 270),
              scene["en_title"], fill=SUB_COLOR, font=fonts["en_title"])

    # 装饰线 / Decorative line
    draw.rounded_rectangle(
        [(WIDTH - 100) // 2, 330, (WIDTH + 100) // 2, 336],
        radius=3, fill=color
    )

    # 特色列表 / Feature list
    cn_lines = scene["cn_desc"].split("\n")
    en_lines = scene["en_desc"].split("\n")
    for i, (cn, en) in enumerate(zip(cn_lines, en_lines)):
        y = 400 + i * 150
        # 背景卡片 / Background card
        card_w = 900
        card_x = (WIDTH - card_w) // 2
        draw_rounded_rect(draw,
                          [card_x, y - 10, card_x + card_w, y + 110],
                          16, fill=(30, 41, 59))
        # 左侧色条 / Left color bar
        draw.rounded_rectangle(
            [card_x, y - 10, card_x + 6, y + 110],
            radius=3, fill=color
        )
        draw.text((card_x + 30, y + 8), cn,
                  fill=TEXT_COLOR, font=fonts["cn_desc"])
        draw.text((card_x + 30, y + 54), en,
                  fill=SUB_COLOR, font=fonts["en_desc"])

    _draw_footer(draw, fonts, color, scene_idx, total_scenes)
    return img


def _draw_footer(draw, fonts, color, scene_idx, total_scenes):
    """绘制底部水印和进度条 / Draw footer watermark and progress bar."""
    # 水印 / Watermark
    wm = "AI Explorer | AI 探索之旅"
    bbox = draw.textbbox((0, 0), wm, font=fonts["watermark"])
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, HEIGHT - 50), wm,
              fill=(100, 116, 139), font=fonts["watermark"])

    # 进度条 / Progress bar
    progress = (scene_idx + 1) / total_scenes
    bar_y = HEIGHT - 8
    draw.rectangle([0, bar_y, WIDTH, HEIGHT], fill=(30, 41, 59))
    draw.rectangle([0, bar_y, int(WIDTH * progress), HEIGHT], fill=color)


def render_scene(scene_idx, scene, fonts, tmp_dir):
    """
    根据场景类型渲染对应的画面 / Render scene based on type.
    """
    total = len(SCENES)
    scene_type = scene.get("type", "title")

    if scene_type == "title":
        img = render_title_scene(scene, fonts, total, scene_idx)
    elif scene_type == "course":
        img = render_course_scene(scene, fonts, total, scene_idx)
    elif scene_type == "lesson_demo":
        img = render_lesson_demo_scene(scene, fonts, total, scene_idx)
    elif scene_type == "quiz_demo":
        img = render_quiz_demo_scene(scene, fonts, total, scene_idx)
    elif scene_type == "features":
        img = render_features_scene(scene, fonts, total, scene_idx)
    else:
        img = render_title_scene(scene, fonts, total, scene_idx)

    path = os.path.join(tmp_dir, f"scene_{scene_idx:02d}.png")
    img.save(path, "PNG")
    return path


async def generate_tts(scene_idx, tts_text, tmp_dir):
    """生成中文语音 / Generate Chinese TTS audio for a scene."""
    import edge_tts

    audio_path = os.path.join(tmp_dir, f"scene_{scene_idx:02d}.mp3")
    communicate = edge_tts.Communicate(tts_text, TTS_VOICE, rate="-5%")
    await communicate.save(audio_path)
    return audio_path


def get_audio_duration(audio_path):
    """获取音频时长(秒) / Get audio duration in seconds."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def assemble_video(scene_images, scene_audios, tmp_dir, output_path):
    """
    使用 ffmpeg 将图片和音频组合成视频
    Assemble images + audio into final MP4 using ffmpeg.
    """
    clips = []
    for i, (img_path, audio_path) in enumerate(zip(scene_images, scene_audios)):
        duration = get_audio_duration(audio_path)
        total_duration = duration + 1.6  # 0.8s 前后间隔 / padding
        clip_path = os.path.join(tmp_dir, f"clip_{i:02d}.mp4")

        subprocess.run([
            "ffmpeg", "-y",
            "-loop", "1", "-i", img_path,
            "-i", audio_path,
            "-filter_complex",
            f"[0:v]scale={WIDTH}:{HEIGHT},"
            f"fade=t=in:st=0:d=0.5,"
            f"fade=t=out:st={total_duration - 0.5}:d=0.5[v];"
            f"[1:a]adelay=800|800,"
            f"afade=t=out:st={total_duration - 0.5}:d=0.5[a]",
            "-map", "[v]", "-map", "[a]",
            "-t", str(total_duration),
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-r", str(FPS),
            clip_path
        ], check=True, capture_output=True)
        clips.append(clip_path)
        print(f"  片段 {i + 1}/{len(scene_images)} 完成 / Clip {i + 1} done")

    # 合并 / Concatenate
    concat_list = os.path.join(tmp_dir, "concat.txt")
    with open(concat_list, "w") as f:
        for clip in clips:
            f.write(f"file '{clip}'\n")

    print("\n合并所有片段 / Merging all clips...")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_list,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_path
    ], check=True, capture_output=True)


async def main():
    """主函数 / Main entry point."""
    project_dir = Path(__file__).parent
    output_path = str(project_dir / OUTPUT_FILE)

    print("=" * 60)
    print("  AI 探索之旅 — Demo 视频生成器 v2")
    print("  AI Explorer — Demo Video Generator v2")
    print("=" * 60)

    # 检查截图目录 / Check screenshots directory
    if not SCREENSHOT_DIR.exists():
        print(f"\n[错误] 截图目录不存在: {SCREENSHOT_DIR}")
        print("请先运行: uv run take_screenshots.py")
        return

    tmp_dir = tempfile.mkdtemp(prefix="ai_demo_")
    print(f"\n临时目录 / Temp dir: {tmp_dir}\n")

    try:
        # 1. 加载字体 / Load fonts
        print("1. 加载字体 / Loading fonts...")
        fonts = load_fonts()
        print("   完成 / Done.\n")

        # 2. 渲染场景图片 / Render scene images
        print("2. 渲染场景图片 / Rendering scene images...")
        scene_images = []
        for i, scene in enumerate(SCENES):
            img_path = render_scene(i, scene, fonts, tmp_dir)
            scene_images.append(img_path)
            print(f"   [{i + 1}/{len(SCENES)}] {scene['cn_title']}")
        print()

        # 3. 生成语音 / Generate TTS audio
        print("3. 生成中文配音 / Generating Chinese voiceover...")
        scene_audios = []
        for i, scene in enumerate(SCENES):
            audio_path = await generate_tts(i, scene["tts"], tmp_dir)
            scene_audios.append(audio_path)
            dur = get_audio_duration(audio_path)
            print(f"   [{i + 1}/{len(SCENES)}] {dur:.1f}s — {scene['cn_title']}")
        print()

        # 4. 组装视频 / Assemble video
        print("4. 组装视频 / Assembling video...")
        assemble_video(scene_images, scene_audios, tmp_dir, output_path)

        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"\n{'=' * 60}")
        print(f"  视频生成完成！/ Video generated successfully!")
        print(f"  输出文件 / Output: {output_path}")
        print(f"  文件大小 / Size: {size_mb:.1f} MB")
        print(f"  场景数量 / Scenes: {len(SCENES)}")
        print(f"{'=' * 60}")

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        print("\n临时文件已清理 / Temp files cleaned up.")


if __name__ == "__main__":
    asyncio.run(main())
