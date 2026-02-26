---
paths:
  - "proposal/**"
---

# NSFC Quality Gates (S-tier)

**Thresholds:**
- **>= 80/100** = safe draft export
- **>= 90/100** = submission-ready (aspirational)

## Rubric (0–100)

### Critical (block export)
- Missing required section (auto-fail)
- Logical mismatch: research questions not answered by methods (auto-fail)
- Evidence failure: key novelty/causal/policy claim unbound (auto-fail)
- Inconsistency: core numbers/definitions contradict across sections (auto-fail)

### Major (deductions)
- Weak innovation articulation (−10)
- Vague mechanism without test plan (−8)
- Technical route not operational (inputs/outputs/timelines missing) (−8)
- Literature review lacks positioning vs top-5 closest works (−6)
- English abstract vague or promotional (−6)
- Overlong/opaque paragraphs harming readability (−4)

### Minor (deductions)
- Repetitive “AI vocabulary” /套话 (−1 to −3 per section)
- Formatting drift (headings, numbering) (−1 to −3)

## Required Artifacts (for traceability)

- `proposal/claims/claim_registry.*` exists and covers key claims
- `proposal/reviews/round_*.json` exists for each QA round
- `proposal/changes/change_log.md` updated for each applied issue

