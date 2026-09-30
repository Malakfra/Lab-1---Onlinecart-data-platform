"""
QuickCart setup checker  (PROVIDED BY COURSE STAFF)
==================================================

Run it from the project folder, with your virtual environment activated:

    python tools/check_setup.py

It checks that everything needed for the current week is installed and tells you
exactly what to fix. It changes nothing on your computer.

    [ OK ]  everything is fine
    [WARN]  not needed yet, or not critical - read the message
    [FAIL]  must be fixed before the lab
"""

import importlib            # lets us try to import a package by its name
import shutil               # finds programs such as git and docker
import subprocess           # runs a program (e.g. "git --version") and reads its answer
import sys                  # information about the Python that is running this script
import urllib.request       # a simple web request (to test the internet connection)
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
failures = 0


def report(status, message, fix=""):
    """Print one line of the report and remember failures."""
    global failures
    if status == "FAIL":
        failures += 1
    print(f"[{status:^4}] {message}")
    if fix:
        print(f"         -> {fix}")


def run(command):
    """Run a command and return its output as text ('' if it fails)."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
        return result.stdout.strip()
    except Exception:
        return ""


print("=" * 70)
print("QuickCart setup check")
print("=" * 70)

# 1. Python version ----------------------------------------------------------------------------
version = sys.version_info
if version >= (3, 12):
    report("OK", f"Python {version.major}.{version.minor}.{version.micro}")
elif version >= (3, 10):
    report("WARN", f"Python {version.major}.{version.minor} works, but the course uses 3.13",
           "Install Python 3.13 when convenient.")
else:
    report("FAIL", f"Python {version.major}.{version.minor} is too old",
           "Install Python 3.13 from python.org.")

# 2. Virtual environment -----------------------------------------------------------------------
if sys.prefix != sys.base_prefix:
    report("OK", f"Virtual environment is active ({Path(sys.prefix).name})")
else:
    report("FAIL", "No virtual environment is active",
           "Windows: .venv\\Scripts\\Activate.ps1    macOS: source .venv/bin/activate")

# 3. Python packages for this week -------------------------------------------------------------
for package in ["pandas", "ipykernel"]:
    try:
        module = importlib.import_module(package)
        report("OK", f"Package '{package}' {getattr(module, '__version__', '')}")
    except ImportError:
        report("FAIL", f"Package '{package}' is not installed",
               "pip install -r requirements.txt")

# 4. Git ----------------------------------------------------------------------------------------
if shutil.which("git"):
    report("OK", run(["git", "--version"]))
    name = run(["git", "config", "--global", "user.name"])
    email = run(["git", "config", "--global", "user.email"])
    if name and email:
        report("OK", f"Git identity: {name} <{email}>")
    else:
        report("FAIL", "Git does not know your name/e-mail yet",
               'git config --global user.name "Your Name"  and  '
               'git config --global user.email "you@example.com"')
else:
    report("FAIL", "Git is not installed", "Install Git from https://git-scm.com/downloads")

# 5. Docker (needed from Week 3) ----------------------------------------------------------------
if shutil.which("docker"):
    answer = run(["docker", "--version"])
    report("OK", answer or "Docker is installed")
else:
    report("WARN", "Docker is not installed (needed from Week 3)",
           "Install Docker Desktop: https://www.docker.com/products/docker-desktop/")

# 6. VS Code command line (optional) ------------------------------------------------------------
if shutil.which("code"):
    report("OK", "VS Code 'code' command is available")
else:
    report("WARN", "The 'code' command was not found (optional)",
           "Not a problem if you open VS Code from the Start menu / Applications.")

# 7. Project folder is writable ----------------------------------------------------------------
try:
    test_file = PROJECT_ROOT / "data" / "source_exports" / ".write_test"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("ok")
    test_file.unlink()
    report("OK", f"Project folder is writable ({PROJECT_ROOT.name})")
except Exception as error:
    report("FAIL", f"Cannot write in the project folder: {error}",
           "Move the project to a folder you own, e.g. Documents.")

# 8. Internet access to the weather API (needed in Week 2) -------------------------------------
try:
    urllib.request.urlopen("https://api.open-meteo.com/v1/forecast?latitude=31.95&longitude=35.93"
                           "&current=temperature_2m", timeout=8)
    report("OK", "Weather API (api.open-meteo.com) is reachable")
except Exception:
    report("WARN", "Weather API not reachable right now (needed in Week 2)",
           "Check your internet connection; the course provides offline copies if needed.")

print("=" * 70)
if failures == 0:
    print("RESULT: READY - all required checks passed.")
else:
    print(f"RESULT: NOT READY - fix the {failures} [FAIL] item(s) above, then run this again.")
print("=" * 70)
sys.exit(1 if failures else 0)
