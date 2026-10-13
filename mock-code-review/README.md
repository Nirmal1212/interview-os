# Mock Code Review

Practice code review with a realistic interviewer. You give a language and the job you are preparing for. The session writes a short change in that language, set in the job's domain, with a few real problems planted in it. You review it as you would a pull request, and the interviewer assesses what you found, how you explained it, and how you prioritized it.

## Install in Claude Code

1. Add the interview-os marketplace:

   ```
   /plugin marketplace add Nirmal1212/interview-os
   ```

2. Install the plugin:

   ```
   /plugin install mock-code-review@interview-os
   ```

3. Start a new session, or run `/reload-plugins`.

To check it is installed, run `/plugin` and look for `mock-code-review`.

## Use it

Ask for a code review session, and give three things: the programming language, your target role and level, and a job description or the domain you work in.

> Run a mock code review. Language: Python. Role: senior data engineer. Domain: ingestion pipelines for event data.

The interviewer then:

1. Shows you the change, with no list of problems.
2. Asks for your review in your own words. For each finding, say how severe it is and whether it would block the merge.
3. Assesses each finding, and probes any that look wrong with a question rather than a correction.
4. Gives the debrief when you say `end review` or the time runs out.

You can ask for a focus area, such as concurrency or data correctness. The default session is 30 simulated minutes.

### Commands during the review

- `hint`: asks a guiding question. The hint is noted in your scorecard.
- `pause`: stops the review without a debrief.
- `end review`: moves to the debrief.

## What you get

- **Scorecard:** six dimensions, each rated from 1 to 4 with one line of evidence from your review: issue detection, risk explanation, prioritization, fix suggestion, false positives, and communication.
- **Level signal:** Strong hire, Hire, Lean no, or No hire, with whether your review reads at the "12x engineer" bar for depth.
- **Missed issues:** every planted problem you did not find, with its location and its risk.
- **Top three improvements:** what to change, and what to write next time.
- **Reference review:** a model review of the change, marked where yours matched and where it diverged.
- **Follow-up drills:** two or three practice prompts aimed at your weakest dimension.

## Limits

- The change is generated for each session, so the problems differ from one session to the next.
- Pasted code is not supported in this version. The skill offers a generated change instead.
- Output appears in the conversation only. The skill cannot save the review or the scorecard to a file yet. Ask it to repeat the content as text, and copy that.
- Nothing is stored. A new conversation has no record of an earlier review.
- The generated code is checked by the skill before it is shown, but it is not run. Check any detail you plan to rely on.

## Your data

- The change, the planted problems, and your review exist only in the conversation.
- When you use the skill in Claude, what you share becomes part of that Claude conversation, under Claude's terms for that product.
- The plugin does not store, upload, or keep any copy of your review.

## For contributors

The plugin lives in `mock-code-review/`:

```
.claude-plugin/plugin.json          plugin manifest
skills/mock-code-review/SKILL.md    the reviewer's rules
tests/test_manifests.py             checks the manifests and marketplace entry
tests/scenarios.md                  behavior scenarios to run by hand
```

Run the tests from `mock-code-review/`:

```
python -m unittest discover tests
```
