"""Post-run drift detection: compare latest case report with previous run.

Detects:
- Case went from failed → passed (fix applied)
- Case went from passed → failed (regression)
- New failure patterns not in SKILL.md known issues

Usage:
    python core/skills/builtin/structured-e2e/scripts/drift_check.py [case_id ...]

If no case_id given, checks all reports in tests/e2e_corevo/reports/.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPORTS_DIR = Path("tests/e2e_corevo/reports")
SKILL_FILE = Path("core/skills/builtin/structured-e2e/SKILL.md")

# Known pitfall patterns → keyword in error messages
# Each entry: (pitfall_name, [error_substring_matches])
# When adding a new pitfall here, also add it to SKILL.md "踩坑清单"
KNOWN_PITFALLS: list[tuple[str, list[str]]] = [
    ("wait_dom_reply missing", ["DOM text is empty after WS complete"]),
    ("dispatch panel overlay blocks send", ["intercepts pointer events"]),
    ("tab role is button not tab", ["found 0 time(s)", "role=\"tab\""]),
    ("input_box bounds too small", ["none were inside region 'input_box'"]),
    ("force click skips real interaction", ["Timed out waiting for WS task completion"]),
    ("assertion text from wrong component", ["Text not visible within"]),
    ("hover_target missing for orb", ["element is not visible"]),
]


def _load_report(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def _find_previous_report(case_id: str) -> dict | None:
    """Find the second-most-recent report for a case (the 'before' state)."""
    candidates = sorted(
        REPORTS_DIR.glob(f"{case_id}_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    # Latest is [0], previous is [1]
    if len(candidates) >= 2:
        return _load_report(candidates[1])
    return None


def _match_known_pitfalls(error_text: str) -> list[str]:
    matched = []
    lower = error_text.lower()
    for pitfall_name, keywords in KNOWN_PITFALLS:
        if any(kw.lower() in lower for kw in keywords):
            matched.append(pitfall_name)
    return matched


def _check_skill_doc(pitfall_name: str) -> bool:
    """Check if the pitfall is already documented in SKILL.md."""
    if not SKILL_FILE.exists():
        return False
    content = SKILL_FILE.read_text(encoding="utf-8").lower()
    # Use the pitfall name as a rough keyword check
    keywords = pitfall_name.lower().split()
    return all(kw in content for kw in keywords if len(kw) > 3)


def check_case(case_id: str) -> dict:
    """Check a single case for drift."""
    latest_path = REPORTS_DIR / f"{case_id}_latest.json"
    latest = _load_report(latest_path)
    if not latest:
        return {"case_id": case_id, "status": "no_report"}

    previous = _find_previous_report(case_id)
    current_status = latest.get("status", "unknown")
    prev_status = previous.get("status", "unknown") if previous else "unknown"

    result: dict = {
        "case_id": case_id,
        "current_status": current_status,
        "previous_status": prev_status,
        "transition": f"{prev_status} → {current_status}",
        "needs_doc_update": False,
        "new_pitfalls": [],
        "regression": False,
    }

    # Detect fix (failed → passed)
    if prev_status == "failed" and current_status == "passed":
        # Analyze what the previous failure was about
        prev_errors = []
        for step in previous.get("steps", []):
            if step.get("error"):
                prev_errors.append(step["error"])
        if previous.get("assertion_failures"):
            prev_errors.extend(previous["assertion_failures"])

        for error in prev_errors:
            matched = _match_known_pitfalls(error)
            for pitfall in matched:
                if not _check_skill_doc(pitfall):
                    result["new_pitfalls"].append({
                        "pitfall": pitfall,
                        "error_snippet": error[:200],
                        "documented": False,
                    })
                    result["needs_doc_update"] = True

    # Detect regression (passed → failed)
    if prev_status == "passed" and current_status == "failed":
        result["regression"] = True
        result["needs_doc_update"] = True

    return result


def main() -> None:
    case_ids = sys.argv[1:] if len(sys.argv) > 1 else [
        p.stem.replace("_latest", "")
        for p in REPORTS_DIR.glob("*_latest.json")
    ]

    results = []
    for case_id in sorted(set(case_ids)):
        result = check_case(case_id)
        results.append(result)

    output = {"checked": len(results), "results": results}
    print(json.dumps(output, ensure_ascii=False, indent=2))

    # Summary
    needs_update = [r for r in results if r.get("needs_doc_update")]
    regressions = [r for r in results if r.get("regression")]

    if needs_update:
        print(f"\n[ACTION] {len(needs_update)} case(s) need skill doc update:", file=sys.stderr)
        for r in needs_update:
            if r.get("new_pitfalls"):
                for p in r["new_pitfalls"]:
                    print(f"  - {r['case_id']}: new pitfall '{p['pitfall']}'", file=sys.stderr)
            if r.get("regression"):
                print(f"  - {r['case_id']}: REGRESSION {r['transition']}", file=sys.stderr)
        sys.exit(1)
    else:
        print("\n[OK] No skill doc updates needed.", file=sys.stderr)


if __name__ == "__main__":
    main()
