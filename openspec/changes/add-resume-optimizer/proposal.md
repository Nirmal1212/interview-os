# Proposal

## Why

Engineers preparing for interviews repeatedly tailor the same resume to different job descriptions by hand, and most public tools either rewrite too much (inventing experience) or score keywords without producing an edited document. interview-os needs a resume optimizer that starts from one maintained master resume, targets one JD at a time, and makes only edits the candidate's real experience supports. The capability is authored from scratch in this repo.

## What Changes

- Add a resume optimization capability that takes a **master resume** (.docx or .pdf) and a **job description** (full text preferred, or a role title) and produces a tailored, ATS-safe .docx for that JD.
- Gate the input before optimizing: call out structural resume problems, and stop on blocking issues or a major resume/JD deviation.
- Extract weighted JD keywords, score keyword coverage before and after editing, and target a score above 85% using only truthful edits (terminology swaps, surfacing evidenced bullets, skills additions backed by experience, summary alignment, reordering).
- After each run, show a change log in a fixed template: the score before and after, one row per change with its section, what changed, its ATS impact in keyword-match points, and why, then the genuine gaps. The change log always ends with a disclaimer that the target company's ATS algorithm may differ from the logic used here.
- Ship the Claude skill in this change (`SKILL.md` plus helpers), installable directly. The ChatGPT and Cursor targets are deferred (see below).
- Keep the master resume as the source of truth. Each run produces a new per-JD file and never overwrites the master.

**BREAKING**: none (new capability).

## Capabilities

### New Capabilities
- `resume-optimization`: Tailoring a master resume to a job description with truthful, minimal edits, keyword-match scoring, and ATS-safe .docx output.

### Modified Capabilities
<!-- None: no existing capabilities in openspec/specs/ (the project has no specs yet). -->

## Impact

- **New code and content:** a `resume-optimization` capability folder under the repo, containing the skill definition, the keyword-scoring helper, and the packaging for each target.
- **Dependencies:** `python-docx` (reading and writing .docx) and `pypdf` (PDF text extraction), declared in `core/requirements.txt`. Their licenses are recorded before public release. No external skills are required.
- **Affected systems:** none existing. No APIs or databases are introduced in this change.
- **Out of scope:** the mock design interview and mock code review (separate changes), hosting, accounts, and billing.
- **Deferred to a follow-up change:** the ChatGPT target (form not yet decided: Custom GPT or MCP app) and the Cursor target (Cursor is the chosen editor; packaging as rules or plugin not yet decided). The core and the Claude skill are not blocked by either.
- **Data handling:** resumes contain personal data. The design must not store uploaded resumes beyond the session unless the user chooses to keep them.
