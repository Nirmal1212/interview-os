# Tasks

## 1. Plugin scaffold

- [x] 1.1 Create `mock-code-review/.claude-plugin/plugin.json` and `mock-code-review/skills/mock-code-review/`, verified by the manifest parsing as JSON and the skill folder existing at the path the manifest implies
- [x] 1.2 Add a `mock-code-review` entry to the root `.claude-plugin/marketplace.json` with source `./mock-code-review`, verified by the JSON parsing and the source folder containing the plugin manifest and SKILL.md

## 2. Manifest test

- [x] 2.1 Add `mock-code-review/tests/test_manifests.py` that checks the plugin manifest and the marketplace entry parse as JSON, and that the marketplace source resolves to a folder containing the manifest and `skills/mock-code-review/SKILL.md`, verified by the test passing

## 3. Skill

- [x] 3.1 Write `skills/mock-code-review/SKILL.md` with the inputs, the generation rules (language, job use case, three to five planted issues, at least one correct part), the self-check before presenting the change, the review turn rules, the three-category finding assessment, the command handling, and the debrief with the six-dimension scorecard, verified by a checklist review against each requirement in specs/mock-code-review/spec.md
- [ ] 3.2 Add the rule that planted issues are never revealed, hinted at, or named before the debrief, verified by scenario S5 in the scenario file
- [ ] 3.3 Add the rule that pasted code is declined, verified by scenario S19 in the scenario file
- [x] 3.4 Confirm SKILL.md never uses "staff" as a level label and uses "12x engineer" in every level reference, verified by a grep for the word "staff" finding no level label in SKILL.md

## 4. Scenario file

- [x] 4.1 Write `mock-code-review/tests/scenarios.md` with at least one scenario per requirement in the spec, each giving the inputs and expected behavior, verified by a checklist confirming every requirement heading in the spec has a matching scenario
- [ ] 4.2 Run each scenario by hand against the installed skill and record pass or fail in scenarios.md, verified by every row having a recorded result

## 5. Plugin documentation

- [ ] 5.1 Write `mock-code-review/README.md` covering install from the marketplace, what the session covers, the output limits (chat only, no pasted code, no saved files), and data handling, verified by a reviewer following the install steps

## 6. Install check

- [ ] 6.1 Install from the marketplace with `/plugin marketplace add` and `/plugin install mock-code-review@interview-os`, then run one session, verified by the skill being listed and the debrief showing the scorecard, level signal, planted issues, and "12x engineer" wording
