# /// script
# requires-python = ">=3.10"
# dependencies = ["beautifulsoup4", "lxml"]
# ///
"""Test content completeness: verify all sections, quizzes, and interactive components per SPEC."""

import json
import sys
from pathlib import Path
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parent.parent
results = []

# Expected structure per SPEC.md (standard-5 edition)
EXPECTED = {
    "lesson1": {
        "file": "standard-5/lessons/lesson1.html",
        "quiz_id": "lesson1",
        "quiz_count": 5,
        "sections_min": 6,
        "interactive": ["timeline", "ai-or-human", "quiz"],
        "keywords_zh": ["人工智能", "图灵", "AlphaGo", "ChatGPT", "感知", "推理", "创造"],
    },
    "lesson2": {
        "file": "standard-5/lessons/lesson2.html",
        "quiz_id": "lesson2",
        "quiz_count": 5,
        "sections_min": 6,
        "interactive": ["decision-tree", "code-block", "quiz"],
        "keywords_zh": ["监督学习", "无监督学习", "强化学习", "数据", "决策树"],
    },
    "lesson3": {
        "file": "standard-5/lessons/lesson3.html",
        "quiz_id": "lesson3",
        "quiz_count": 5,
        "sections_min": 7,
        "interactive": ["expandable-card", "quiz"],
        "keywords_zh": ["神经元", "神经网络", "深度学习", "卷积", "反向传播"],
    },
    "lesson4": {
        "file": "standard-5/lessons/lesson4.html",
        "quiz_id": "lesson4",
        "quiz_count": 5,
        "sections_min": 8,
        "interactive": ["prompt-challenge", "expandable-card", "quiz"],
        "keywords_zh": ["Token", "Transformer", "注意力", "Prompt", "AIGC"],
    },
    "lesson5": {
        "file": "standard-5/lessons/lesson5.html",
        "quiz_id": "lesson5",
        "quiz_count": 10,
        "sections_min": 8,
        "interactive": ["expandable-card", "prompt-challenge", "quiz"],
        "keywords_zh": ["偏见", "隐私", "深度伪造", "批判性思维", "创造力"],
    },
}


def record(name, passed, detail=""):
    results.append({"test": name, "passed": passed, "detail": detail})


def load(rel_path):
    p = PROJECT_ROOT / rel_path
    return BeautifulSoup(p.read_text(encoding="utf-8"), "lxml")


def test_sections():
    for lid, spec in EXPECTED.items():
        soup = load(spec["file"])
        sections = soup.find_all("div", class_="section")
        # also count sections that may use <section> tag
        sections += soup.find_all("section", class_="section")
        count = len(sections)
        record(
            f"sections_count::{lid}",
            count >= spec["sections_min"],
            f"found {count}, expected >= {spec['sections_min']}",
        )


def test_quiz_exists_and_count():
    for lid, spec in EXPECTED.items():
        soup = load(spec["file"])
        quiz = soup.find("div", class_="quiz", attrs={"data-quiz-id": spec["quiz_id"]})
        record(f"quiz_exists::{lid}", quiz is not None)

        if quiz:
            questions = quiz.find_all("div", class_="quiz-question")
            record(
                f"quiz_question_count::{lid}",
                len(questions) == spec["quiz_count"],
                f"found {len(questions)}, expected {spec['quiz_count']}",
            )
            # Each question should have data-correct
            for i, q in enumerate(questions, 1):
                has_correct = q.get("data-correct") is not None
                record(f"quiz_q{i}_has_answer::{lid}", has_correct)
            # Each question should have 4 options
            for i, q in enumerate(questions, 1):
                opts = q.find_all("button", class_="quiz-option")
                record(
                    f"quiz_q{i}_options::{lid}",
                    len(opts) == 4,
                    f"found {len(opts)} options",
                )
            # Quiz result container
            result_div = quiz.find("div", class_="quiz-result")
            record(f"quiz_result_container::{lid}", result_div is not None)
        else:
            record(f"quiz_question_count::{lid}", False, "quiz not found")


def test_interactive_components():
    for lid, spec in EXPECTED.items():
        soup = load(spec["file"])
        for component in spec["interactive"]:
            if component == "quiz":
                continue  # tested separately
            elif component == "timeline":
                el = soup.find("div", class_="timeline")
                items = el.find_all("div", class_="timeline-item") if el else []
                record(f"interactive_timeline::{lid}", el is not None and len(items) >= 4,
                       f"{len(items)} items" if el else "missing")
            elif component == "ai-or-human":
                el = soup.find("div", class_="ai-or-human")
                items = el.find_all("div", class_="aoh-item") if el else []
                record(f"interactive_ai_or_human::{lid}", el is not None and len(items) >= 3,
                       f"{len(items)} items" if el else "missing")
            elif component == "decision-tree":
                el = soup.find("div", class_="decision-tree")
                nodes = el.find_all("div", class_="tree-node") if el else []
                record(f"interactive_decision_tree::{lid}", el is not None and len(nodes) >= 3,
                       f"{len(nodes)} nodes" if el else "missing")
            elif component == "code-block":
                els = soup.find_all("div", class_="code-block")
                record(f"interactive_code_block::{lid}", len(els) >= 1,
                       f"{len(els)} code blocks")
            elif component == "expandable-card":
                els = soup.find_all("div", class_="expandable-card")
                record(f"interactive_expandable_cards::{lid}", len(els) >= 1,
                       f"{len(els)} expandable cards")
            elif component == "prompt-challenge":
                els = soup.find_all("div", class_="prompt-challenge")
                record(f"interactive_prompt_challenge::{lid}", len(els) >= 1,
                       f"{len(els)} prompt challenges")


def test_quiz_explanations():
    for lid, spec in EXPECTED.items():
        soup = load(spec["file"])
        quiz = soup.find("div", class_="quiz", attrs={"data-quiz-id": spec["quiz_id"]})
        if not quiz:
            record(f"quiz_explanations::{lid}", False, "quiz not found")
            continue
        questions = quiz.find_all("div", class_="quiz-question")
        has_all = True
        missing = []
        for i, q in enumerate(questions, 1):
            expl = q.find(class_="quiz-explanation")
            if not expl or not expl.get_text(strip=True):
                has_all = False
                missing.append(f"Q{i}")
        record(f"quiz_explanations::{lid}", has_all,
               f"missing explanations: {', '.join(missing)}" if missing else "all present")


def test_keywords_present():
    for lid, spec in EXPECTED.items():
        soup = load(spec["file"])
        text = soup.get_text()
        missing = [kw for kw in spec["keywords_zh"] if kw not in text]
        record(f"keywords_zh::{lid}", len(missing) == 0,
               f"missing: {', '.join(missing)}" if missing else "all found")


def test_hero_section():
    for lid, spec in EXPECTED.items():
        soup = load(spec["file"])
        hero = soup.find(class_="hero")
        record(f"hero_section::{lid}", hero is not None)
        if hero:
            h1 = hero.find("h1")
            record(f"hero_title::{lid}", h1 is not None and len(h1.get_text(strip=True)) > 0)


def test_lesson_nav_footer():
    for lid, spec in EXPECTED.items():
        soup = load(spec["file"])
        nav_footer = soup.find(class_="lesson-nav-footer")
        record(f"lesson_nav_footer::{lid}", nav_footer is not None)


# ---------- Homepage / Portal specific ----------
def test_homepage():
    soup = load("index.html")
    hero = soup.find(class_="hero")
    record("portal_hero", hero is not None)

    edition_cards = soup.find_all("div", class_="edition-card")
    record("portal_edition_cards", len(edition_cards) == 5, f"found {len(edition_cards)}")

    features = soup.find_all("div", class_="feature-card")
    record("portal_feature_cards", len(features) == 4, f"found {len(features)}")

    edition_ctas = soup.find_all("a", class_="edition-cta")
    record("portal_edition_ctas", len(edition_ctas) == 5, f"found {len(edition_ctas)}")


def test_edition_index_pages():
    """Each edition index.html should have a hero and lesson cards."""
    editions = {
        "standard-5": {"lesson_count": 5},
        "standard-15": {"lesson_count": 15},
        "lab-10": {"lesson_count": 10},
        "app-inventor-10": {"lesson_count": 10},
        "web-ai-12": {"lesson_count": 12},
    }
    for name, spec in editions.items():
        idx = PROJECT_ROOT / name / "index.html"
        if not idx.exists():
            record(f"edition_index_exists::{name}", False, "file not found")
            continue
        soup = load(f"{name}/index.html")
        hero = soup.find(class_="hero")
        record(f"edition_hero::{name}", hero is not None)
        cards = soup.find_all("div", class_="lesson-card")
        record(f"edition_lesson_cards::{name}", len(cards) == spec["lesson_count"],
               f"found {len(cards)}, expected {spec['lesson_count']}")


def test_edition_lessons_basic():
    """Basic structure check for all edition lesson files."""
    for edition_dir in ["standard-15", "lab-10", "app-inventor-10", "web-ai-12"]:
        lesson_dir = PROJECT_ROOT / edition_dir / "lessons"
        if not lesson_dir.exists():
            continue
        for f in sorted(lesson_dir.glob("lesson*.html")):
            soup = BeautifulSoup(f.read_text(encoding="utf-8"), "lxml")
            # Has hero
            hero = soup.find(class_="hero")
            record(f"basic_hero::{edition_dir}/{f.name}", hero is not None)
            # Has quiz
            quiz = soup.find("div", class_="quiz")
            record(f"basic_quiz::{edition_dir}/{f.name}", quiz is not None)
            # Has content sections
            sections = soup.find_all("section", class_="section")
            record(f"basic_sections::{edition_dir}/{f.name}", len(sections) >= 3,
                   f"found {len(sections)}")
            # Has footer
            footer = soup.find("footer")
            record(f"basic_footer::{edition_dir}/{f.name}", footer is not None)


# ---------- Run ----------

if __name__ == "__main__":
    test_sections()
    test_quiz_exists_and_count()
    test_quiz_explanations()
    test_interactive_components()
    test_keywords_present()
    test_hero_section()
    test_lesson_nav_footer()
    test_homepage()
    test_edition_index_pages()
    test_edition_lessons_basic()

    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"])
    total = len(results)

    report = {
        "suite": "Content Completeness",
        "total": total,
        "passed": passed,
        "failed": failed,
        "results": results,
    }

    report_path = PROJECT_ROOT / "test" / "reports" / "content_completeness.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"  Content Completeness Tests: {passed}/{total} passed, {failed} failed")
    print(f"{'='*60}")
    for r in results:
        icon = "PASS" if r["passed"] else "FAIL"
        line = f"  [{icon}] {r['test']}"
        if r["detail"]:
            line += f"  ({r['detail']})"
        print(line)

    sys.exit(0 if failed == 0 else 1)
