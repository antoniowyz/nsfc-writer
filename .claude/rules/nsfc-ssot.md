---
paths:
  - "proposal/**"
  - "templates/nsfc/**"
---

# NSFC SSOT (Single Source of Truth) Protocol

**Single source of truth:** `proposal/source/` (Markdown + YAML only).

## Derived Artifacts (DO NOT EDIT)

- `proposal/output/**` (DOCX/PDF exports) are derived. Never hand-edit them.
- `proposal/reviews/**` is reviewer output (JSON). Never edit history; append new rounds.
- `proposal/claims/**` is the claim-evidence registry (generated/maintained by workflow).
- `proposal/changes/**` is the change log (append-only).

## Editing Rules

1. All substantive writing and revisions happen in `proposal/source/**`.
2. Every non-trivial claim that could be challenged by an NSFC reviewer MUST be bound in the claim registry.
   **Mechanism:** tag strong-claim sentences in SSOT with `[[CLAIM:C###]]` and ensure the same `C###` is `BOUND` in `proposal/claims/claim_registry.md`.
3. Claim tags are mandatory for:
   - novelty/significance (“首次/突破/领先/关键意义/重大影响”)
   - causal/policy claims
   - feasibility claims about data access or unique resources
4. The claim registry must include, at minimum:
   - Claim text
   - Location (file + heading)
   - Evidence type: citation / preliminary result / dataset / theory / policy doc
   - Evidence pointer (bib key, file path, table id, or TODO marker)
5. If a claim lacks evidence, it MUST be downgraded (hedged) or marked as TODO before export.

## File Skeleton (Required)

At minimum, maintain these SSOT files:

- `proposal/source/00_metadata.yaml`
- `proposal/source/01_abstract_zh.md`
- `proposal/source/02_abstract_en.md`
- `proposal/source/03_sec1_lixiangyiju.md`
- `proposal/source/04_sec2_neirong_mubiao_kexuewenti.md`
- `proposal/source/05_sec3_fangan_kexingxing.md`
- `proposal/source/06_sec4_tese_chuangxin.md`
- `proposal/source/07_sec5_plan_expected.md`
- `proposal/source/08_foundation_conditions.md`
