# QuickCart Data Platform

This repository is **your** semester project for the Data Engineering course.
Every week you add one new part to the same system: the data platform of **QuickCart**,
a (fictional) online grocery-delivery company in Amman.

> **My seed (last 4 digits of my student ID):** ____  
> Use this seed every time you run `tools/generate_day.py`.

## What is in this repository (Week 1)

| Path | What it is | Do I edit it? |
|---|---|---|
| `tools/check_setup.py` | Checks that your computer is ready | No |
| `tools/generate_day.py` | Pretends to be QuickCart's app team and creates the raw data files | No |
| `notebooks/week01_explore.ipynb` | Week 1 lab notebook | **Yes** |
| `docs/data_issues.md` | Your log of problems found in the raw data | **Yes** |
| `data/source_exports/` | Where the generated files appear (not stored in Git) | No |
| `requirements.txt` | Python packages the project needs | Only when told |
| `.gitignore` | Files Git must never store (data, passwords, `.venv`) | No |

## Quick start

**Windows (PowerShell in VS Code)**
```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python tools\check_setup.py
python tools\generate_day.py --seed 1234 --start 2026-10-01 --days 3
```

**macOS (Terminal in VS Code)**
```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python tools/check_setup.py
python tools/generate_day.py --seed 1234 --start 2026-10-01 --days 3
```

Replace `1234` with **your** seed.

## Important rules

- Never commit `.venv/`, `.env` or anything in `data/` — `.gitignore` already prevents this.
- Commit and push at the end of every lab.
- The data is synthetic. Treat it as if it were real personal data anyway.
