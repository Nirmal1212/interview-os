# Resume optimization workflow

This document is the single source of the workflow rules. Every target (Claude skill, ChatGPT, Cursor) follows it. Targets link here rather than copying it.

## Inputs

1. **Master resume**: .docx or PDF. Never modified.
2. **Job description (JD)**: full text preferred. If only a role title is given, ask whether a full JD exists. If not, build a representative keyword set from common requirements for that title and seniority, and say so to the user.
3. **Commentary flag**: off by default. Turn it on only when the user asks (for example "with commentary" or "show me the changes").

If the user gives several JDs, ask which one to target. Optimize one JD at a time.

## Step 1: Read the master resume

Extract the full text, including section headers, dates, titles, and skills. Use the docx or PDF adapter in `docx_io.py`.

## Step 2: Quality gate

Check the resume for structural problems an ATS or recruiter would penalize.

Major issues: report each one, then continue if the content allows.
- Missing core sections: contact information, work experience, or skills
- No dates, or roles without dates
- Experience described only as duties, with no measurable outcomes
- Tables, text boxes, images, or multi-column layouts that ATS parsers mangle
- Critical typos in contact details, employer names, or titles
- Length far outside norms (for example 5+ pages for an individual contributor)

Blocking issues: stop and ask the user to fix the input first.
- Extracted text is unreadable or garbled (for example a scanned PDF with no text layer)
- The resume is a fragment, such as only a skills list with no experience

Each callout names the issue, why it hurts, and a one-line fix. No praise.

## Step 3: Deviation gate

Compare the candidate's domain, seniority, and core competencies with the JD. Classify the match:

- **Aligned**: same domain, most core requirements evidenced. Proceed.
- **Adjacent**: same domain family, some core gaps. Proceed, note the genuine gaps, and optimize only what the resume supports.
- **Major deviation**: different profession, or the JD's must-have core is absent. **Stop. Do not optimize.** State plainly that the resume and JD diverge, list the 3 to 5 missing must-haves, and offer a closer target role or ask the candidate to confirm any unlisted experience.

## Step 4: Extract keywords and score the baseline

1. Build `keywords.json` from the JD (schema in `examples/keywords.example.json`):
   - weight 3: must-have hard skills, tools, certifications, and the exact job title
   - weight 2: important skills or methods mentioned more than once or in requirements
   - weight 1: nice-to-haves and soft skills
   - `alternates`: synonyms, abbreviations, and inflections (for example `Kubernetes` with `k8s`)
2. Score the resume with `core/score.py`. Report this as the **keyword-match score**, not as a guarantee for any specific ATS.

## Step 5: Minimal targeted edits

Target: a score above **85%**. Work from the missed terms, highest weight first.

Allowed edits, in order of preference:
1. **Terminology swap**: use the JD's wording for work the candidate already did.
2. **Surface buried evidence**: make explicit a keyword an existing bullet implies.
3. **Skills additions**: add a JD keyword to the skills section only when the experience section already evidences it.
4. **Headline or summary alignment**: align the title or summary to the JD title when the seniority and role support it.
5. **Reordering**: move the most JD-relevant bullets and skills earlier.

Never allowed: new employers, projects, metrics, certifications, or skills without support; changed dates or titles that alter seniority.

If a high-weight keyword cannot be added truthfully, leave it unmatched and list it as a genuine gap.

Keep everything else unchanged: voice, structure, achievements, and formatting that already works. A minimal diff is a feature.

## Step 6: Re-score and iterate

Re-score after each round of edits. Repeat Steps 5 and 6 until the score is above 85% or no truthful edits remain. If 85% is not reachable truthfully, deliver the best truthful version and say so, with the achieved score and the gap keywords.

## Step 7: Produce the output .docx

- Single-column, ATS-safe layout: standard fonts, no tables for main content, no text boxes, no images, clear headers (Summary, Experience, Skills, Education).
- Clean .docx input: edit in place to keep the candidate's formatting.
- PDF or ATS-hostile input: rebuild in the single-column template.
- File name: `<CandidateName>_<Role>_ATS.docx`, with spaces replaced by underscores.
- Write a new file. Never write to the master.

## Step 8: Report (change log)

Every run ends with the change log, rendered by `core/changelog.py` (`apply_edits` then `render_markdown`). Its fixed template is:

1. A header line: keyword-match score before and after, with the points changed.
2. One table with columns `#`, `Section`, `Change`, `ATS impact`, `Why`. One row per edit, in the order applied. `ATS impact` is the points the edit adds to the score when applied in sequence. Impacts add up to the total change, within rounding.
3. A note that impacts depend on the order the edits were applied.
4. The genuine gaps: high-weight keywords not added because the resume has no supporting evidence.
5. The disclaimer, as the last line: the target company's ATS algorithm may differ from the keyword-match logic used here.

Also show the quality callouts from Step 2 above the change log. The disclaimer belongs in this report only, never inside the resume .docx.

Keep each `Change` and `Why` cell under about ten words.

## Consistency rules

- Every keyword added must trace to evidence in the master resume or to a confirmation the candidate gave in this session. Record the confirmation in the reply.
- The master resume and the candidate's stated facts are the only sources of content.
- The keyword-match score is a proxy. Say so when reporting it.
