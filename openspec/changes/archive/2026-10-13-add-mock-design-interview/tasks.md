# Tasks

## 1. Plugin scaffold

- [x] 1.1 Create `mock-design-interview/.claude-plugin/plugin.json` and `mock-design-interview/skills/mock-design-interview/`, verified by the manifest parsing as JSON and the skill folder existing at the path the manifest implies
- [x] 1.2 Add a `mock-design-interview` entry to the root `.claude-plugin/marketplace.json` with source `./mock-design-interview`, verified by the JSON parsing and the source folder containing the plugin manifest and SKILL.md

## 2. Resume reader copy

- [x] 2.1 Copy `resume-optimization/skills/ats-resume-optimizer/core/docx_io.py` byte-for-byte to `mock-design-interview/skills/mock-design-interview/core/docx_io.py`, and add `core/requirements.txt` pinning python-docx and pypdf, verified by `pip install -r` succeeding in a fresh virtual environment
- [x] 2.2 Add `mock-design-interview/tests/test_reader_copy.py` that fails unless the two `docx_io.py` files are byte-identical, verified by the test passing now
- [x] 2.3 Add a test in the same file that reads a synthetic .docx through `read_resume` and checks its headings, verified by the test passing

## 3. Skill

- [x] 3.1 Write `skills/mock-design-interview/SKILL.md` with the inputs, problem proposal, interview turn rules, phase timing, interviewer behavior, the debrief with the nine-dimension scorecard, and the accuracy rules, verified by a checklist review against each requirement in specs/mock-design-interview/spec.md
- [ ] 3.2 Add the resume upload steps to SKILL.md: read uploads with `core/docx_io.py`, and on `UnreadableResumeError` say so and ask the user to paste the resume, verified by scenario S3 in the scenario file
- [x] 3.3 Confirm SKILL.md never uses "staff" as a level label and uses "12x engineer" in every level reference, verified by a grep for the word "staff" finding no level label in SKILL.md

## 4. Scenario file

- [x] 4.1 Write `mock-design-interview/tests/scenarios.md` with at least one scenario per requirement in the spec, each giving the inputs and the expected behavior, verified by a checklist confirming every requirement heading in the spec has a matching scenario
- [ ] 4.2 Run each scenario by hand against the installed skill and record pass or fail in scenarios.md, verified by every row having a recorded result

## 5. Plugin documentation

- [ ] 5.1 Write `mock-design-interview/README.md` covering install from the marketplace, what the interview covers, the output limits (chat only, no saved files), and data handling, verified by a reviewer following the install steps

## 6. Install check

- [ ] 6.1 Install from the marketplace with `/plugin marketplace add` and `/plugin install mock-design-interview@interview-os`, then run one session, verified by the skill being listed and the debrief showing the scorecard, level signal, and "12x engineer" wording
