# Proposal

Written for: the author, to review the scope before the spec and design are written.

## Why

Code review is a core senior engineering skill, and it is hard to practice alone. Engineers preparing for data and backend roles are often asked to review code in an interview: find the real bugs, explain the risk, prioritize the comments, and say what they would not block a merge on. The mock design interview already gives candidates a realistic interviewer for system design. This change does the same for code review, so the two can be practiced together.

## What Changes

- Add a mock code review capability. The user gives a language and a job description. The skill writes a short change in that language, set in the job's domain, with a known set of issues planted in it. The candidate reviews it as they would a pull request, and the interviewer scores what they found, how they explained it, and how they prioritized it.
- The change is generated for each session, not taken from a fixed bank. The skill keeps the planted issues to itself until the debrief.
- The interviewer is strictly interactive, following the same turn rules as the design interview: short turns, no answers given away, and probing of every finding.
- The debrief gives a scorecard, a level signal, the issues the candidate missed, improvement advice, and a reference review.
- The scorecard uses the "12x engineer" label throughout, never "staff".
- Output stays in the conversation. Saving the review or the scorecard to a file is out of scope for v1.
- Ship as a Claude plugin, added to the `interview-os` marketplace. ChatGPT and Cursor targets are out of scope.

**BREAKING**: none (new capability).

## Capabilities

### New Capabilities
- `mock-code-review`: Running a mock code review session on a generated change in the user's language and job domain, with planted issues that the candidate must find, explain, and prioritize, ending with a scorecard and reference review.

### Modified Capabilities
<!-- None. The mock design interview's spec is unchanged. -->

## Impact

- **New content:** a `mock-code-review` plugin folder with a skill and its review rules, plus its tests and scenario file.
- **Marketplace:** `.claude-plugin/marketplace.json` gains a third plugin entry.
- **Dependencies:** none beyond the Claude environment. The change is generated in the conversation, so no file reader or Python packages are needed.
- **Systems:** none. No accounts, storage, or hosting.
- **Out of scope:** user-pasted code and file uploads, saving output, ChatGPT and Cursor targets, and persistent progress across sessions.
