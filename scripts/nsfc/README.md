# NSFCAgent Scripts

These scripts make the NSFC workflow **robust and repeatable**:

- `orchestrate.py` — resumable state machine runner (no LLM dependency)
- `checks.py` — compliance / claim-binding / humanizer heuristics
- `export_docx.py` — export SSOT (`proposal/source/**`) to `proposal/output/*.docx`

## Quick Commands

```powershell
python scripts/nsfc/orchestrate.py init
python scripts/nsfc/orchestrate.py check
python scripts/nsfc/orchestrate.py export-docx
```

## Dependency Note (DOCX)

DOCX export uses `python-docx`. If missing:

```powershell
python -m pip install python-docx
```

