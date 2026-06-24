"""Run a case and check for skill drift afterward.

Wraps run_case.py: runs the case, then checks if the result
reveals a new pitfall or regression that should be documented.

Usage:
    python core/skills/builtin/structured-e2e/scripts/run_with_drift.py --case tests/e2e_corevo/fixtures/cases/case_XXX.json --headed

Exit codes:
    0 = case passed, no drift
    1 = case failed
    2 = case passed but skill docs need update (drift detected)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Run case + drift check")
    parser.add_argument("--case", required=True, help="Path to case JSON")
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--timeout-ms", type=int, default=120000)
    args = parser.parse_args()

    # Run the case
    cmd = [sys.executable, "-m", "tests.e2e_corevo.tools.run_case",
           "--case", args.case]
    if args.headed:
        cmd.append("--headed")
    cmd.extend(["--timeout-ms", str(args.timeout_ms)])

    env = {**__import__("os").environ, "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)

    # Print case output
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

    case_failed = result.returncode != 0

    # Run drift check
    drift_result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "drift_check.py")],
        capture_output=True, text=True,
    )

    if drift_result.stdout:
        try:
            drift_data = json.loads(drift_result.stdout)
        except json.JSONDecodeError:
            drift_data = None
    else:
        drift_data = None

    # Determine exit code
    if case_failed:
        return 1

    if drift_data:
        needs_update = [r for r in drift_data.get("results", [])
                        if r.get("needs_doc_update")]
        if needs_update:
            print(f"\n[DRIFT] {len(needs_update)} case(s) need skill doc update:")
            for r in needs_update:
                if r.get("new_pitfalls"):
                    for p in r["new_pitfalls"]:
                        print(f"  NEW PITFALL: {p['pitfall']}")
                        print(f"    Error: {p['error_snippet'][:120]}")
                if r.get("regression"):
                    print(f"  REGRESSION: {r['case_id']} {r['transition']}")
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
