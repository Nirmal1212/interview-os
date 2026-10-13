# Design

## Context

The source is a prompt-only skill (`mock-design-interview/SKILL.md`). It has no code, and its behavior lives entirely in its rules: phases, interviewer behavior, the scorecard rubric, and accuracy rules. The resume optimizer is already a plugin in the `interview-os` marketplace, with its own folder under the repo root. The resume optimizer's reader, `core/docx_io.py`, reads .docx and PDF files and rejects scanned PDFs with a blocking message. See proposal.md for motivation and scope.

Installed plugins are copied into the plugin cache as separate folders. A plugin therefore cannot import code from another plugin's folder at run time.

## Goals / Non-Goals

**Goals:**
- A plugin that installs alongside the resume optimizer from the same marketplace.
- Behavior that matches the spec, enforced by the skill's own rules and checked by a scripted scenario set.
- No stored state: nothing persists between sessions.

**Non-Goals:**
- Automated grading of interview answers. The scorecard is the skill's judgment, guided by the rubric.
- Any ChatGPT or Cursor packaging.
- Generated documents. Output is chat only in this version.

## Decisions

**D1. Plugin folder at the repo root, matching the resume plugin's layout.** `mock-design-interview/` gets `.claude-plugin/plugin.json` and `skills/mock-design-interview/SKILL.md`. The root `marketplace.json` gets a second plugin entry. Alternative: put it under `resume-optimization/`. Rejected because the two are separate products and the marketplace should list them separately.

**D2. The skill is prompt-only; the interview rules live in SKILL.md.** The phases, interviewer behavior, rubric, and accuracy rules are written as instructions for Claude. Alternative: a Python state machine that drives the phases. Rejected because the interview is conversational, and a state machine would make the turns feel scripted, which works against the realism the source skill is built for.

**D3. Share the resume reader by copying it, and test that the copies match.** `docx_io.py` is copied byte-for-byte into `skills/mock-design-interview/core/`. A test compares the two files and fails if they differ. Alternatives considered:
- Import from the resume plugin's folder. Rejected because installed plugins are isolated and the import would fail after install.
- Copy only the read functions. Rejected because a partial copy drifts silently, while a byte-identical copy with a test fails loudly.
- Move the reader into a shared package and have both plugins vendor it at release time. Deferred, because it needs release tooling and there are only two consumers.

**D4. Dependencies match the resume plugin.** python-docx and pypdf are pinned in `core/requirements.txt`. The skill installs them only when an uploaded file needs reading and they are missing.

**D5. Examples in the skill are generic.** The SKILL.md examples use no real company. Company names and job details appear in the conversation only when the user supplies them. This keeps the public plugin from carrying one company's specifics.

**D6. Verification has two parts.** Automated tests cover the copied reader and the manifests. Behavior is checked with a scripted scenario file: each scenario gives the inputs and the behaviors expected from the spec, and the author runs them by hand. A scenario file is the only practical check for prompt behavior, and it makes regressions visible across skill edits.

## Risks / Trade-offs

- **Interviewer drift across long sessions.** The skill may slip out of character or reveal the design late in a long conversation. Mitigation: short turns and the explicit rule against revealing the design, both checked in the scenario file.
- **Technical inaccuracy in probes and the reference design.** A wrong fact would teach the wrong thing. Mitigation: the accuracy requirement, and an instruction to ask the candidate to explain unverifiable tools rather than confirm them.
- **Copy drift in the reader.** Two copies of `docx_io.py` can diverge. Mitigation: the byte-comparison test runs with the other tests.
- **Resume misreading.** Extraction can mangle a resume, and the interviewer could then probe claims the candidate never made. Mitigation: the spec says to reference only stated experience, and the user can paste text instead.
- **Scorecard subjectivity.** The rating is judgment, not measurement. Mitigation: each rating needs one line of evidence from the candidate's own answers.

## Migration Plan

This is a new plugin, so there is nothing to migrate. Rollout:
1. Plugin folder, skill, and reader copy with the byte-comparison test.
2. Marketplace entry and a local install check.
3. Scenario file run by hand before the first release.

Rollback: remove the plugin folder and its marketplace entry. The resume plugin is unaffected because the two share no runtime code.
