# /// script
# requires-python = ">=3.10"
# dependencies = ["beautifulsoup4", "lxml"]
# ///
"""Test HTML structure and validity for all pages."""

import json
import sys
from pathlib import Path
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def collect_html_files():
    """Discover all HTML files across all editions."""
    files = [PROJECT_ROOT / "index.html"]
    for edition_dir in ["standard-5", "standard-15", "lab-10"]:
        idx = PROJECT_ROOT / edition_dir / "index.html"
        if idx.exists():
            files.append(idx)
        lesson_dir = PROJECT_ROOT / edition_dir / "lessons"
        if lesson_dir.exists():
            files.extend(sorted(lesson_dir.glob("lesson*.html")))
    return files


HTML_FILES = collect_html_files()

results = []


def record(name: str, passed: bool, detail: str = ""):
    results.append({"test": name, "passed": passed, "detail": detail})


def load(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")


# ---------- Tests ----------

def test_files_exist():
    # Portal
    record("file_exists::index.html", (PROJECT_ROOT / "index.html").exists())
    # Standard-5
    record("file_exists::standard-5/index.html", (PROJECT_ROOT / "standard-5" / "index.html").exists())
    for i in range(1, 6):
        p = PROJECT_ROOT / "standard-5" / "lessons" / f"lesson{i}.html"
        record(f"file_exists::standard-5/lessons/lesson{i}.html", p.exists(), str(p))
    # Standard-15
    record("file_exists::standard-15/index.html", (PROJECT_ROOT / "standard-15" / "index.html").exists())
    for i in range(1, 16):
        p = PROJECT_ROOT / "standard-15" / "lessons" / f"lesson{i}.html"
        record(f"file_exists::standard-15/lessons/lesson{i}.html", p.exists(), str(p))
    # Lab-10
    record("file_exists::lab-10/index.html", (PROJECT_ROOT / "lab-10" / "index.html").exists())
    for i in range(1, 11):
        p = PROJECT_ROOT / "lab-10" / "lessons" / f"lesson{i}.html"
        record(f"file_exists::lab-10/lessons/lesson{i}.html", p.exists(), str(p))


def test_doctype_and_lang():
    for f in HTML_FILES:
        raw = f.read_text(encoding="utf-8")
        has_doctype = raw.strip().lower().startswith("<!doctype html>")
        record(f"doctype::{f.name}", has_doctype)

        soup = load(f)
        html_tag = soup.find("html")
        has_lang = html_tag and html_tag.get("lang")
        record(f"lang_attr::{f.name}", bool(has_lang), f"lang={html_tag.get('lang') if html_tag else 'N/A'}")


def test_meta_tags():
    for f in HTML_FILES:
        soup = load(f)
        charset = soup.find("meta", attrs={"charset": True})
        record(f"meta_charset::{f.name}", charset is not None)

        viewport = soup.find("meta", attrs={"name": "viewport"})
        record(f"meta_viewport::{f.name}", viewport is not None)

        title = soup.find("title")
        record(f"title_tag::{f.name}", title is not None and len(title.text.strip()) > 0,
               title.text.strip() if title else "missing")


def test_data_attributes():
    for f in HTML_FILES:
        soup = load(f)
        html_tag = soup.find("html")
        has_data_lang = html_tag and html_tag.get("data-lang")
        has_data_theme = html_tag and html_tag.get("data-theme")
        record(f"data-lang::{f.name}", bool(has_data_lang))
        record(f"data-theme::{f.name}", bool(has_data_theme))


def test_nav_structure():
    for f in HTML_FILES:
        soup = load(f)
        nav = soup.find("nav", class_="nav")
        record(f"nav_exists::{f.name}", nav is not None)

        if nav:
            logo = nav.find("a", class_="nav-logo")
            record(f"nav_logo::{f.name}", logo is not None)

            lang_btn = nav.find("button", class_="lang-toggle")
            record(f"nav_lang_toggle::{f.name}", lang_btn is not None)

            theme_btn = nav.find("button", class_="theme-toggle")
            record(f"nav_theme_toggle::{f.name}", theme_btn is not None)

            hamburger = nav.find("button", class_="nav-hamburger")
            record(f"nav_hamburger::{f.name}", hamburger is not None)


def test_footer_exists():
    for f in HTML_FILES:
        soup = load(f)
        footer = soup.find("footer", class_="footer")
        record(f"footer::{f.name}", footer is not None)


def test_css_js_linked():
    for f in HTML_FILES:
        soup = load(f)
        css_link = soup.find("link", attrs={"rel": "stylesheet"})
        record(f"css_linked::{f.name}", css_link is not None)

        scripts = soup.find_all("script", attrs={"src": True})
        has_main_js = any("main.js" in s.get("src", "") for s in scripts)
        record(f"js_linked::{f.name}", has_main_js)


def test_no_empty_tags():
    """Check that there are no completely empty heading or paragraph tags."""
    for f in HTML_FILES:
        soup = load(f)
        empty_count = 0
        for tag_name in ["h1", "h2", "h3", "p"]:
            for tag in soup.find_all(tag_name):
                if not tag.get_text(strip=True) and not tag.find_all(True):
                    empty_count += 1
        record(f"no_empty_tags::{f.name}", empty_count == 0,
               f"{empty_count} empty heading/paragraph tags found" if empty_count else "")


def test_svg_stroke_width_uniform():
    """Theme toggle SVG icons should have uniform stroke-width=1.5."""
    for f in HTML_FILES:
        soup = load(f)
        toggle = soup.find("button", class_="theme-toggle")
        if not toggle:
            continue
        svgs = toggle.find_all("svg")
        for i, svg in enumerate(svgs, 1):
            sw = svg.get("stroke-width", "")
            record(f"svg_stroke_uniform::{f.name}::#{i}",
                   sw == "1.5",
                   f"stroke-width={sw}" if sw != "1.5" else "")


# ---------- Run ----------

if __name__ == "__main__":
    test_files_exist()
    test_doctype_and_lang()
    test_meta_tags()
    test_data_attributes()
    test_nav_structure()
    test_footer_exists()
    test_css_js_linked()
    test_no_empty_tags()
    test_svg_stroke_width_uniform()

    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"])
    total = len(results)

    report = {
        "suite": "HTML Structure & Validation",
        "total": total,
        "passed": passed,
        "failed": failed,
        "results": results,
    }

    report_path = PROJECT_ROOT / "test" / "reports" / "html_structure.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  HTML Structure Tests: {passed}/{total} passed, {failed} failed")
    print(f"{'='*60}")
    for r in results:
        icon = "PASS" if r["passed"] else "FAIL"
        line = f"  [{icon}] {r['test']}"
        if r["detail"]:
            line += f"  ({r['detail']})"
        print(line)

    sys.exit(0 if failed == 0 else 1)
