# /// script
# requires-python = ">=3.10"
# dependencies = ["beautifulsoup4", "lxml"]
# ///
"""Test bilingual coverage: every user-visible text element should have both zh and en spans."""

import json
import sys
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def collect_html_files():
    """Discover all HTML files across all editions."""
    files = [PROJECT_ROOT / "index.html"]
    for edition_dir in ["standard-5", "standard-15", "lab-10", "app-inventor-10", "web-ai-12"]:
        idx = PROJECT_ROOT / edition_dir / "index.html"
        if idx.exists():
            files.append(idx)
        lesson_dir = PROJECT_ROOT / edition_dir / "lessons"
        if lesson_dir.exists():
            files.extend(sorted(lesson_dir.glob("lesson*.html")))
    return files


HTML_FILES = collect_html_files()

results = []


def record(name, passed, detail=""):
    results.append({"test": name, "passed": passed, "detail": detail})


def load(path):
    return BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")


# Tags whose direct text children must be bilingual
BILINGUAL_TAGS = ["h1", "h2", "h3", "h4"]


def test_headings_bilingual():
    """All headings should contain both .zh and .en spans."""
    for f in HTML_FILES:
        soup = load(f)
        for tag_name in BILINGUAL_TAGS:
            tags = soup.find_all(tag_name)
            for tag in tags:
                # Skip if inside <code> or <pre>
                if tag.find_parent(["code", "pre"]):
                    continue
                zh = tag.find(class_="zh")
                en = tag.find(class_="en")
                has_both = zh is not None and en is not None
                # Some headings might be purely structural (no text) — skip
                text = tag.get_text(strip=True)
                if not text:
                    continue
                record(
                    f"bilingual_heading::{f.name}::{tag_name}::{text[:30]}",
                    has_both,
                    "missing .en" if not en else ("missing .zh" if not zh else ""),
                )


def test_buttons_bilingual():
    """Nav buttons and CTA buttons should be bilingual."""
    for f in HTML_FILES:
        soup = load(f)
        for btn in soup.find_all("button", class_=lambda c: c and ("lang-toggle" in c or "theme-toggle" in c)):
            # lang-toggle should have zh/en
            if "lang-toggle" in (btn.get("class") or []):
                zh = btn.find(class_="zh")
                en = btn.find(class_="en")
                record(f"bilingual_lang_toggle::{f.name}", zh is not None and en is not None)


def test_quiz_prompts_bilingual():
    """Quiz question prompts should have both languages."""
    for f in HTML_FILES:
        soup = load(f)
        prompts = soup.find_all(class_="quiz-prompt")
        for i, p in enumerate(prompts, 1):
            zh = p.find(class_="zh")
            en = p.find(class_="en")
            record(f"bilingual_quiz_prompt::{f.name}::Q{i}",
                   zh is not None and en is not None)


def test_quiz_options_bilingual():
    """Quiz options should have both languages."""
    for f in HTML_FILES:
        soup = load(f)
        options = soup.find_all("button", class_="quiz-option")
        missing_count = 0
        for opt in options:
            zh = opt.find(class_="zh")
            en = opt.find(class_="en")
            if not (zh and en):
                missing_count += 1
        record(f"bilingual_quiz_options::{f.name}",
               missing_count == 0,
               f"{missing_count} options missing bilingual" if missing_count else f"all {len(options)} bilingual")


def test_quiz_explanations_bilingual():
    """Quiz explanations should have both languages."""
    for f in HTML_FILES:
        soup = load(f)
        explanations = soup.find_all(class_="quiz-explanation")
        missing_count = 0
        for expl in explanations:
            zh = expl.find(class_="zh")
            en = expl.find(class_="en")
            if not (zh and en):
                missing_count += 1
        record(f"bilingual_quiz_explanations::{f.name}",
               missing_count == 0,
               f"{missing_count} missing bilingual" if missing_count else f"all {len(explanations)} bilingual")


def test_nav_lessons_bilingual():
    """Nav lesson links should be bilingual."""
    for f in HTML_FILES:
        soup = load(f)
        nav_lessons = soup.find(class_="nav-lessons")
        if not nav_lessons:
            continue
        links = nav_lessons.find_all("a")
        for a in links:
            zh = a.find(class_="zh")
            en = a.find(class_="en")
            record(f"bilingual_nav_link::{f.name}::{a.get_text(strip=True)[:20]}",
                   zh is not None and en is not None)


def test_footer_bilingual():
    for f in HTML_FILES:
        soup = load(f)
        footer = soup.find("footer")
        if not footer:
            continue
        zh = footer.find(class_="zh")
        en = footer.find(class_="en")
        record(f"bilingual_footer::{f.name}", zh is not None and en is not None)


def test_lesson_nav_footer_bilingual():
    """Prev/next navigation text should be bilingual across all editions."""
    lesson_dirs = [
        PROJECT_ROOT / "standard-5" / "lessons",
        PROJECT_ROOT / "standard-15" / "lessons",
        PROJECT_ROOT / "lab-10" / "lessons",
        PROJECT_ROOT / "app-inventor-10" / "lessons",
        PROJECT_ROOT / "web-ai-12" / "lessons",
    ]
    for ld in lesson_dirs:
        if not ld.exists():
            continue
        for f in sorted(ld.glob("lesson*.html")):
            soup = load(f)
            nav_footer = soup.find(class_="lesson-nav-footer")
            if not nav_footer:
                continue
            links = nav_footer.find_all("a")
            edition = ld.parent.name
            for a in links:
                zh = a.find(class_="zh")
                en = a.find(class_="en")
                record(f"bilingual_lesson_nav::{edition}/{f.name}::{a.get_text(strip=True)[:20]}",
                       zh is not None and en is not None)


# ---------- Run ----------

if __name__ == "__main__":
    test_headings_bilingual()
    test_buttons_bilingual()
    test_quiz_prompts_bilingual()
    test_quiz_options_bilingual()
    test_quiz_explanations_bilingual()
    test_nav_lessons_bilingual()
    test_footer_bilingual()
    test_lesson_nav_footer_bilingual()

    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"])
    total = len(results)

    report = {
        "suite": "Bilingual Coverage",
        "total": total,
        "passed": passed,
        "failed": failed,
        "results": results,
    }

    report_path = PROJECT_ROOT / "test" / "reports" / "bilingual_coverage.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  Bilingual Coverage Tests: {passed}/{total} passed, {failed} failed")
    print(f"{'='*60}")
    for r in results:
        icon = "PASS" if r["passed"] else "FAIL"
        line = f"  [{icon}] {r['test']}"
        if r["detail"]:
            line += f"  ({r['detail']})"
        print(line)

    sys.exit(0 if failed == 0 else 1)
