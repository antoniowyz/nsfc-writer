from __future__ import annotations

import re
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$")


def _rtf_escape(text: str) -> str:
    """
    RTF unicode escaping.
    - Escape control chars: \\ { }
    - Represent non-ASCII via \\uN?
    """
    out: list[str] = []
    for ch in text:
        code = ord(ch)
        if ch in ["\\", "{", "}"]:
            out.append("\\" + ch)
        elif ch == "\n":
            out.append("\\line ")
        elif 0x20 <= code <= 0x7E:
            out.append(ch)
        else:
            # RTF \uN uses signed 16-bit; Word accepts larger too, but keep in range.
            signed = code if code <= 32767 else code - 65536
            out.append(f"\\u{signed}?")
    return "".join(out)


def _load_md_files(repo_root: Path) -> list[Path]:
    src = repo_root / "proposal" / "source"
    return sorted(p for p in src.glob("*.md"))


def export_rtf(repo_root: Path, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    parts: list[str] = []
    parts.append(r"{\rtf1\ansi\deff0")
    parts.append(r"{\fonttbl{\f0 Calibri;}{\f1 SimSun;}}")
    parts.append(r"\viewkind4\uc1")

    def add_paragraph(text: str, fs: int = 22, bold: bool = False, space_before: int = 120, space_after: int = 120):
        b_on = r"\b" if bold else ""
        b_off = r"\b0" if bold else ""
        parts.append(rf"\pard\sa{space_after}\sb{space_before}\f0\fs{fs} {b_on} {_rtf_escape(text)} {b_off}\par")

    for md_path in _load_md_files(repo_root):
        text = md_path.read_text(encoding="utf-8")
        for raw_line in text.splitlines():
            line = raw_line.rstrip()
            if not line.strip():
                continue

            # Strip claim tags from exported text, but keep content.
            line = re.sub(r"\s*\[\[CLAIM:C\d{3,}\]\]\s*", "", line)

            m = HEADING_RE.match(line)
            if m:
                level = len(m.group(1))
                title = m.group(2).strip()
                if level == 1:
                    add_paragraph(title, fs=32, bold=True, space_before=200, space_after=160)
                elif level == 2:
                    add_paragraph(title, fs=28, bold=True, space_before=180, space_after=140)
                else:
                    add_paragraph(title, fs=24, bold=True, space_before=160, space_after=120)
                continue

            if line.lstrip().startswith(("-", "*")):
                bullet_text = "• " + line.lstrip()[1:].strip()
                add_paragraph(bullet_text, fs=22, bold=False, space_before=80, space_after=80)
                continue

            add_paragraph(line)

    parts.append("}")
    out_path.write_text("".join(parts), encoding="utf-8")


__all__ = ["export_rtf"]

