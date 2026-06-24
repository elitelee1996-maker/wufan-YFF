"""Coverage audit for E2E test fixtures.

Usage:
    python core/skills/builtin/structured-e2e/scripts/coverage_report.py

Scans tests/e2e_corevo/fixtures/ and outputs JSON + human-readable summary
of current map/rule/case coverage.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

FIXTURES_DIR = Path("tests/e2e_corevo/fixtures")
MAPS_DIR = FIXTURES_DIR / "maps"
RULES_DIR = FIXTURES_DIR / "rules"
CASES_DIR = FIXTURES_DIR / "cases"
ACTIONS_FILE = FIXTURES_DIR / "actions" / "browser_actions.json"


def _scan_maps() -> list[dict]:
    items = []
    for map_dir in sorted(MAPS_DIR.iterdir()):
        map_json = map_dir / "map.json"
        if not map_json.exists():
            continue
        data = json.loads(map_json.read_text(encoding="utf-8"))
        regions = data.get("regions", [])
        region_ids = [r["region_id"] for r in regions]
        controls = sum(len(r.get("controls", [])) for r in regions)
        items.append({
            "name": map_dir.name,
            "map_id": data.get("map_id", map_dir.name),
            "regions": region_ids,
            "region_count": len(region_ids),
            "control_count": controls,
            "state": data.get("page", {}).get("state", ""),
        })
    return items


def _scan_rules() -> list[dict]:
    items = []
    for rule_file in sorted(RULES_DIR.glob("*.rules.json")):
        data = json.loads(rule_file.read_text(encoding="utf-8"))
        rules = data.get("rules", [])
        items.append({
            "ruleset_id": data.get("ruleset_id", rule_file.stem),
            "map_ref": data.get("map_ref", ""),
            "rule_count": len(rules),
            "rule_ids": [r.get("rule_id", "") for r in rules],
        })
    return items


def _scan_actions() -> list[dict]:
    if not ACTIONS_FILE.exists():
        return []
    data = json.loads(ACTIONS_FILE.read_text(encoding="utf-8"))
    return [
        {"action_id": a["action_id"], "description": a.get("description", "")}
        for a in data.get("actions", [])
    ]


def _scan_cases() -> list[dict]:
    items = []
    for case_file in sorted(CASES_DIR.glob("*.json")):
        data = json.loads(case_file.read_text(encoding="utf-8"))
        steps = data.get("steps", [])
        items.append({
            "case_id": data.get("case_id", case_file.stem),
            "title": data.get("title", ""),
            "map_ref": data.get("map_ref", ""),
            "step_count": len(steps),
            "actions_used": list({s.get("action", "") for s in steps}),
            "auth_strategy": data.get("environment", {}).get("auth_strategy", ""),
        })
    return items


def _find_gaps(maps: list[dict], rules: list[dict], cases: list[dict]) -> dict:
    map_names = {m["name"] for m in maps}
    case_map_refs = {c["map_ref"] for c in cases if c["map_ref"]}
    rule_map_refs = {r["map_ref"] for r in rules if r["map_ref"]}

    return {
        "maps_without_cases": sorted(map_names - case_map_refs - {""}),
        "maps_without_rules": sorted(map_names - rule_map_refs - {""}),
        "cases_without_map": [c["case_id"] for c in cases if not c["map_ref"]],
    }


def main() -> None:
    maps = _scan_maps()
    rules = _scan_rules()
    actions = _scan_actions()
    cases = _scan_cases()
    gaps = _find_gaps(maps, rules, cases)

    report = {
        "maps": {"total": len(maps), "items": maps},
        "rules": {"total": len(rules), "items": rules},
        "actions": {"total": len(actions), "items": actions},
        "cases": {"total": len(cases), "items": cases},
        "coverage_gaps": gaps,
    }

    # JSON output
    json_str = json.dumps(report, ensure_ascii=False, indent=2)
    print(json_str)

    # Human-readable summary
    print("\n" + "=" * 60)
    print(f"Maps:   {len(maps)}")
    print(f"Rules:  {len(rules)}")
    print(f"Actions: {len(actions)}")
    print(f"Cases:  {len(cases)}")
    print("-" * 60)

    for m in maps:
        print(f"  map: {m['name']:35s} regions={m['region_count']} controls={m['control_count']}")

    print("-" * 60)
    for c in cases:
        print(f"  case: {c['case_id']:10s} {c['title'][:40]:40s} map={c['map_ref'] or '(none)'}")

    if gaps["maps_without_cases"]:
        print(f"\n[GAP] Maps without cases: {gaps['maps_without_cases']}")
    if gaps["maps_without_rules"]:
        print(f"[GAP] Maps without rules: {gaps['maps_without_rules']}")
    if gaps["cases_without_map"]:
        print(f"[GAP] Cases without map: {gaps['cases_without_map']}")

    # Write to file
    out_path = FIXTURES_DIR / "coverage_report.json"
    out_path.write_text(json_str, encoding="utf-8")
    print(f"\nReport written to {out_path}")


if __name__ == "__main__":
    main()
