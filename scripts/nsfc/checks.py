from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    passed: bool
    message: str
    details: list[str]


REQUIRED_SOURCE_FILES = [
    "proposal/source/00_metadata.yaml",
    "proposal/source/01_abstract_zh.md",
    "proposal/source/02_abstract_en.md",
    "proposal/source/03_sec1_lixiangyiju.md",
    "proposal/source/04_sec2_neirong_mubiao_kexuewenti.md",
    "proposal/source/05_sec3_fangan_kexingxing.md",
    "proposal/source/06_sec4_tese_chuangxin.md",
    "proposal/source/07_sec5_plan_expected.md",
    "proposal/source/08_foundation_conditions.md",
]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required_files(repo_root: Path) -> CheckResult:
    missing: list[str] = []
    for rel in REQUIRED_SOURCE_FILES:
        if not (repo_root / rel).exists():
            missing.append(rel)
    if missing:
        return CheckResult(
            check_id="required_files",
            passed=False,
            message="Missing required SSOT files.",
            details=missing,
        )
    return CheckResult("required_files", True, "All required SSOT files exist.", [])


CLAIM_TAG_RE = re.compile(r"\[\[CLAIM:(C\d{3,})\]\]")


def _parse_claim_registry(registry_text: str) -> dict[str, dict[str, str]]:
    """
    Very small markdown-table parser.
    Expects rows like:
    | C001 | ... | ... | ... | ... | ... | BOUND | ... |
    """
    lines = [ln.strip() for ln in registry_text.splitlines()]
    rows = [ln for ln in lines if ln.startswith("|") and ln.endswith("|")]
    claims: dict[str, dict[str, str]] = {}
    for r in rows:
        cols = [c.strip() for c in r.strip("|").split("|")]
        if not cols:
            continue
        if cols[0].upper() in {"CLAIM ID", "---"}:
            continue
        claim_id = cols[0]
        if not re.fullmatch(r"C\d{3,}", claim_id):
            continue
        status = cols[6] if len(cols) >= 7 else ""
        claims[claim_id] = {"status": status}
    return claims


def check_claim_tags_bound(repo_root: Path) -> CheckResult:
    src_dir = repo_root / "proposal" / "source"
    registry_path = repo_root / "proposal" / "claims" / "claim_registry.md"
    if not registry_path.exists():
        return CheckResult(
            "claim_registry_exists",
            False,
            "Claim registry missing: proposal/claims/claim_registry.md",
            [],
        )

    registry = _parse_claim_registry(_read_text(registry_path))
    found_tags: dict[str, list[str]] = {}
    for md in sorted(src_dir.glob("*.md")):
        text = _read_text(md)
        for m in CLAIM_TAG_RE.finditer(text):
            found_tags.setdefault(m.group(1), []).append(str(md.relative_to(repo_root)))

    if not found_tags:
        return CheckResult(
            "claim_tags_present",
            False,
            "No [[CLAIM:C###]] tags found in proposal/source/*.md. Add tags to strong claims.",
            ["Example: 这将显著提高… [[CLAIM:C001]]"],
        )

    unbound: list[str] = []
    for cid, locations in found_tags.items():
        status = registry.get(cid, {}).get("status", "").upper()
        if status != "BOUND":
            unbound.append(f"{cid} (status={status or 'MISSING'}) in {', '.join(locations)}")

    if unbound:
        return CheckResult(
            "claim_tags_bound",
            False,
            "Some claim tags are not BOUND in claim registry.",
            unbound,
        )
    return CheckResult("claim_tags_bound", True, "All claim tags are BOUND.", [])


CN_AI_WORDS = [
    "赋能",
    "生态",
    "范式",
    "维度",
    "框架",
    "进一步",
    "此外",
    "同时",
    "从而",
    "具有重要意义",
    "里程碑",
    "开创性",
    "重大突破",
]

EN_AI_WORDS = [
    "additionally",
    "crucial",
    "pivotal",
    "underscores",
    "showcase",
    "delve",
    "landscape",
    "testament",
]


def check_humanizer_heuristics(repo_root: Path) -> CheckResult:
    src_dir = repo_root / "proposal" / "source"
    hits: list[str] = []
    for md in sorted(src_dir.glob("*.md")):
        text = _read_text(md)
        lower = text.lower()
        cn_count = sum(text.count(w) for w in CN_AI_WORDS)
        en_count = sum(lower.count(w) for w in EN_AI_WORDS)
        if cn_count + en_count >= 12:
            hits.append(f"{md.name}: ai-word hits={cn_count + en_count} (cn={cn_count}, en={en_count})")

    if hits:
        return CheckResult(
            "humanizer_heuristics",
            False,
            "High density of common AI-pattern words; run nsfc-humanizer and tighten language.",
            hits,
        )
    return CheckResult("humanizer_heuristics", True, "Humanizer heuristic density OK.", [])


REF_HEADING_RE = re.compile(r"^#{1,3}\s+.*(参考文献|主要参考文献目录).*$")
IDENTIFIER_RE = re.compile(r"(doi:\s*\S+|arxiv:\s*\S+|https?://\S+)", re.IGNORECASE)
TODO_RE = re.compile(r"\b(TODO|TBD|待补|占位)\b", re.IGNORECASE)


def _extract_reference_blocks(md_text: str) -> list[list[str]]:
    """
    Extract reference blocks under headings containing 参考文献/主要参考文献目录.
    A block ends at the next heading line.
    """
    lines = md_text.splitlines()
    blocks: list[list[str]] = []
    i = 0
    while i < len(lines):
        if REF_HEADING_RE.match(lines[i].strip()):
            i += 1
            block: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("#"):
                if lines[i].strip():
                    block.append(lines[i].strip())
                i += 1
            blocks.append(block)
            continue
        i += 1
    return blocks


def check_reference_identifiers(repo_root: Path, mode: str) -> CheckResult:
    src_dir = repo_root / "proposal" / "source"
    offenders: list[str] = []
    for md in sorted(src_dir.glob("*.md")):
        text = _read_text(md)
        for block in _extract_reference_blocks(text):
            for entry in block:
                # allow markdown bullets and numbering
                normalized = entry.lstrip("-* ").strip()
                if not normalized:
                    continue
                has_id = bool(IDENTIFIER_RE.search(normalized))
                has_todo = bool(TODO_RE.search(normalized))
                if mode == "draft":
                    # Draft: allow TODO, but still flag totally untraceable entries as major.
                    if (not has_id) and (not has_todo):
                        offenders.append(f"{md.name}: {normalized}")
                else:
                    # Strict: must have identifier and no TODO placeholders.
                    if (not has_id) or has_todo:
                        offenders.append(f"{md.name}: {normalized}")

    if offenders:
        msg = (
            "Reference entries missing identifiers (require doi:/arxiv:/https://)."
            if mode == "strict"
            else "Draft references should include doi:/arxiv:/https:// or explicit TODO marker."
        )
        return CheckResult("citation_integrity", False, msg, offenders[:50])
    return CheckResult("citation_integrity", True, "Citation integrity check OK.", [])


def run_all_checks(repo_root: Path, fail_fast: bool, mode: str = "strict") -> list[CheckResult]:
    if mode not in {"draft", "strict"}:
        raise ValueError(f"Unknown mode: {mode}")

    checks = [check_required_files, check_humanizer_heuristics]
    if mode == "strict":
        checks.insert(1, check_claim_tags_bound)

    # Citation integrity is always checked (draft is lenient; strict is blocking).
    checks.append(lambda rr: check_reference_identifiers(rr, mode=mode))

    results: list[CheckResult] = []
    for fn in checks:
        r = fn(repo_root)
        results.append(r)
        if fail_fast and not r.passed:
            break
    return results


__all__ = ["CheckResult", "run_all_checks"]
