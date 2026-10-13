# Design

## Context

The capability is authored from scratch in this repo. There is no external reference implementation to match, so the workflow rules are written here and the scorer is designed against the spec's scenarios. See proposal.md for motivation and the capability list.

Constraints that shape the approach:
- The repo is public-facing, so the core must not depend on private or unlicensed files.
- Resumes are personal data and must not be stored by default (see the data-handling requirement in specs).
- The scoring number is a proxy. It must be reproducible, so the same inputs always give the same score.

## Goals / Non-Goals

**Goals:**
- One portable core (the workflow rules and scoring) that each target wraps without rewriting.
- A deterministic scorer that runs locally with no network calls.
- A Claude skill that can be installed directly, as the first deliverable.

**Non-Goals:**
- Hosting, accounts, or any server-side storage of resumes.
- Parsing every PDF layout. Scanned or image-only PDFs are rejected by the quality gate.
- The ChatGPT and Cursor targets. They are deferred to a follow-up change (see Open Questions).

## Decisions

**D1. Shared core, thin wrappers.** The workflow rules live in one Markdown file (`core/workflow.md`) and the scorer lives in one module (`core/score`). The Claude skill's `SKILL.md` points to the core rather than copying it. Alternative: duplicate the rules per target. Rejected, because the rules are the product and drift would be silent.

**D2. The scorer is a small, documented module written in this repo.** Weighted term matching against the resume text, case-insensitive, with alternates, and a fixed rule for multi-word terms. The scoring formula is weighted matched weight divided by total weight, expressed as a percentage. The spec pins the rule, so the behavior is testable without any outside reference.

**D3. Scorer in Python, standard library only.** It is a pure function from (keywords, text) to (score, matched, missed). Standard library only keeps the scorer's own footprint at zero and makes its tests runnable with `unittest`. Cursor's packaging will call this logic through its Python runtime, so no JavaScript port is needed for the core.

**D4. .docx and PDF handling use python-docx and pypdf, behind one adapter.** Reading and writing goes through a single module (`core/docx_io.py`) so the libraries can change without touching the workflow. Both are declared in `core/requirements.txt`. Their licenses are recorded from package metadata before release (task 7.1).

**D5. Edit in place only for clean .docx input.** Clean .docx files are edited in place to preserve the candidate's formatting. PDFs and ATS-hostile files are rebuilt into a single-column template. This matches the source skill's rule and keeps the minimal-diff requirement.

**D6. Deviation and quality gates run before any scoring.** This avoids spending effort on JDs the candidate cannot truthfully target and surfaces structural problems early. Alternative: score first, then gate. Rejected because a high score on a mismatched resume is misleading.

**D7. The change log is shown on every run.** The author asked for it after the first build, replacing the earlier opt-in commentary. The renderer in `core/changelog.py` produces the fixed template, so every target shows the same table.

**D8. ATS impact is measured sequentially on unrounded scores.** Each edit is applied in order and its impact is the change in the unrounded score it causes. This makes the impacts add up to the total change, within rounding. The cost is that impacts depend on order, so the report states that. Alternative: measure each edit alone against the baseline. Rejected because the impacts would not add up, and the candidate would see numbers that contradict the total.

**D9. The disclaimer goes in the report, not the resume.** The report ends with a disclaimer that the target company's ATS may differ from the keyword-match logic here. It is not in the .docx, because the resume goes to recruiters and a disclaimer there would be read by them.

## Risks / Trade-offs

- **Scorer rule is only as good as its written definition** → Mitigation: the spec pins the rule, and scenarios cover case, alternates, and multi-word terms. Hand-computed fixtures check the implementation against that rule.
- **Keyword matching rewards stuffing** → Mitigation: the truthful-edits requirement and the rule that every added keyword must trace to evidence. The scorer cannot check truthfulness, so the workflow must.
- **Dependency licenses could block redistribution** → Mitigation: D4 isolates the libraries, and task 7.1 records their licenses before any public release.
- **Layout differences across ATS parsers** → Mitigation: target only the conservative single-column template. Claims are limited to a keyword-match proxy, as the requirements state.
- **Personal data in logs or outputs** → Mitigation: no persistence by default; tests use synthetic resumes.

## Migration Plan

This is a new capability, so there is nothing to migrate. Rollout order:
1. Core workflow and scorer, tested against synthetic resumes and JDs.
2. Claude skill packaging and local install test.
3. Public release only after the dependency license check and hand-computed scorer fixtures pass.

Rollback: remove the capability folder. No shared state is touched.

## Open Questions

- **Deferred to a follow-up change:** the ChatGPT form (Custom GPT vs. MCP-based app) and the Cursor packaging (rules vs. plugin). The Cursor editor target is already chosen by the author. Neither question affects the core or the Claude skill, so they are not blocking this change.
