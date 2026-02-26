# NSFCAgent Workflow Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a new NSFCAgent writing workflow to this repo, based on the existing plan-first/memory/SSOT/multi-agent/adversarial QA/orchestrator design, using Markdown+YAML as SSOT and aligning outputs to `nsfc case.pdf`.

**Architecture:** Extend `.claude/` with NSFC-specific rules + agents. Create a `proposal/` SSOT tree (`proposal/source/` is authoritative; `proposal/output/` is derived). Add a panel-critic adversarial loop with hard gates (compliance/evidence/consistency/humanizer) and a two-round cap (S-tier).

**Tech Stack:** Claude Code rules/agents/hooks; Markdown+YAML SSOT; optional future LangGraph Python orchestrator (spec-only in rules for now).

---

### Task 1: Add NSFC SSOT structure

**Files:**
- Create: `proposal/README.md`
- Create: `proposal/source/.gitkeep`
- Create: `proposal/output/.gitkeep`
- Create: `proposal/reviews/.gitkeep`
- Create: `proposal/claims/.gitkeep`
- Create: `proposal/changes/.gitkeep`

**Step 1:** Create folders and stub files (SSOT contract + usage).
**Step 2:** Ensure SSOT rules reference these paths.

---

### Task 2: Add NSFC rules (path-scoped)

**Files:**
- Create: `.claude/rules/nsfc-ssot.md`
- Create: `.claude/rules/nsfc-orchestrator-protocol.md`
- Create: `.claude/rules/nsfc-quality-gates.md`
- Create: `.claude/rules/nsfc-compliance-template.md`
- Create: `.claude/rules/nsfc-humanizer-gate.md`

**Step 1:** Encode SSOT, required section skeleton, gates, and the S-tier 2-round adversarial loop.
**Step 2:** Define “hard fail” conditions (missing sections, unbound critical claims, inconsistent core numbers, humanizer violations).

---

### Task 3: Add NSFC agents (specialists)

**Files:**
- Create: `.claude/agents/nsfc-writer.md`
- Create: `.claude/agents/nsfc-searcher.md`
- Create: `.claude/agents/nsfc-designer.md`
- Create: `.claude/agents/nsfc-reviewer.md`
- Create: `.claude/agents/nsfc-evidence-auditor.md`
- Create: `.claude/agents/nsfc-consistency-checker.md`
- Create: `.claude/agents/nsfc-compliance-guard.md`
- Create: `.claude/agents/nsfc-humanizer.md`

**Step 1:** Make reviewer/auditors read-only by instruction; fixer/writer write SSOT only.
**Step 2:** Standardize output schemas for issues (JSON fields) and verdicts.

---

### Task 4: Add NSFC templates

**Files:**
- Create: `templates/nsfc/claim-registry.md`
- Create: `templates/nsfc/review-issues.schema.json`
- Create: `templates/nsfc/decision-log.md`

**Step 1:** Provide formats for Claim–Evidence binding, issue tracking, and decisions.

---

### Task 5: Update quick references

**Files:**
- Modify: `.claude/WORKFLOW_QUICK_REF.md`
- Modify: `CLAUDE.md`

**Step 1:** Add NSFC workflow entry points, SSOT reminder, and hard gates.
**Step 2:** Keep `CLAUDE.md` short and point to the NSFC rules.

---

### Task 6: Verification (lightweight)

**Files:**
- None (commands only)

**Step 1:** Run: `rg -n "nsfc-" .claude/rules .claude/agents templates proposal`
Expected: Files present and discoverable.
**Step 2:** Run: `git status`
Expected: New files show up; no accidental edits to protected files.

