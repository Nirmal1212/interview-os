# Mock code review: scenarios

Run each scenario by hand against the installed skill, in a fresh conversation. Record the result in the last column as `pass`, `fail` (with a short note), or `not run`.

Each row covers one behavior from `openspec/changes/add-mock-code-review/specs/mock-code-review/spec.md`. The requirement column matches the spec's requirement names.

## Inputs

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S1 | Required inputs | Ask: "Run a mock code review." Give no language. | One message asks for the language, role and level, and job description or domain. The session does not start. | not run |
| S2 | Required inputs | Give a language, a role and level, and a job description. | The change is generated without asking again. | not run |
| S3 | Optional inputs | Give only the required inputs. | The session runs for 30 simulated minutes with no focus areas. | not run |
| S4 | Optional inputs | Ask to focus on concurrency. | The change includes at least one planted issue about concurrency. | not run |

## Generated change

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S5 | Planted issues stay hidden | Start a session. Before the candidate finds anything, ask: "Are there any bugs yet?" | The interviewer does not name an issue, point to a line, or describe a category. | not run |
| S6 | Generated change in the job's use case | Give a Python language choice and a data engineer job description for ingestion pipelines. | The change is an ingestion-style change, not an unrelated web handler. | not run |
| S7 | Generated change in the job's use case | Give the same inputs. | The change has a title, a two-sentence purpose, and two to four files or functions. | not run |
| S8 | Generated change in the job's use case | Inspect the generated change. | It has three to five planted issues, at least one high-severity and at least one low-severity. | not run |
| S9 | Generated change in the job's use case | Inspect the generated change. | At least one part is correct code that a reviewer should not flag. | not run |

## Review turns

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S10 | Review turns | Start a session. | The change is shown and the candidate is asked for their review in their own words. No list of issues or categories is shown. | not run |
| S11 | Review turns | The candidate lists a finding without a severity. | The interviewer asks whether it would block the merge. | not run |

## Finding assessment

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S12 | Finding assessment | The candidate describes a planted issue and its risk. | The finding is recorded as a match. | not run |
| S13 | Finding assessment | The candidate names the right line but describes the wrong risk. | The finding is recorded as a partial match, and the interviewer asks what could go wrong. | not run |
| S14 | Finding assessment | The candidate flags a correct part of the change as a bug. | The interviewer asks a question that tests the claim. It does not say the code is correct. | not run |

## Interviewer commands

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S15 | Interviewer commands | Type "hint" when stuck. | A guiding question is asked, not an answer. The hint is recorded. | not run |
| S16 | Interviewer commands | Type "end review". | The review stops and the debrief begins. | not run |

## Debrief

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S17 | Debrief | End a review. | The debrief order is: scorecard, level signal, missed issues, top three improvements, reference review, follow-up drills. | not run |
| S18 | Debrief | Read the missed-issues section. | Every planted issue the candidate did not find is named with its location and its risk. | not run |
| S19 | Output scope and data handling | Paste a diff and ask for a review. | The skill says pasted code is not supported in this version and offers a generated change instead. | not run |
| S20 | Level terminology | Finish a review where the answers read at the top level. | The verdict says "12x engineer". The word "staff" does not appear as a level label. | not run |
| S21 | Output scope and data handling | Ask: "Save the scorecard as a file." | The skill says saving is not supported yet and offers the content as copyable text. No file is written. | not run |
| S22 | Output scope and data handling | Start a new conversation and ask about the earlier review. | The skill has no record of the earlier review and does not claim to. | not run |

## Accuracy

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S23 | Accuracy | Read every planted issue in the debrief. | Each one is a real defect in the chosen language, not a style preference. | not run |
| S24 | Accuracy | Ask for a change that depends on an obscure library's exact behavior. | The change avoids that dependency, and the reference review does not rely on it. | not run |
