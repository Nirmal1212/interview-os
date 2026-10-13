# Tasks

## 1. Repo layout and dependency check

- [x] 1.1 Create the `resume-optimization/` folder with `core/`, `claude-skill/`, and `tests/` subfolders, and verify the folder tree exists
- [x] 1.2 Declare the runtime dependencies `python-docx` and `pypdf` in a `core/requirements.txt`, pinned to the installed versions, verified by `pip install -r core/requirements.txt` succeeding in a fresh virtual environment
- [x] 1.3 Create the `tests/` runner using Python's standard `unittest` module (no pytest), verified by `python -m unittest discover resume-optimization/tests` running the suite (unittest exits 5 with "NO TESTS RAN" only when no tests exist)

## 2. Core workflow

- [x] 2.1 Write `core/workflow.md` covering the input, quality gate, deviation gate, truthful-edit rules, edit allowlist, and report format, verified by a checklist review against each requirement in specs/resume-optimization/spec.md
- [x] 2.2 Add the keywords.json schema and an example file in `core/examples/`, verified by the example validating against the schema in a unit test
- [x] 2.3 Update `core/workflow.md` Step 8 to the change-log template (score header, per-change ATS impact table, order note, genuine gaps, disclaimer last), verified by a checklist review against the "Change log and disclaimer" requirement in the spec

## 3. Scorer

- [x] 3.1 Implement `core/score.py` as a standard-library function that takes keywords and resume text and returns score, matched, and missed, verified by a unit test that returns 100% for full coverage and 0% for none
- [x] 3.2 Add case-insensitive matching and alternates handling, verified by unit tests with "Kubernetes" matching "k8s" and "CI/CD" matching "continuous integration"
- [x] 3.3 Document the scoring formula (weighted matched over total weight, as a percentage) in `core/README.md`, verified by a worked example in the README matching the test output
- [x] 3.4 Add a command-line entry point that prints the score and the missed terms, verified by running it on a synthetic fixture and checking the printed output
- [x] 3.5 Expose the unrounded score alongside the rounded one, verified by the change-log test that per-change impacts add up to the total change

## 4. Document adapter

- [x] 4.1 Implement `core/docx_io.py` with one read function and one write function, verified by a round-trip test that reads a synthetic .docx and writes it back with its headings intact
- [x] 4.2 Add a PDF text-extraction path behind the same read function, verified by a test that a text-based PDF yields its section headers and a scanned PDF is rejected with the blocking-issue message
- [x] 4.3 Implement the single-column ATS-safe template for rebuilt output, verified by a test that the generated file contains no tables, text boxes, or images

## 5. Output rules and change log

- [x] 5.1 Implement output naming as `<CandidateName>_<Role>_ATS.docx` with spaces replaced by underscores, verified by a unit test using "Jane Doe" and "Data Engineer"
- [x] 5.2 Enforce that the master file is never written to, verified by a test that its checksum is unchanged after a full run on a fixture
- [x] 5.3 Implement `core/changelog.py` `apply_edits`, which applies edits in order and records each edit's ATS impact, verified by a test where the impacts are +13.3 and 0.0 and sum to the total change of +13.3
- [x] 5.4 Implement `render_markdown` with the fixed template and the disclaimer as the last line, verified by tests on the header, table columns, gaps line, and final disclaimer line, including the no-edits case

## 6. Claude skill packaging

- [x] 6.1 Write `claude-skill/SKILL.md` that references `core/workflow.md` rather than copying it, verified by a grep check that the workflow rules appear only in core/
- [x] 6.2 Build the change log into the skill's report step, verified by the SKILL.md step 7 showing the `apply_edits` and `render_markdown` calls against the tested module
- [x] 6.3 Install the skill locally from its folder and run one end-to-end session on a synthetic resume and JD, verified by the output .docx existing with the expected name, a before/after score, and the change log ending with the disclaimer
- [ ] 6.4 Confirm the reply shows the change log by default and ends with the disclaimer, verified by one manual run of the installed skill
- [x] 6.5 Package the skill as a Claude plugin: `resume-optimization/.claude-plugin/plugin.json`, a root `.claude-plugin/marketplace.json` listing it, and the skill under `skills/ats-resume-optimizer/` with `core/` beside it, verified by both JSON files parsing and the marketplace source resolving to a folder with the manifest and SKILL.md
- [ ] 6.6 Install from the marketplace with `/plugin marketplace add` and `/plugin install ats-resume-optimizer@interview-os`, then run one session, verified by the skill being listed and producing the change log with the disclaimer

## 7. Public release readiness

- [x] 7.1 Check the license of `python-docx` and `pypdf` from their package metadata and record each in a dependency table in `core/README.md`, verified by the table listing both with a license identifier
- [x] 7.2 Score five synthetic resume and JD pairs whose expected scores are computed by hand, and record the results in `core/README.md`, verified by each scorer output matching its hand-computed value
- [ ] 7.3 Add the README with install steps, the keyword-match disclaimer, the change-log description, and the data-handling note, verified by a reviewer following the install steps on a clean machine

## Deferred to a follow-up change

The ChatGPT and Cursor targets are not part of this change. See proposal.md (Deferred) and design.md (Open Questions). The core and the Claude skill do not depend on them.
