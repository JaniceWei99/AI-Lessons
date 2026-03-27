# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Test CSS: verify required component styles, design tokens, responsive breakpoints, and print styles."""

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSS_FILE = PROJECT_ROOT / "css" / "style.css"

results = []


def record(name, passed, detail=""):
    results.append({"test": name, "passed": passed, "detail": detail})


css_text = CSS_FILE.read_text(encoding="utf-8")


# ---------- Design Tokens ----------

def test_css_variables():
    tokens = {
        "--c-primary": "#6366f1",
        "--c-secondary": "#06b6d4",
        "--c-accent": "#f59e0b",
        "--c-success": "#22c55e",
        "--c-error": "#ef4444",
        "--c-bg": "#f8fafc",
        "--c-text": "#1e293b",
    }
    for var, expected in tokens.items():
        pattern = re.compile(rf"{re.escape(var)}\s*:\s*{re.escape(expected)}")
        record(f"css_var::{var}", bool(pattern.search(css_text)), expected)


def test_dark_mode_tokens():
    record("dark_mode_selector", '[data-theme="dark"]' in css_text)
    dark_vars = ["--c-bg: #0f172a", "--c-card: #1e293b", "--c-text: #e2e8f0"]
    for v in dark_vars:
        record(f"dark_mode_var::{v.split(':')[0].strip()}", v.replace(" ", "") in css_text.replace(" ", ""))


def test_font_families():
    record("font_body", "Noto Sans SC" in css_text)
    record("font_code", "JetBrains Mono" in css_text or "Fira Code" in css_text)


# ---------- Component Styles ----------

REQUIRED_SELECTORS = [
    ".nav",
    ".hero",
    ".card",
    ".lesson-card",
    ".quiz",
    ".quiz-option",
    ".quiz-option.correct",
    ".quiz-option.wrong",
    ".quiz-explanation",
    ".quiz-result",
    ".timeline",
    ".timeline-item",
    ".timeline-card",
    ".decision-tree",
    ".tree-node",
    ".tree-btn",
    ".ai-or-human",
    ".aoh-item",
    ".aoh-btn",
    ".prompt-challenge",
    ".pc-input",
    ".pc-reveal-btn",
    ".pc-reference",
    ".expandable-card",
    ".ec-header",
    ".ec-body",
    ".code-block",
    ".code-pre",
    ".code-copy-btn",
    ".info-box",
    ".lesson-nav-footer",
    ".footer",
    ".hidden",
]


def test_required_selectors():
    for sel in REQUIRED_SELECTORS:
        # Simple check: the selector text appears in CSS
        found = sel in css_text
        record(f"css_selector::{sel}", found)


# ---------- Bilingual CSS ----------

def test_bilingual_css_rules():
    record("bilingual_zh_hide_en", '[data-lang="zh"] .en' in css_text)
    record("bilingual_en_hide_zh", '[data-lang="en"] .zh' in css_text)


# ---------- Responsive ----------

def test_responsive_breakpoints():
    record("breakpoint_1023", "@media" in css_text and "1023px" in css_text)
    record("breakpoint_767", "@media" in css_text and "767px" in css_text)


def test_mobile_nav():
    record("mobile_nav_hamburger", ".nav-hamburger" in css_text)
    record("mobile_nav_lessons_open", ".nav-lessons.open" in css_text)


# ---------- Print ----------

def test_print_styles():
    record("print_media_query", "@media print" in css_text)
    record("print_hide_nav", "print" in css_text and ".nav" in css_text)


# ---------- Animations ----------

def test_animations():
    record("transition_base", "--tr-base" in css_text)
    record("scroll_reveal", ".reveal" in css_text)
    record("fade_slide_keyframe", "fadeSlideIn" in css_text)
    record("hover_effects", "translateY(-4px)" in css_text)


# ---------- Accessibility Styles ----------

def test_focus_visible():
    """CSS should have :focus-visible styles."""
    record("focus_visible", ":focus-visible" in css_text)


def test_prefers_reduced_motion():
    """CSS should respect prefers-reduced-motion."""
    record("prefers_reduced_motion", "prefers-reduced-motion" in css_text)


def test_active_states():
    """CSS should have :active states for touch feedback."""
    record("active_state_card", ":active" in css_text and "scale(0.98)" in css_text)
    record("active_state_button", ":active" in css_text and "scale(0.96)" in css_text)


def test_skip_link_styles():
    """CSS should have .skip-link styles."""
    record("skip_link_style", ".skip-link" in css_text)


def test_dark_mode_nav_portal():
    """CSS should have dark mode adaptation for nav-portal."""
    record("dark_nav_portal", ".nav-portal" in css_text and "#93c5fd" in css_text)


# ---------- Syntax Highlighting ----------

def test_syntax_colors():
    for cls in [".kw", ".fn", ".str", ".num", ".cm"]:
        record(f"syntax_color::{cls}", f".code-pre {cls}" in css_text)


# ---------- Run ----------

if __name__ == "__main__":
    test_css_variables()
    test_dark_mode_tokens()
    test_font_families()
    test_required_selectors()
    test_bilingual_css_rules()
    test_responsive_breakpoints()
    test_mobile_nav()
    test_print_styles()
    test_animations()
    test_focus_visible()
    test_prefers_reduced_motion()
    test_active_states()
    test_skip_link_styles()
    test_dark_mode_nav_portal()
    test_syntax_colors()

    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"])
    total = len(results)

    report = {
        "suite": "CSS Component Coverage",
        "total": total,
        "passed": passed,
        "failed": failed,
        "results": results,
    }

    report_path = PROJECT_ROOT / "test" / "reports" / "css_coverage.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  CSS Coverage Tests: {passed}/{total} passed, {failed} failed")
    print(f"{'='*60}")
    for r in results:
        icon = "PASS" if r["passed"] else "FAIL"
        line = f"  [{icon}] {r['test']}"
        if r["detail"]:
            line += f"  ({r['detail']})"
        print(line)

    sys.exit(0 if failed == 0 else 1)
