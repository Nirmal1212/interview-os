# Mock Design Interview

Practice system design interviews with a realistic, interactive interviewer. You drive the design, and the interviewer probes it, asks for the numbers, and introduces curveballs. At the end you get a scorecard, a level signal, your top improvements, a reference design, and follow-up drills.

## Install in Claude Code

1. Add the interview-os marketplace:

   ```
   /plugin marketplace add Nirmal1212/interview-os
   ```

2. Install the plugin:

   ```
   /plugin install mock-design-interview@interview-os
   ```

3. Start a new session, or run `/reload-plugins`.

To check it is installed, run `/plugin` and look for `mock-design-interview`.

## Use it

Ask for a mock interview and give three things: your track (for example data engineering or backend), your target role and level, and a job description or the company and team. A resume is optional.

> Run a mock system design interview for a senior data engineer role. Here is the job description: ...

The interviewer then:

1. Proposes six to eight problems, with what each tests, and asks which to start with. You can name a problem instead.
2. Runs the interview in turns of a few sentences, announcing the time as it goes.
3. Gives the debrief when you say `end interview` or the simulated time runs out.

### Commands during the interview

- `hint`: asks a guiding question. The hint is noted in your scorecard.
- `pause`: stops the interview without a debrief.
- `end interview`: moves to the debrief.

### Interviewer styles

Ask for a supportive, standard (the default), or tough bar-raiser interviewer. A bar-raiser probes harder and gives less guidance.

## Resume

You can paste your resume as text, or upload a .docx or PDF file. Scanned PDFs without a text layer cannot be read. If that happens, paste the text instead.

## What you get

- **Scorecard:** each dimension rated from 1 to 4, with one line of evidence from your answers. The leadership dimension appears only for engineering manager roles.
- **Level signal:** Strong hire, Hire, Lean no, or No hire, with whether your answers read at the "12x engineer" bar for depth.
- **Top three improvements:** what to change, and what to say next time.
- **Reference design:** a model answer, marked where your design matched and where it diverged.
- **Follow-up drills:** two or three questions aimed at your weakest area.

## Limits

- Output appears in the conversation only. The skill cannot save a scorecard or a reference design to a file yet. Ask it to repeat the content as text, and copy that.
- Interview content is not stored. A new conversation has no record of an earlier interview.
- Accuracy depends on the skill's knowledge. The interviewer asks you to explain any tool or feature it cannot verify, rather than confirming it. Check any fact you plan to rely on.

## Your data

- Your resume and the interview exist only in the conversation.
- When you use the skill in Claude, what you share becomes part of that Claude conversation, under Claude's terms for that product.
- The plugin does not store, upload, or keep any copy of your interview.

## For contributors

The plugin lives in `mock-design-interview/`:

```
.claude-plugin/plugin.json                 plugin manifest
skills/mock-design-interview/
  SKILL.md                                  the interviewer's rules
  core/docx_io.py                           resume reader (copied from resume-optimization)
  core/requirements.txt                     python-docx and pypdf
tests/
  test_reader_copy.py                       checks the reader copy is identical
  scenarios.md                              behavior scenarios to run by hand
```

Run the tests from `mock-design-interview/`:

```
python -m unittest discover tests
```

If you change `resume-optimization/skills/ats-resume-optimizer/core/docx_io.py`, copy it here byte-for-byte. The test fails until the two match.
