---
name: ats-resume-optimizer
description: "Tailor a master resume (.docx or PDF) to one job description, making minimal truthful edits to raise the keyword-match score above 85%, and produce an ATS-safe .docx. Use when the user asks to tailor, optimize, align, or make a resume pass ATS for a job, role, or job description, or uploads a resume together with a job posting or role title."
---

# ATS Resume Optimizer

Tailor the candidate's master resume to one job description (JD). Change as little as possible, never invent experience, and report the keyword-match score before and after.

The full workflow rules are in `core/workflow.md`, next to this file. Read that file before starting and follow it exactly. Do not work from memory of the rules.

## Setup

Before step 2, check that the libraries import: `python -c "import docx, pypdf"`. If that fails, run `pip install -r core/requirements.txt` from this skill's folder, then continue. Tell the user you installed them.

## Steps

1. **Get inputs.** Master resume (.docx or PDF) and the JD text. If only a role title is given, ask whether a full JD exists. If several JDs are given, ask which one to target.
2. **Read the master** with the adapter:
   ```python
   import sys; sys.path.insert(0, "core")
   from docx_io import read_resume, UnreadableResumeError
   blocks = read_resume("path/to/master.docx")   # or .pdf
   ```
   If this raises `UnreadableResumeError`, show its message to the user and stop.
3. **Run the quality and deviation gates** from `core/workflow.md` (Steps 2 and 3) before editing. Stop on a blocking issue or a major deviation.
4. **Build `keywords.json`** from the JD using the schema in `core/examples/keywords.example.json`, then score:
   ```
   python core/score.py keywords.json resume.txt
   ```
   Write `resume.txt` from the block texts. Report the result as a keyword-match score, not an ATS guarantee.
5. **Edit** only as `core/workflow.md` Step 5 allows, working through the missed terms in the order it specifies. Re-score after each round, and stop when `core/workflow.md` Step 6 says to.
6. **Write the output** with the tailored blocks. This never touches the master:
   ```python
   from docx_io import write_tailored_resume
   path = write_tailored_resume("path/to/master.docx", "outputs", "Candidate Name", "Role", blocks)
   ```
7. **Report** with the change log, as `core/workflow.md` Step 8 specifies. Build the edits as `Edit` objects with `core/changelog.py`, then render:
   ```python
   from changelog import Edit, apply_edits, render_markdown
   from score import validate_keywords
   keywords = validate_keywords(keywords_json)  # the parsed keywords.json dict
   edited, report = apply_edits(keywords, blocks, [Edit(4, "new text", "what changed", "why")])
   print(render_markdown(report))
   ```
   The rendered output always ends with the disclaimer. Show it as the final part of your reply.

The truthful-edit, master-protection, and reporting rules are defined in `core/workflow.md` and apply to every step above.
