# /// script
# requires-python = ">=3.10"
# dependencies = ["beautifulsoup4", "lxml"]
# ///
"""Test navigation links: verify all internal links point to existing files."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

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


def resolve_link(base_file: Path, href: str) -> Path | None:
    """Resolve a relative href to an absolute path."""
    parsed = urlparse(href)
    if parsed.scheme in ("http", "https", "mailto", ""):
        if parsed.netloc:
            return None  # external link
    clean = href.split("#")[0].split("?")[0]
    if not clean:
        return None  # anchor-only link
    return (base_file.parent / clean).resolve()


def test_internal_links():
    for f in HTML_FILES:
        soup = load(f)
        links = soup.find_all("a", href=True)
        for a in links:
            href = a["href"]
            parsed = urlparse(href)
            # Skip external links
            if parsed.scheme in ("http", "https", "mailto"):
                record(f"external_link::{f.name}::{href[:50]}",
                       True, "external — skipped")
                continue
            target = resolve_link(f, href)
            if target is None:
                continue  # anchor-only
            exists = target.exists()
            record(f"internal_link::{f.name}->{target.name}",
                   exists, href)


def test_css_link():
    for f in HTML_FILES:
        soup = load(f)
        for link in soup.find_all("link", attrs={"rel": "stylesheet"}):
            href = link.get("href", "")
            if href.startswith("http"):
                record(f"css_external::{f.name}", True, href[:60])
                continue
            target = resolve_link(f, href)
            if target:
                record(f"css_file::{f.name}->{target.name}", target.exists(), href)


def test_js_link():
    for f in HTML_FILES:
        soup = load(f)
        for script in soup.find_all("script", src=True):
            src = script["src"]
            if src.startswith("http"):
                record(f"js_external::{f.name}", True, src[:60])
                continue
            target = resolve_link(f, src)
            if target:
                record(f"js_file::{f.name}->{target.name}", target.exists(), src)


def natural_sort_key(path):
    """Sort lesson files by numeric order (lesson1 < lesson2 < lesson10)."""
    m = re.search(r'(\d+)', path.stem)
    return int(m.group(1)) if m else 0


def test_lesson_prev_next():
    """Verify prev/next links in lesson footer navigation across all editions."""
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
        lessons = sorted(ld.glob("lesson*.html"), key=natural_sort_key)
        edition = ld.parent.name
        for i, f in enumerate(lessons):
            soup = load(f)
            nav_footer = soup.find(class_="lesson-nav-footer")
            if not nav_footer:
                record(f"prev_next_nav::{edition}/{f.name}", False, "lesson-nav-footer missing")
                continue
            links = nav_footer.find_all("a", href=True)
            hrefs = [a["href"] for a in links]

            if i == 0:
                has_no_prev_lesson = not any("lesson0" in h for h in hrefs)
                record(f"first_lesson_no_prev::{edition}/{f.name}", has_no_prev_lesson)
            if i == len(lessons) - 1:
                has_index = any("index" in h for h in hrefs)
                record(f"last_lesson_to_index::{edition}/{f.name}", has_index,
                       f"links: {hrefs}")

            for href in hrefs:
                target = resolve_link(f, href)
                if target:
                    record(f"nav_footer_link::{edition}/{f.name}->{target.name}", target.exists(), href)


def test_homepage_lesson_links():
    """Portal page should link to edition index pages."""
    soup = load(PROJECT_ROOT / "index.html")
    # Check edition links
    edition_links = soup.find_all("a", class_="edition-cta")
    for a in edition_links:
        href = a.get("href", "")
        target = resolve_link(PROJECT_ROOT / "index.html", href)
        if target:
            record(f"portal_edition_link::{target.name}", target.exists(), href)

    # Check edition index pages link to their lessons
    for edition_dir in ["standard-5", "standard-15", "lab-10", "app-inventor-10", "web-ai-12"]:
        idx = PROJECT_ROOT / edition_dir / "index.html"
        if not idx.exists():
            continue
        s = load(idx)
        cards = s.find_all("div", class_="lesson-card")
        for card in cards:
            lid = card.get("data-lesson", "?")
            link = card.find("a", href=True)
            if not link:
                record(f"edition_card_link::{edition_dir}/{lid}", False, "no link found")
                continue
            target = resolve_link(idx, link["href"])
            if target:
                record(f"edition_card_link::{edition_dir}/{lid}", target.exists(), link["href"])


# ---------- Run ----------

if __name__ == "__main__":
    test_internal_links()
    test_css_link()
    test_js_link()
    test_lesson_prev_next()
    test_homepage_lesson_links()

    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"])
    total = len(results)

    report = {
        "suite": "Navigation & Links",
        "total": total,
        "passed": passed,
        "failed": failed,
        "results": results,
    }

    report_path = PROJECT_ROOT / "test" / "reports" / "navigation_links.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  Navigation & Links Tests: {passed}/{total} passed, {failed} failed")
    print(f"{'='*60}")
    for r in results:
        icon = "PASS" if r["passed"] else "FAIL"
        line = f"  [{icon}] {r['test']}"
        if r["detail"]:
            line += f"  ({r['detail']})"
        print(line)

    sys.exit(0 if failed == 0 else 1)
