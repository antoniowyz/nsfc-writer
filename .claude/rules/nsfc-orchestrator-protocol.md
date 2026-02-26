---
paths:
  - "proposal/**"
  - "templates/nsfc/**"
---

# NSFC Orchestrator Protocol (LangGraph-style State Machine, S-tier)

**Coordination model:** 8 specialist agents + 1 orchestrator. SSOT is `proposal/source/**`.

## State Machine (Conceptual)

```
INTAKE -> PLAN (user approves)
      -> RESEARCH (Searcher)
      -> OUTLINE (Writer + 1-round panel inputs)
      -> DRAFT (Writer)
      -> VERIFY (ComplianceGuard + EvidenceAuditor + ConsistencyChecker)
      -> CRITIC_PANEL (Reviewer + auditors)  [Round 1]
      -> TRIAGE (Writer resolves conflicts)
      -> FIX (Designer applies issues to SSOT)
      -> HUMANIZE (Humanizer full coverage)
      -> REVERIFY (same checks)
      -> SCORE/GATE
          PASS -> EXPORT (derived docx) -> FINAL_VERIFY -> DONE
          FAIL -> CRITIC_PANEL (Round 2 max) -> ... -> DONE WITH BLOCKERS
```

## Adversarial QA (Panel Critic)

**Read-only critics (must not edit files):**
- Reviewer (scientific critic)
- EvidenceAuditor
- ConsistencyChecker
- ComplianceGuard
- CitationVerifier

**Fixers (edit SSOT only):**
- Designer (primary fixer)
- Writer (only for high-level decisions and final integration)

## Issue Schema (must be structured)

Each critic outputs issues using this minimum schema (saved to `proposal/reviews/round_XX_issues.json`):

- `issue_id` (stable)
- `severity` (`critical|major|minor`)
- `section` (e.g., `sec3_fangan_kexingxing`)
- `location` (file + heading)
- `problem` (1–3 sentences)
- `why_it_matters` (NSFC reviewer lens)
- `proposed_fix` (actionable)
- `requires_user_decision` (bool)

## Hard Gates (must pass before export)

- Compliance template satisfied (all required sections present)
- Claim registry exists and binds all strong claims
- Consistency checks pass for core definitions/numbers
- Humanizer gate passes (no obvious AI-pattern writing)
- Citation integrity passes (no fake/unverifiable references)

## Loop Limits (S-tier)

- Max QA rounds: **2**
- If blockers remain after Round 2: stop, list blockers + request user decisions.
