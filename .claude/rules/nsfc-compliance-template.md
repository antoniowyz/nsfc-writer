---
paths:
  - "proposal/source/**"
---

# NSFC Compliance Guard (Template Alignment)

**This workflow must align the proposal to `nsfc case.pdf`'s section skeleton.**

## Required Sections (Minimum)

1. **中文摘要** (`proposal/source/01_abstract_zh.md`)
2. **英文摘要** (`proposal/source/02_abstract_en.md`)
3. **1. 项目的立项依据**（研究意义、国内外研究现状及发展动态分析、参考文献目录等）
4. **2. 项目的研究内容、研究目标，以及拟解决的关键科学问题**
5. **3. 拟采取的研究方案及可行性分析**（研究方法、技术路线、关键技术、可行性分析等）
6. **4. 本项目的特色与创新之处**
7. **5. 年度研究计划及预期研究结果**（学术交流/预期成果等）
8. **研究基础 / 工作条件 / 项目情况等**（按申请书要求补齐）

## Hard Fail Conditions (Block Export)

- Missing any required section file.
- Section headings do not match the intended section purpose (e.g., “创新”写成了背景综述).
- “参考文献目录”缺失或引用无来源（在 SSOT 中用 bib keys 或明确 TODO）。
- Non-trivial tables/figures referenced but absent in SSOT or not reproducible.

## Style Constraints (Academic + NSFC)

- Avoid marketing tone and exaggerated claims; every “首次/领先/突破” must be evidence-bound.
- Methods must map to questions; questions must map to measurable outcomes and data.
- Keep each section internally structured with numbered subsections where appropriate (1.1/1.2...).

