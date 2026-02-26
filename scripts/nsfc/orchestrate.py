#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
# Allow running as a script: `python scripts/nsfc/orchestrate.py ...`
sys.path.insert(0, str(REPO_ROOT))

from scripts.nsfc.checks import CheckResult, run_all_checks  # noqa: E402
from scripts.nsfc.export_docx import export_docx  # noqa: E402
from scripts.nsfc.export_rtf import export_rtf  # noqa: E402
PROPOSAL_DIR = REPO_ROOT / "proposal"
STATE_DIR = PROPOSAL_DIR / "run"
STATE_PATH = STATE_DIR / "state.json"


@dataclass(frozen=True)
class OrchestratorState:
    phase: str
    round: int
    updated_at: str

    @staticmethod
    def default() -> "OrchestratorState":
        return OrchestratorState(
            phase="DRAFT",
            round=1,
            updated_at=datetime.now().isoformat(timespec="seconds"),
        )


def _load_state() -> OrchestratorState:
    if not STATE_PATH.exists():
        return OrchestratorState.default()
    data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return OrchestratorState(
        phase=str(data.get("phase", "DRAFT")),
        round=int(data.get("round", 1)),
        updated_at=str(data.get("updated_at", "")),
    )


def _save_state(state: OrchestratorState) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(
        json.dumps(
            {"phase": state.phase, "round": state.round, "updated_at": state.updated_at},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def cmd_init() -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if not (PROPOSAL_DIR / "README.md").exists():
        print("ERROR: proposal/ workspace not found. Run from repo root.", file=sys.stderr)
        return 2
    state = OrchestratorState.default()
    _save_state(state)
    print(f"Initialized state at {STATE_PATH} (phase={state.phase}, round={state.round}).")
    return 0


def _print_check_summary(results: list[CheckResult]) -> None:
    ok = [r for r in results if r.passed]
    bad = [r for r in results if not r.passed]
    print(f"Checks: {len(ok)} passed, {len(bad)} failed.")
    for r in bad:
        print(f"- FAIL [{r.check_id}] {r.message}")
        for d in r.details[:20]:
            print(f"  - {d}")


def cmd_check(fail_fast: bool, mode: str) -> int:
    results = run_all_checks(repo_root=REPO_ROOT, fail_fast=fail_fast, mode=mode)
    _print_check_summary(results)
    return 0 if all(r.passed for r in results) else 1


def cmd_export_docx(output: str | None, template: str | None, mode: str) -> int:
    # Gate: always run checks before export.
    results = run_all_checks(repo_root=REPO_ROOT, fail_fast=True, mode=mode)
    if not all(r.passed for r in results):
        _print_check_summary(results)
        print(f"Blocked ({mode}): checks failed; refusing to export DOCX.", file=sys.stderr)
        return 1

    out_path = Path(output) if output else (PROPOSAL_DIR / "output" / "NSFC_proposal.docx")
    template_path = Path(template) if template else None
    try:
        export_docx(repo_root=REPO_ROOT, out_path=out_path, template_path=template_path)
        print(f"Exported DOCX: {out_path}")
    except SystemExit as e:
        # Fallback: generate RTF (Word-readable) when python-docx isn't available.
        if out_path.suffix.lower() in {".doc", ".rtf"}:
            export_rtf(repo_root=REPO_ROOT, out_path=out_path)
            print(f"Exported RTF (Word-readable): {out_path}")
        else:
            raise e
    return 0


def cmd_advance_phase(phase: str | None) -> int:
    state = _load_state()
    new_phase = (phase or "").strip().upper()
    if not new_phase:
        print("ERROR: phase required.", file=sys.stderr)
        return 2
    _save_state(
        OrchestratorState(
            phase=new_phase,
            round=state.round,
            updated_at=datetime.now().isoformat(timespec="seconds"),
        )
    )
    print(f"Phase updated: {state.phase} -> {new_phase}")
    return 0


def cmd_next_round() -> int:
    state = _load_state()
    if state.round >= 2:
        print("S-tier limit reached: max QA rounds is 2.", file=sys.stderr)
        return 2
    _save_state(
        OrchestratorState(
            phase=state.phase,
            round=state.round + 1,
            updated_at=datetime.now().isoformat(timespec="seconds"),
        )
    )
    print(f"Advanced to QA round {state.round + 1}.")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="nsfc-orchestrate")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init")

    p_check = sub.add_parser("check")
    p_check.add_argument("--fail-fast", action="store_true")
    p_check.add_argument("--mode", choices=["draft", "strict"], default="strict")

    p_export = sub.add_parser("export-docx")
    p_export.add_argument("--output", default=None)
    p_export.add_argument("--template", default=None)
    p_export.add_argument("--mode", choices=["draft", "strict"], default="strict")

    p_phase = sub.add_parser("set-phase")
    p_phase.add_argument("phase")

    sub.add_parser("next-round")

    args = parser.parse_args(argv)

    if args.cmd == "init":
        return cmd_init()
    if args.cmd == "check":
        return cmd_check(fail_fast=bool(args.fail_fast), mode=str(args.mode))
    if args.cmd == "export-docx":
        return cmd_export_docx(output=args.output, template=args.template, mode=str(args.mode))
    if args.cmd == "set-phase":
        return cmd_advance_phase(phase=args.phase)
    if args.cmd == "next-round":
        return cmd_next_round()

    print(f"Unknown command: {args.cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
