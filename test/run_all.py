# /// script
# requires-python = ">=3.10"
# dependencies = ["beautifulsoup4", "lxml"]
# ///
"""
AI-Class Test Runner
====================
Runs all test suites and generates:
  - Individual JSON reports in test/reports/
  - A consolidated HTML report in test/reports/report.html
"""

import json
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "test" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

TEST_SUITES = [
    ("HTML Structure & Validation", "test_html_structure.py", "html_structure.json"),
    ("Content Completeness", "test_content_completeness.py", "content_completeness.json"),
    ("Navigation & Links", "test_navigation.py", "navigation_links.json"),
    ("Bilingual Coverage", "test_bilingual.py", "bilingual_coverage.json"),
    ("CSS Component Coverage", "test_css.py", "css_coverage.json"),
    ("JavaScript Functionality", "test_javascript.py", "javascript_functionality.json"),
    ("Accessibility", "test_accessibility.py", "accessibility.json"),
]


def run_suite(script_name: str) -> tuple[int, str]:
    script_path = PROJECT_ROOT / "test" / script_name
    result = subprocess.run(
        ["uv", "run", str(script_path)],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
        timeout=120,
    )
    output = result.stdout + result.stderr
    return result.returncode, output


def load_report(json_name: str) -> dict:
    path = REPORTS_DIR / json_name
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"suite": json_name, "total": 0, "passed": 0, "failed": 0, "results": []}


def generate_html_report(all_reports: list[dict], timestamp: str) -> str:
    grand_total = sum(r["total"] for r in all_reports)
    grand_passed = sum(r["passed"] for r in all_reports)
    grand_failed = sum(r["failed"] for r in all_reports)
    pass_rate = f"{grand_passed / grand_total * 100:.1f}" if grand_total else "0"

    suites_html = ""
    for rpt in all_reports:
        status_class = "suite-pass" if rpt["failed"] == 0 else "suite-fail"
        suite_badge = "PASS" if rpt["failed"] == 0 else "FAIL"

        rows = ""
        for r in rpt["results"]:
            icon = '<span class="icon-pass">&#10004;</span>' if r["passed"] else '<span class="icon-fail">&#10008;</span>'
            detail_html = f'<span class="detail">{r["detail"]}</span>' if r.get("detail") else ""
            rows += f"""<tr class="{'row-pass' if r['passed'] else 'row-fail'}">
  <td>{icon}</td>
  <td>{r['test']}</td>
  <td>{detail_html}</td>
</tr>
"""

        suites_html += f"""
<div class="suite {status_class}">
  <div class="suite-header" onclick="this.parentElement.classList.toggle('open')">
    <span class="suite-badge {'badge-pass' if rpt['failed'] == 0 else 'badge-fail'}">{suite_badge}</span>
    <span class="suite-name">{rpt['suite']}</span>
    <span class="suite-stats">{rpt['passed']}/{rpt['total']} passed</span>
    <span class="suite-chevron">&#9660;</span>
  </div>
  <div class="suite-body">
    <table>
      <thead><tr><th></th><th>Test</th><th>Detail</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</div>
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI-Class Test Report — {timestamp}</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: "Segoe UI", system-ui, -apple-system, sans-serif; background: #0f172a; color: #e2e8f0; line-height: 1.6; padding: 2rem; }}
h1 {{ text-align: center; margin-bottom: 0.5rem; font-size: 1.8rem; }}
.timestamp {{ text-align: center; color: #94a3b8; font-size: 0.85rem; margin-bottom: 2rem; }}

/* Summary */
.summary {{ display: flex; gap: 1.5rem; justify-content: center; margin-bottom: 2.5rem; flex-wrap: wrap; }}
.summary-card {{ background: #1e293b; border-radius: 12px; padding: 1.25rem 2rem; text-align: center; min-width: 140px; border: 1px solid #334155; }}
.summary-card .num {{ font-size: 2rem; font-weight: 700; }}
.summary-card .label {{ font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; }}
.num-total {{ color: #a5b4fc; }}
.num-passed {{ color: #86efac; }}
.num-failed {{ color: #fca5a5; }}
.num-rate {{ color: #fde68a; }}

/* Progress bar */
.progress-bar {{ max-width: 600px; margin: 0 auto 2.5rem; height: 10px; background: #334155; border-radius: 5px; overflow: hidden; }}
.progress-fill {{ height: 100%; background: linear-gradient(90deg, #22c55e, #86efac); border-radius: 5px; transition: width 0.5s; }}

/* Suites */
.suite {{ background: #1e293b; border-radius: 12px; margin-bottom: 1rem; border: 1px solid #334155; overflow: hidden; }}
.suite-header {{ display: flex; align-items: center; gap: 0.75rem; padding: 1rem 1.25rem; cursor: pointer; user-select: none; }}
.suite-header:hover {{ background: rgba(99,102,241,0.06); }}
.suite-badge {{ padding: 2px 10px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.05em; }}
.badge-pass {{ background: rgba(34,197,94,0.15); color: #86efac; }}
.badge-fail {{ background: rgba(239,68,68,0.15); color: #fca5a5; }}
.suite-name {{ font-weight: 600; flex: 1; }}
.suite-stats {{ color: #94a3b8; font-size: 0.85rem; }}
.suite-chevron {{ color: #64748b; transition: transform 0.2s; }}
.suite.open .suite-chevron {{ transform: rotate(180deg); }}
.suite-body {{ display: none; }}
.suite.open .suite-body {{ display: block; }}

/* Table */
table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
th {{ text-align: left; padding: 0.5rem 1rem; background: rgba(0,0,0,0.2); color: #94a3b8; font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }}
td {{ padding: 0.4rem 1rem; border-top: 1px solid #1e293b; }}
.row-fail {{ background: rgba(239,68,68,0.04); }}
.icon-pass {{ color: #22c55e; }}
.icon-fail {{ color: #ef4444; }}
.detail {{ color: #94a3b8; font-size: 0.8rem; }}

@media (max-width: 640px) {{
  body {{ padding: 1rem; }}
  .summary {{ flex-direction: column; align-items: center; }}
  .summary-card {{ width: 100%; }}
}}
</style>
</head>
<body>
<h1>AI-Class Test Report</h1>
<p class="timestamp">{timestamp}</p>

<div class="summary">
  <div class="summary-card"><div class="num num-total">{grand_total}</div><div class="label">Total Tests</div></div>
  <div class="summary-card"><div class="num num-passed">{grand_passed}</div><div class="label">Passed</div></div>
  <div class="summary-card"><div class="num num-failed">{grand_failed}</div><div class="label">Failed</div></div>
  <div class="summary-card"><div class="num num-rate">{pass_rate}%</div><div class="label">Pass Rate</div></div>
</div>

<div class="progress-bar"><div class="progress-fill" style="width:{pass_rate}%"></div></div>

{suites_html}

</body>
</html>
"""


# ---------- Main ----------

if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*60}")
    print(f"  AI-Class Test Runner")
    print(f"  {timestamp}")
    print(f"{'='*60}\n")

    all_reports = []
    any_failure = False

    for suite_name, script, json_file in TEST_SUITES:
        print(f"  Running: {suite_name} ...", end=" ", flush=True)
        try:
            code, output = run_suite(script)
            report = load_report(json_file)
            all_reports.append(report)
            if code != 0:
                any_failure = True
                print(f"FAIL ({report['failed']} failures)")
            else:
                print(f"PASS ({report['passed']}/{report['total']})")
        except Exception as e:
            print(f"ERROR: {e}")
            all_reports.append({
                "suite": suite_name, "total": 1, "passed": 0, "failed": 1,
                "results": [{"test": "suite_execution", "passed": False, "detail": str(e)}],
            })
            any_failure = True

    # Generate HTML report
    html = generate_html_report(all_reports, timestamp)
    html_path = REPORTS_DIR / "report.html"
    html_path.write_text(html, encoding="utf-8")

    # Summary JSON
    summary = {
        "timestamp": timestamp,
        "suites": [{
            "name": r["suite"],
            "total": r["total"],
            "passed": r["passed"],
            "failed": r["failed"],
        } for r in all_reports],
        "grand_total": sum(r["total"] for r in all_reports),
        "grand_passed": sum(r["passed"] for r in all_reports),
        "grand_failed": sum(r["failed"] for r in all_reports),
    }
    summary_path = REPORTS_DIR / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    grand_total = summary["grand_total"]
    grand_passed = summary["grand_passed"]
    grand_failed = summary["grand_failed"]

    print(f"\n{'='*60}")
    print(f"  TOTAL: {grand_passed}/{grand_total} passed, {grand_failed} failed")
    print(f"  Reports: {REPORTS_DIR.relative_to(PROJECT_ROOT)}/")
    print(f"    - report.html   (visual report)")
    print(f"    - summary.json  (machine-readable)")
    print(f"{'='*60}\n")

    sys.exit(0 if not any_failure else 1)
