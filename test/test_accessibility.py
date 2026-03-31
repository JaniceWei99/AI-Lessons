# /// script
# requires-python = ">=3.10"
# dependencies = ["beautifulsoup4", "lxml"]
# ///
"""Test accessibility: ARIA labels, semantic HTML, alt text, focus indicators."""

import json
import sys
from pathlib import Path
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
CSS_FILE = PROJECT_ROOT / "css" / "style.css"

results = []


def record(name, passed, detail=""):
    results.append({"test": name, "passed": passed, "detail": detail})


def load(path):
    return BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")


# ---------- ARIA Labels ----------

def test_aria_labels():
    """Buttons without visible text should have aria-label."""
    for f in HTML_FILES:
        soup = load(f)
        # Theme toggle
        for btn in soup.find_all("button", class_="theme-toggle"):
            record(f"aria_theme_toggle::{f.name}",
                   btn.get("aria-label") is not None)
        # Lang toggle
        for btn in soup.find_all("button", class_="lang-toggle"):
            record(f"aria_lang_toggle::{f.name}",
                   btn.get("aria-label") is not None)
        # Hamburger
        for btn in soup.find_all("button", class_="nav-hamburger"):
            record(f"aria_hamburger::{f.name}",
                   btn.get("aria-label") is not None)


# ---------- Semantic HTML ----------

def test_semantic_structure():
    for f in HTML_FILES:
        soup = load(f)
        record(f"semantic_nav::{f.name}", soup.find("nav") is not None)
        record(f"semantic_footer::{f.name}", soup.find("footer") is not None)
        # At least one heading
        h1 = soup.find("h1")
        record(f"semantic_h1::{f.name}", h1 is not None)


def test_heading_hierarchy():
    """Page should start with h1; h2/h3/h4 may follow in any order within card components.
       We only check that h1 exists and no heading level > 4 is used (h5/h6 unnecessary)."""
    for f in HTML_FILES:
        soup = load(f)
        headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        levels = [int(h.name[1]) for h in headings]
        has_h1 = 1 in levels
        # Ensure first heading is h1
        first_is_h1 = levels[0] == 1 if levels else False
        # No h5/h6 should be used (over-nesting)
        no_deep_headings = all(l <= 4 for l in levels)
        valid = has_h1 and first_is_h1 and no_deep_headings
        record(f"heading_hierarchy::{f.name}", valid,
               f"levels: {levels[:10]}..." if len(levels) > 10 else f"levels: {levels}")


# ---------- Images ----------

def test_images_alt():
    """All <img> tags should have alt attributes."""
    for f in HTML_FILES:
        soup = load(f)
        imgs = soup.find_all("img")
        missing = [img.get("src", "?") for img in imgs if not img.get("alt")]
        record(f"img_alt::{f.name}",
               len(missing) == 0,
               f"{len(missing)} missing alt" if missing else f"{len(imgs)} images OK")


# ---------- Form Elements ----------

def test_textarea_labels():
    """Textarea inputs should have placeholder or associated label."""
    for f in HTML_FILES:
        soup = load(f)
        textareas = soup.find_all("textarea")
        for i, ta in enumerate(textareas, 1):
            has_placeholder = ta.get("placeholder") is not None
            has_label = ta.get("id") and soup.find("label", attrs={"for": ta.get("id")})
            record(f"textarea_accessible::{f.name}::#{i}",
                   has_placeholder or bool(has_label))


# ---------- Color Contrast (basic check) ----------

def test_focus_styles():
    """CSS should have :focus styles for interactive elements."""
    css_text = CSS_FILE.read_text(encoding="utf-8")
    record("css_focus_styles", ":focus" in css_text)


# ---------- Skip Link ----------

def test_skip_link():
    """Every page should have a skip-link pointing to #main-content."""
    for f in HTML_FILES:
        soup = load(f)
        skip = soup.find("a", class_="skip-link")
        has_skip = skip is not None
        correct_href = skip and skip.get("href") == "#main-content"
        record(f"skip_link_exists::{f.name}", has_skip)
        record(f"skip_link_href::{f.name}", bool(correct_href),
               skip.get("href", "missing") if skip else "no skip-link")


def test_main_content_id():
    """Every page should have an element with id='main-content'."""
    for f in HTML_FILES:
        soup = load(f)
        target = soup.find(id="main-content")
        record(f"main_content_id::{f.name}", target is not None)


# ---------- ARIA on Interactive Cards ----------

def test_expandable_card_aria():
    """Expandable card headers should have role=button, tabindex=0, aria-expanded."""
    for f in HTML_FILES:
        soup = load(f)
        headers = soup.find_all(class_="ec-header")
        for i, hdr in enumerate(headers, 1):
            has_role = hdr.get("role") == "button"
            has_tabindex = hdr.get("tabindex") == "0"
            has_aria = hdr.get("aria-expanded") is not None
            record(f"ec_header_role::{f.name}::#{i}", has_role)
            record(f"ec_header_tabindex::{f.name}::#{i}", has_tabindex)
            record(f"ec_header_aria_expanded::{f.name}::#{i}", has_aria)


def test_timeline_card_aria():
    """Timeline cards should have role=button and tabindex=0."""
    for f in HTML_FILES:
        soup = load(f)
        cards = soup.find_all(class_="timeline-card")
        for i, card in enumerate(cards, 1):
            has_role = card.get("role") == "button"
            has_tabindex = card.get("tabindex") == "0"
            record(f"timeline_card_role::{f.name}::#{i}", has_role)
            record(f"timeline_card_tabindex::{f.name}::#{i}", has_tabindex)


# ---------- Keyboard Navigation ----------

def test_interactive_are_focusable():
    """Interactive elements should be <button> or <a> (natively focusable)."""
    for f in HTML_FILES:
        soup = load(f)
        # Quiz options should be buttons
        quiz_opts = soup.find_all(class_="quiz-option")
        non_btn = [o.name for o in quiz_opts if o.name != "button"]
        record(f"quiz_opts_buttons::{f.name}",
               len(non_btn) == 0,
               f"{len(non_btn)} non-button quiz options" if non_btn else "")

        # Tree buttons should be buttons
        tree_btns = soup.find_all(class_="tree-btn")
        non_btn = [o.name for o in tree_btns if o.name != "button"]
        record(f"tree_btns_buttons::{f.name}",
               len(non_btn) == 0,
               f"{len(non_btn)} non-button tree btns" if non_btn else "")


# ---------- Viewport Meta ----------

def test_viewport_no_maximum_scale():
    """viewport should not restrict user zoom (no maximum-scale=1 or user-scalable=no)."""
    for f in HTML_FILES:
        soup = load(f)
        vp = soup.find("meta", attrs={"name": "viewport"})
        if not vp:
            record(f"viewport_zoom::{f.name}", False, "no viewport meta")
            continue
        content = (vp.get("content") or "").lower()
        restricts = "user-scalable=no" in content or "maximum-scale=1" in content
        record(f"viewport_zoom::{f.name}", not restricts,
               "zoom restricted" if restricts else "zoom allowed")


# ---------- Run ----------

if __name__ == "__main__":
    test_aria_labels()
    test_semantic_structure()
    test_heading_hierarchy()
    test_images_alt()
    test_textarea_labels()
    test_focus_styles()
    test_skip_link()
    test_main_content_id()
    test_expandable_card_aria()
    test_timeline_card_aria()
    test_interactive_are_focusable()
    test_viewport_no_maximum_scale()

    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"])
    total = len(results)

    report = {
        "suite": "Accessibility",
        "total": total,
        "passed": passed,
        "failed": failed,
        "results": results,
    }

    report_path = PROJECT_ROOT / "test" / "reports" / "accessibility.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  Accessibility Tests: {passed}/{total} passed, {failed} failed")
    print(f"{'='*60}")
    for r in results:
        icon = "PASS" if r["passed"] else "FAIL"
        line = f"  [{icon}] {r['test']}"
        if r["detail"]:
            line += f"  ({r['detail']})"
        print(line)

    sys.exit(0 if failed == 0 else 1)
