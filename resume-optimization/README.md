# ATS Resume Optimizer

Tailors your master resume to one job description. It makes only edits your experience supports, shows a change log with the ATS impact of each change, and writes an ATS-safe .docx. Your master file is never modified.

## Install the plugin in Claude Code

1. Add the interview-os marketplace:

   ```
   /plugin marketplace add Nirmal1212/interview-os
   ```

2. Install the plugin:

   ```
   /plugin install ats-resume-optimizer@interview-os
   ```

3. Start a new session, or run `/reload-plugins`, so the skill is loaded.

To check it is installed, run `/plugin` and look for `ats-resume-optimizer`.

## Use it

Attach your master resume (.docx or PDF) and paste the job description, then ask:

> Tailor my resume to this job description.

You get:

- The keyword-match score before and after.
- A change log with one row per change: the section, what changed, its ATS impact, and why.
- The genuine gaps: required keywords your experience does not support, which the optimizer does not add.
- An ATS-safe .docx named like `Jane_Doe_Data_Engineer_ATS.docx`.

The change log always ends with this disclaimer: the target company's ATS algorithm may be different from the keyword-match logic used here.

## How the score works

The score is a keyword-match proxy: the matched weight divided by the total weight, as a percentage. A keyword matches when its term or an alternate appears in the resume as a whole phrase. The full rule is in `skills/ats-resume-optimizer/core/README.md`.

**This is not an ATS guarantee.** Commercial ATS products use their own parsers and rules, and a high score here does not promise a result in any specific system.

## Truthful edits

The optimizer never adds an employer, project, metric, credential, or skill that your master resume does not support. If you have a skill you have not listed, tell it and confirm. Keywords it cannot support are reported as gaps, not invented.

## Your data

- The scripts run locally and do not send your resume anywhere.
- When you use the skill in Claude, the resume and job description you share become part of that Claude conversation, so they are handled under Claude's terms for that product.
- The optimizer does not keep copies of your resume. It writes a new output file and never writes to your master.

## For contributors

The plugin lives in `resume-optimization/`. Its layout:

```
.claude-plugin/plugin.json        plugin manifest
skills/ats-resume-optimizer/
  SKILL.md                        the skill Claude runs
  core/                           shared rules and scripts
```

Run the tests from `resume-optimization/`:

```
python -m unittest discover tests
```
