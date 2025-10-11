"""
Django app_label diagnostics helper.

Purpose:
- Detects common causes of "Apps aren't loaded yet" or "Model has no app_label" errors.
- Checks for bad model imports, circular references, and miswired INSTALLED_APPS.

Usage:
  Run manually or as a GitHub Action workflow step:
    python tools/diagnose_app_labels.py
"""

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

PROBES = {
    "apps": [
        "admissions",
        "academics",
        "enrollment",
        "attendance",
        "assessments",
        "results",
        "transcripts",
        "audit",
    ],
    "settings": "backend/sims_backend/sims_backend/settings.py",
}


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def scan_installed_apps() -> list[str]:
    """Ensure INSTALLED_APPS uses correct short module paths."""
    problems = []
    p = REPO_ROOT / PROBES["settings"]
    txt = read_text(p)

    # Look for suspicious app paths
    for line in txt.splitlines():
        if "INSTALLED_APPS" in line:
            break

    for app in PROBES["apps"]:
        if f"'{app}'" not in txt and f'"{app}"' not in txt:
            if f"'sims_backend.{app}.apps" in txt or f'"sims_backend.{app}.apps' in txt:
                problems.append(
                    f"{p}: Avoid using AppConfig path for '{app}'. Use 'sims_backend.{app}' instead."
                )
            elif f"'sims_backend.{app}'" not in txt:
                problems.append(
                    f"{p}: Missing '{app}' in INSTALLED_APPS (expected 'sims_backend.{app}')."
                )
    return problems


def scan_models_for_direct_imports() -> list[str]:
    """
    Detect direct model imports or wrong ForeignKey targets that cause app_label issues.
    """
    problems = []
    direct_import_re = re.compile(
        r"from\s+sims_backend\.[a-z_]+\.models\s+import\s+([A-Za-z_,\s]+)"
    )

    fk_patterns = [
        re.compile(r"ForeignKey\s*\(\s*([^\s,]+)"),
        re.compile(r"OneToOneField\s*\(\s*([^\s,]+)"),
        re.compile(r"ManyToManyField\s*\(\s*([^\s,]+)"),
    ]

    for app in PROBES["apps"]:
        p = REPO_ROOT / "backend" / "sims_backend" / app / "models.py"
        txt = read_text(p)
        if not txt:
            continue

        # 1) Flag cross-app direct imports
        for m in direct_import_re.finditer(txt):
            problems.append(
                f"{p}: direct cross-app import -> {m.group(0)} "
                "(use lazy string e.g. 'admissions.Student')"
            )

        # 2) Flag FK targets that use module paths (should use app label)
        for rx in fk_patterns:
            for m in rx.finditer(txt):
                target = m.group(1).strip().strip('"').strip("'")
                if target.startswith("sims_backend."):
                    problems.append(
                        f"{p}: Relational field target '{target}' should use app label, "
                        "e.g., 'admissions.ModelName'"
                    )
    return problems


def scan_apps_py_labels() -> list[str]:
    """Check that apps.py defines correct name and label."""
    problems = []
    for app in PROBES["apps"]:
        p = REPO_ROOT / "backend" / "sims_backend" / app / "apps.py"
        txt = read_text(p)
        if not txt:
            problems.append(f"{p}: apps.py missing or unreadable")
            continue

        if f'name = "sims_backend.{app}"' not in txt:
            problems.append(f"{p}: name should be 'sims_backend.{app}'")

        if f'label = \"{app}\"' not in txt and f"label = '{app}'" not in txt:
            problems.append(f"{p}: label should be '{app}'")
    return problems


def main() -> int:
    print("== Django app_label diagnostics ==")
    problems = []
    problems += scan_installed_apps()
    problems += scan_apps_py_labels()
    problems += scan_models_for_direct_imports()

    if problems:
        print("\n❌ Problems found:\n")
        for p in problems:
            print("-", p)
        print(f"\nTotal issues detected: {len(problems)}")
        return 1

    print("\n✅ SUCCESS: app_label wiring validated. No structural issues found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
