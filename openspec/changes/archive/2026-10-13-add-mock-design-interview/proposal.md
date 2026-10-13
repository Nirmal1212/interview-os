# Proposal

Written for: the author, to review the scope before the spec and design are written.

## Why

Engineers preparing for senior system design interviews have few places to practice with a realistic interviewer. Reading design guides does not train the skills an interview tests: clarifying requirements, estimating scale, defending trade-offs, and responding to curveballs. The source skill (`mock-design-interview`) already plays a demanding but fair interviewer. This change packages it as a plugin in the same interview-os marketplace as the resume optimizer, so both can be installed together.

## What Changes

- Add a mock design interview capability. The user picks a track and role, optionally supplies a job description, a resume, and focus areas. The skill proposes problems, runs a turn-by-turn interview, then gives a scorecard, level signal, top improvements, a reference design, and follow-up drills.
- The interviewer is strictly interactive: one short turn per reply, never revealing the design during the interview, and probing every major choice.
- The resume can be pasted as text or uploaded as a .docx or PDF. Uploaded files are read with the same reader the resume optimizer uses. The reader is copied into this plugin, with a test that keeps the two copies identical.
- Output appears in the conversation only. Saving the scorecard or reference design to a file is out of scope for v1.
- The scorecard uses the "12x engineer" label throughout, never "staff".
- Ship as a Claude plugin, added to the existing `interview-os` marketplace. ChatGPT and Cursor targets are out of scope, as with the resume optimizer.

**BREAKING**: none (new capability).

## Capabilities

### New Capabilities
- `mock-design-interview`: Running a realistic, interactive system design mock interview tailored to a track, role, and optional job description and resume, ending with a scorecard, level signal, and reference design.

### Modified Capabilities
<!-- None. The resume optimizer's spec is unchanged; the reader is copied, not shared. -->

## Impact

- **New content:** a `mock-design-interview` plugin folder with a skill, its interview rules, and a copy of the resume reader and its test.
- **Marketplace:** `.claude-plugin/marketplace.json` gains a second plugin entry.
- **Dependencies:** python-docx and pypdf, the same as the resume optimizer, only for uploaded files.
- **Systems:** none. No accounts, storage, or hosting. Interview transcripts exist only in the conversation.
- **Out of scope:** saving output to files, ChatGPT and Cursor targets, live scoring of audio or video, and persistent progress across sessions.
