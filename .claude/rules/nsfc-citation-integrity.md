---
paths:
  - "proposal/source/**"
---

# NSFC Citation Integrity (No Fake References)

**Rule:** The proposal must not contain fabricated or unverifiable citations.

## Requirements (Strict Mode)

In any “参考文献/主要参考文献目录” section:

- Every non-empty reference entry MUST include at least one identifier:
  - `doi:` (preferred), or
  - `arxiv:` (e.g., `arxiv:2310.01234`), or
  - a stable URL (`https://...`) to a publisher/preprint page.
- “TODO/待补/TBD” placeholders are NOT allowed.

## Draft Mode

Placeholders are allowed only if explicitly marked:
- `TODO: add DOI/arXiv/URL`

But any claim relying on that reference should be hedged until verified.

## Enforcement

- CitationVerifier agent must audit references before export.
- The local orchestrator check must fail export if strict citation rules are violated.

