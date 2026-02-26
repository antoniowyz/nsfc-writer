---
paths:
  - "proposal/source/**"
---

# NSFC Humanizer Gate (zh-CN + EN, Full Coverage)

**Goal:** Remove AI-writing patterns while preserving academic rigor and falsifiability.

## Non-Negotiables

- Humanizer edits MUST NOT change scientific claims, identification strategy, or quantitative statements.
- Humanizer edits MUST NOT add new contributions not supported elsewhere.
- If a sentence asserts novelty/significance, it must either:
  1) be evidence-bound in the claim registry, or
  2) be rewritten into a precise, testable, non-exaggerated statement.

## What To Remove (Typical AI Patterns)

- 空泛拔高：意义宏大但不指向可检验贡献（“具有重要意义/里程碑/深刻影响/关键转折点”）
- 模糊归因：没有来源的“已有研究表明/学者认为/普遍认为”
- 模板化段落：挑战-机遇-展望式套话
- 词汇“AI 腔”：过度使用“此外/同时/进一步/赋能/生态/维度/框架/范式”等堆叠
- 英文摘要常见问题：过度形容词、copula avoidance、过长句、重复同义替换

## Gate Criteria (Block Export If Failed)

- Any section contains repeated puffery without concrete mechanisms, data, or tests.
- Any paragraph contains ≥2 unbound strong claims (novelty, causal impact, policy implication).
- English abstract reads like “press release” (too many adjectives, not enough specifics).

## Output Contract

When running the Humanizer agent:
- Provide a short change summary per file (what tone issues were fixed).
- Preserve section structure and numbering.
- For any hedged rewrite, keep meaning but make uncertainty explicit.

