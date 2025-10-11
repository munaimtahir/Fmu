
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SETTINGS = REPO_ROOT / "backend" / "sims_backend" / "sims_backend" / "settings.py"

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
    ]
}

def read_text(p: Path):
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""

def find_missing_inits():
    missing = []
    for app in PROBES["apps"]:
        p = REPO_ROOT / "backend" / "sims_backend" / app / "__init__.py"
        if not p.exists():
            missing.append(str(p.relative_to(REPO_ROOT)))
    return missing

def parse_settings():
    txt = read_text(SETTINGS)
    m = re.search(r"INSTALLED_APPS\\s*=\\s*\\[(.*?)\\]", txt, flags=re.S)
    raw = m.group(1) if m else ""
    entries = re.findall(r"[\\\"']([^\\\"']+)[\\\"']", raw)
    return {"raw": raw, "entries": entries, "text": txt}

def check_installed_apps(installed):
    problems = []
    for app in PROBES["apps"]:
        module_path = f"sims_backend.{app}"
        if module_path not in installed["entries"]:
            problems.append(f"Missing in INSTALLED_APPS: {module_path}")
    return problems

def scan_apps_py():
    problems = []
    for app in PROBES["apps"]:
        p = REPO_ROOT / "backend" / "sims_backend" / app / "apps.py"
        txt = read_text(p)
        if not txt:
            problems.append(f"{p}: missing apps.py")
            continue
        normalized = txt.replace("'", '"')
        if f'name = "sims_backend.{app}"' not in normalized:
            problems.append(f"{p}: expected name = 'sims_backend.{app}'")
        if f'label = "{app}"' not in normalized:
            problems.append(f"{p}: expected label = '{app}'")
    return problems

def scan_models_for_direct_imports():
    problems = []
    direct_import_re = re.compile(r"from\\s+sims_backend\\.[a-z_]+\\.models\\s+import\\s+([A-Za-z_,\\s]+)")
    fk_re = re.compile(r"models\\.ForeignKey\\(([^,]+),")
    for app in PROBES["apps"]:
        p = REPO_ROOT / "backend" / "sims_backend" / app / "models.py"
        txt = read_text(p)
        if not txt:
            continue
        for m in direct_import_re.finditer(txt):
            problems.append(f"{p}: direct cross-app import -> {m.group(0)} (use lazy string e.g. 'admissions.Student')")
        for m in fk_re.finditer(txt):
            target = m.group(1).strip().strip('"').strip("'")
            if target.startswith("sims_backend."):
                problems.append(f"{p}: ForeignKey target '{target}' should use app label, e.g., 'admissions.ModelName'")
    return problems

def scan_migrations_dependencies():
    problems = []
    for app in PROBES["apps"]:
        mig_dir = REPO_ROOT / "backend" / "sims_backend" / app / "migrations"
        if not mig_dir.exists():
            problems.append(f"{mig_dir}: missing migrations directory")
            continue
        for mig in sorted(mig_dir.glob("0*_*.py")):
            txt = read_text(mig)
            bad = re.findall(r'\\("sims_backend\\.[^"]+",\\s*"[0-9]+"\)', txt)
            if bad:
                problems.append(f"{mig}: dependencies should use labels not module paths -> {bad}")
    return problems

def main():
    print("== Django app_label diagnostics ==")
    missing_inits = find_missing_inits()
    installed = parse_settings()
    problems = []
    problems += check_installed_apps(installed)
    problems += scan_apps_py()
    problems += scan_models_for_direct_imports()
    problems += scan_migrations_dependencies()

    if missing_inits:
        print("\\n[Missing __init__.py]")
        for m in missing_inits:
            print(" -", m)
    print("\\n[INSTALLED_APPS entries]")
    for e in installed["entries"]:
        print(" *", e)

    if problems:
        print("\\n[PROBLEMS FOUND]")
        for p in problems:
            print(" -", p)
        print("\\nFAIL: Fix the above lines and re-run.")
        sys.exit(1)
    else:
        print("\\nPASS: Static checks look good. Next we try runtime registry.")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_backend.settings")
    import django
    django.setup()
    from django.apps import apps

    labels = sorted((c.label, c.name) for c in apps.get_app_configs() if c.name.startswith("sims_backend"))
    print("\\n[Runtime app registry]")
    for label, name in labels:
        print(f" - {label:12s} -> {name}")

    for label, model in [("admissions","Student"),("academics","Program"),("academics","Course"),("academics","Section"),("enrollment","Enrollment")]:
        try:
            m = apps.get_model(label, model)
            print(f" get_model({label}, {model}) -> OK: {m}")
        except Exception as e:
            print(f" get_model({label}, {model}) -> ERROR: {e}")
            sys.exit(2)

    print("\\nSUCCESS: app_label wiring validated.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
