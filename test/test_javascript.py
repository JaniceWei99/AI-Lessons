# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Test JavaScript: verify required functions, event bindings, and localStorage usage."""

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
JS_FILE = PROJECT_ROOT / "js" / "main.js"

results = []


def record(name, passed, detail=""):
    results.append({"test": name, "passed": passed, "detail": detail})


js_text = JS_FILE.read_text(encoding="utf-8")


# ---------- Required Functions ----------

REQUIRED_FUNCTIONS = [
    "initTheme",
    "applyTheme",
    "initLang",
    "applyLang",
    "getProgress",
    "saveProgress",
    "markLessonQuiz",
    "updateProgressUI",
    "initQuizzes",
    "showQuizResult",
    "initDecisionTrees",
    "initAIorHuman",
    "initPromptChallenge",
    "initExpandableCards",
    "initCodeCopy",
    "initScrollReveal",
    "initMobileNav",
    "initTimeline",
]


def test_required_functions():
    for fn in REQUIRED_FUNCTIONS:
        pattern = re.compile(rf"function\s+{fn}\s*\(")
        record(f"js_function::{fn}", bool(pattern.search(js_text)))


# ---------- IIFE Encapsulation ----------

def test_iife():
    # Strip leading comments and whitespace before checking for IIFE
    import re
    stripped = re.sub(r'/\*[\s\S]*?\*/', '', js_text).strip()
    record("js_iife", stripped.startswith("(function") or stripped.startswith("(()") or "(function" in js_text)


def test_use_strict():
    record("js_use_strict", "'use strict'" in js_text or '"use strict"' in js_text)


# ---------- localStorage Keys ----------

def test_storage_keys():
    expected_keys = ["ai-class-theme", "ai-class-lang", "ai-class-progress"]
    for key in expected_keys:
        record(f"js_storage_key::{key}", key in js_text)


# ---------- Event Handling ----------

def test_event_listeners():
    record("js_click_events", "addEventListener('click'" in js_text or 'addEventListener("click"' in js_text)
    record("js_dom_ready", "DOMContentLoaded" in js_text)


# ---------- Feature: Theme Toggle ----------

def test_theme_toggle():
    record("js_theme_toggle_selector", "theme-toggle" in js_text)
    record("js_data_theme", "data-theme" in js_text)
    record("js_prefers_dark", "prefers-color-scheme" in js_text)


# ---------- Feature: Language Toggle ----------

def test_lang_toggle():
    record("js_lang_toggle_selector", "lang-toggle" in js_text)
    record("js_data_lang", "data-lang" in js_text)


# ---------- Feature: Quiz ----------

def test_quiz_logic():
    record("js_quiz_correct_class", "'correct'" in js_text or '"correct"' in js_text)
    record("js_quiz_wrong_class", "'wrong'" in js_text or '"wrong"' in js_text)
    record("js_quiz_disabled_class", "'disabled'" in js_text or '"disabled"' in js_text)
    record("js_quiz_data_correct", "data-correct" in js_text)
    record("js_quiz_data_value", "data-value" in js_text)
    record("js_quiz_explanation_reveal", "quiz-explanation" in js_text)
    record("js_quiz_score_display", "quiz-score" in js_text)


# ---------- Feature: Decision Tree ----------

def test_decision_tree():
    record("js_tree_node_active", "active" in js_text)
    record("js_tree_data_next", "data-next" in js_text)
    record("js_tree_restart", "tree-restart" in js_text)


# ---------- Feature: AI or Human ----------

def test_ai_or_human():
    record("js_aoh_data_answer", "data-answer" in js_text)
    record("js_aoh_data_choice", "data-choice" in js_text)
    record("js_aoh_reveal", "aoh-reveal" in js_text)


# ---------- Feature: Code Copy ----------

def test_code_copy():
    record("js_clipboard_api", "navigator.clipboard" in js_text)
    record("js_copy_feedback", "copied" in js_text)


# ---------- Feature: Scroll Reveal ----------

def test_scroll_reveal():
    record("js_intersection_observer", "IntersectionObserver" in js_text)
    record("js_reveal_visible", "'visible'" in js_text or '"visible"' in js_text)


# ---------- Feature: Mobile Nav ----------

def test_mobile_nav():
    record("js_hamburger", "nav-hamburger" in js_text)
    record("js_nav_lessons_open", "open" in js_text)


# ---------- Init Boot ----------

def test_init_boot():
    record("js_init_function", "function init()" in js_text)
    # All init functions should be called in init()
    init_calls = [
        "initTheme", "initLang", "initQuizzes", "initDecisionTrees",
        "initAIorHuman", "initPromptChallenge", "initExpandableCards",
        "initCodeCopy", "initScrollReveal", "initMobileNav", "initTimeline",
        "updateProgressUI",
    ]
    for fn in init_calls:
        record(f"js_init_calls::{fn}", f"{fn}()" in js_text)


# ---------- No Console Errors (static check) ----------

def test_no_console_log():
    """Production code should not have console.log (unless intentional)."""
    count = js_text.count("console.log")
    record("js_no_console_log", count == 0, f"{count} console.log found" if count else "")


# ---------- Run ----------

if __name__ == "__main__":
    test_required_functions()
    test_iife()
    test_use_strict()
    test_storage_keys()
    test_event_listeners()
    test_theme_toggle()
    test_lang_toggle()
    test_quiz_logic()
    test_decision_tree()
    test_ai_or_human()
    test_code_copy()
    test_scroll_reveal()
    test_mobile_nav()
    test_init_boot()
    test_no_console_log()

    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"])
    total = len(results)

    report = {
        "suite": "JavaScript Functionality",
        "total": total,
        "passed": passed,
        "failed": failed,
        "results": results,
    }

    report_path = PROJECT_ROOT / "test" / "reports" / "javascript_functionality.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  JavaScript Functionality Tests: {passed}/{total} passed, {failed} failed")
    print(f"{'='*60}")
    for r in results:
        icon = "PASS" if r["passed"] else "FAIL"
        line = f"  [{icon}] {r['test']}"
        if r["detail"]:
            line += f"  ({r['detail']})"
        print(line)

    sys.exit(0 if failed == 0 else 1)
