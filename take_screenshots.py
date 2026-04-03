# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "playwright>=1.40",
# ]
# ///
"""
take_screenshots.py — 使用 Playwright 截取课程页面截图
Take screenshots of course pages using Playwright + system Chromium.

用法 / Usage:
  uv run take_screenshots.py
"""

import asyncio
import os
from pathlib import Path

# ─── 配置 / Configuration ───────────────────────────────────────────
BASE_URL = "http://localhost:4200"
OUT_DIR = Path(__file__).parent / "screenshots"
CHROMIUM = "/usr/bin/chromium-browser"
VIEWPORT = {"width": 1920, "height": 1080}

# 截图任务列表 / Screenshot task list
# (filename, url_path, actions_before_screenshot)
TASKS = [
    # ── 版本首页截图 / Edition index screenshots ──
    ("edition_standard5.png",    "/standard-5/index.html",       None),
    ("edition_standard15.png",   "/standard-15/index.html",      None),
    ("edition_lab10.png",        "/lab-10/index.html",           None),
    ("edition_app10.png",        "/app-inventor-10/index.html",  None),
    ("edition_web12.png",        "/web-ai-12/index.html",        None),

    # ── 课程内容截图 / Lesson content screenshots ──
    # Standard-5 Lesson 1: hero + card grid
    ("lesson_s5_hero.png",       "/standard-5/lessons/lesson1.html", None),
    # Standard-5 Lesson 1: scroll to timeline
    ("lesson_s5_timeline.png",   "/standard-5/lessons/lesson1.html",
     {"scroll_to": "#section-1-3", "wait": 500}),
    # Standard-5 Lesson 1: scroll to AI-or-Human game
    ("lesson_s5_game.png",       "/standard-5/lessons/lesson1.html",
     {"scroll_to": ".ai-or-human", "wait": 500}),

    # Lab-10 Lesson 1: code block
    ("lesson_lab_code.png",      "/lab-10/lessons/lesson1.html",
     {"scroll_to": ".code-block", "wait": 500}),
    # Lab-10 Lesson 1: card grid
    ("lesson_lab_cards.png",     "/lab-10/lessons/lesson1.html",
     {"scroll_to": "#section-1-1", "wait": 500}),

    # Web-AI-12 Lesson 1: content
    ("lesson_web_content.png",   "/web-ai-12/lessons/lesson1.html",
     {"scroll_to": "#section-1-2", "wait": 500}),
    # Web-AI-12 Lesson 1: code block
    ("lesson_web_code.png",      "/web-ai-12/lessons/lesson1.html",
     {"scroll_to": ".code-block", "wait": 500}),

    # ── Quiz 截图 / Quiz screenshots ──
    # Standard-5: quiz before answering
    ("quiz_before.png",          "/standard-5/lessons/lesson1.html",
     {"scroll_to": ".quiz", "wait": 500}),
    # Standard-5: quiz after clicking correct answer
    ("quiz_after.png",           "/standard-5/lessons/lesson1.html",
     {"scroll_to": ".quiz", "wait": 300,
      "click": ".quiz-question[data-correct] .quiz-option:first-child",
      "post_wait": 800}),
    # Standard-5: quiz with explanation shown
    ("quiz_explained.png",       "/standard-5/lessons/lesson1.html",
     {"scroll_to": ".quiz", "wait": 300,
      "click_correct": True,  # 点击正确答案 / Click correct answer
      "post_wait": 800}),
]


async def take_screenshots():
    """截取所有截图 / Take all screenshots."""
    from playwright.async_api import async_playwright

    OUT_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=CHROMIUM,
            headless=True,
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"],
        )
        context = await browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=1,
        )

        for filename, url_path, actions in TASKS:
            out_path = OUT_DIR / filename
            page = await context.new_page()
            url = f"{BASE_URL}{url_path}"

            print(f"  截图 / Screenshot: {filename}")
            print(f"    URL: {url}")

            await page.goto(url, wait_until="networkidle")
            # 等待页面完全加载 / Wait for full load
            await page.wait_for_timeout(800)

            # 触发所有 reveal 动画 / Trigger all reveal animations
            await page.evaluate("""
                document.querySelectorAll('.reveal, .reveal-stagger')
                    .forEach(el => el.classList.add('revealed'));
            """)

            if actions:
                # 滚动到指定元素 / Scroll to target element
                if "scroll_to" in actions:
                    selector = actions["scroll_to"]
                    try:
                        el = page.locator(selector).first
                        await el.scroll_into_view_if_needed()
                        # 往上偏移一点，让元素不贴着顶部 / Offset up a bit
                        await page.evaluate("window.scrollBy(0, -100)")
                    except Exception as e:
                        print(f"    [warn] scroll_to {selector}: {e}")

                if "wait" in actions:
                    await page.wait_for_timeout(actions["wait"])

                # 点击指定元素 / Click a specific element
                if "click" in actions:
                    try:
                        await page.locator(actions["click"]).first.click()
                    except Exception as e:
                        print(f"    [warn] click {actions['click']}: {e}")

                # 点击正确答案 / Click the correct answer
                if actions.get("click_correct"):
                    try:
                        await page.evaluate("""
                            (() => {
                                const q = document.querySelector('.quiz-question[data-correct]');
                                if (!q) return;
                                const correct = q.getAttribute('data-correct');
                                const btn = q.querySelector(`.quiz-option[data-value="${correct}"]`);
                                if (btn) btn.click();
                            })()
                        """)
                    except Exception as e:
                        print(f"    [warn] click_correct: {e}")

                if "post_wait" in actions:
                    await page.wait_for_timeout(actions["post_wait"])

            await page.screenshot(path=str(out_path), full_page=False)
            await page.close()
            print(f"    -> {out_path}")

        await browser.close()

    print(f"\n所有截图完成！/ All screenshots done!")
    print(f"输出目录 / Output: {OUT_DIR}")
    # 列出文件 / List files
    for f in sorted(OUT_DIR.glob("*.png")):
        size_kb = f.stat().st_size / 1024
        print(f"  {f.name:30s} {size_kb:6.0f} KB")


if __name__ == "__main__":
    asyncio.run(take_screenshots())
