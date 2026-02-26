# NSFCAgent Proposal Workspace (SSOT)

This folder is the **single source of truth** for NSFC proposal writing in this repo.

## SSOT Contract

- Authoritative content lives in `proposal/source/**` (Markdown + YAML).
- Derived exports live in `proposal/output/**` (DOCX/PDF). **Do not hand-edit.**
- Reviews live in `proposal/reviews/**` (JSON per round).
- Claim–evidence binding lives in `proposal/claims/**`.
- Revision trace lives in `proposal/changes/**` (append-only log).

## Required Source Files (minimum skeleton)

- `proposal/source/00_metadata.yaml`
- `proposal/source/01_abstract_zh.md`
- `proposal/source/02_abstract_en.md`
- `proposal/source/03_sec1_lixiangyiju.md`
- `proposal/source/04_sec2_neirong_mubiao_kexuewenti.md`
- `proposal/source/05_sec3_fangan_kexingxing.md`
- `proposal/source/06_sec4_tese_chuangxin.md`
- `proposal/source/07_sec5_plan_expected.md`
- `proposal/source/08_foundation_conditions.md`

## Templates

Use:
- `templates/nsfc/claim-registry.md`
- `templates/nsfc/decision-log.md`

