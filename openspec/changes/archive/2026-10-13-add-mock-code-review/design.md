# Design

## Context

The mock design interview is a prompt-only plugin in `mock-design-interview/`. Its rules, turn behavior, and debrief live in `SKILL.md`, and it has no runtime code beyond a copied resume reader. This change follows the same pattern. See proposal.md for scope and specs/mock-code-review/spec.md for the behavior contract.

Installed plugins are copied into the plugin cache as isolated folders, so this plugin cannot share code with the interview plugin at run time. The turn rules and the "12x engineer" terminology are short enough to restate in this plugin's `SKILL.md`.

## Goals / Non-Goals

**Goals:**
- A plugin that generates a fresh review change for each session, in the user's language, set in the user's job domain.
- Planted issues that stay hidden until the debrief, and a fair scorecard against them.
- A generated change that is accurate: valid code, and only real defects.

**Non-Goals:**
- Running the generated code. No sandbox or test runner is available to the plugin.
- Reviewing user-pasted code. Out of scope for v1, as the spec states.
- Any ChatGPT or Cursor packaging.

## Decisions

**D1. Plugin folder at the repo root, matching the other two plugins.** `mock-code-review/` gets `.claude-plugin/plugin.json`, `skills/mock-code-review/SKILL.md`, a README, and tests. The root marketplace gets a third entry.

**D2. The skill is prompt-only.** The generation rules, the review turn rules, the assessment categories, and the debrief rubric live in SKILL.md. Alternative: a fixed bank of sample changes in the plugin. Rejected because the spec requires the change to reflect the candidate's job domain, and a fixed bank cannot cover every domain.

**D3. The change is generated in the conversation, and its planted issues are recorded in the conversation.** The skill writes the change and records the issue list in its own turn, marked as private until the debrief. The rule against revealing issues is stated in SKILL.md and checked by a scenario. Alternative: write the issue list to a file the candidate cannot read. Rejected because the plugin writes no files in v1.

**D4. Accuracy is checked by the generator, before the change is shown.** Without a runtime, the skill must check its own output. The rule in SKILL.md is: read the generated code for syntax, confirm each planted issue is a real defect in the stated context, and remove any part that depends on library behavior it cannot confirm. Alternative: execute the code in a sandbox. Rejected because no sandbox is available to the plugin, and an execution step would add a dependency the other plugins do not have.

**D5. Assessment uses three categories per finding.** A finding is a match, a partial match, or a false positive. This makes the scorecard reproducible for a given transcript, and it gives the debrief a concrete list of missed issues. Alternative: a single numeric score per finding. Rejected because it hides the difference between finding the right line and explaining the right risk.

**D6. Verification has two parts.** A test checks that the plugin and marketplace manifests parse and resolve. A scenario file, run by hand, covers the behavior: hidden issues, the planted-issue mix, false-positive probing, and the debrief order.

## Risks / Trade-offs

- **Leaking issues.** The model can mention a planted issue early, which spoils the session. Mitigation: the rule in SKILL.md, and scenario S-issue-hidden, which the author runs.
- **Subtly wrong code.** A generated change can contain a bug the generator did not intend, which would make a planted issue ambiguous or a correct part wrong. Mitigation: the self-check in D4, and the rule that every planted issue must be defensible in the debrief.
- **Subjective scoring.** Matching a finding to a planted issue is judgment. Mitigation: the three categories in D5, and one line of evidence per dimension.
- **Language coverage.** The model's accuracy varies across languages. Mitigation: the candidate names the language, and the skill says when it is not confident in a language's details.
- **Rule drift between plugins.** The turn rules and terminology are restated in two plugins, so they can diverge. Mitigation: both are short and checked by the scenario files.

## Migration Plan

This is a new plugin, so there is nothing to migrate. Rollout:
1. Plugin folder, SKILL.md, and manifests, with the manifest test.
2. Marketplace entry and a local install check.
3. Scenario file run by hand before the first release.

Rollback: remove the plugin folder and its marketplace entry. The other plugins share no runtime code with it.
