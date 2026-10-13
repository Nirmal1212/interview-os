# Spec Delta

## Purpose

Runs a mock code review session. The skill writes a short change in the user's language, set in the use case of their target job, with issues planted that a strong reviewer should catch. The candidate reviews the change, and the interviewer scores their findings, explanations, and prioritization, then gives a debrief with a scorecard and a reference review.

## ADDED Requirements

### Requirement: Required inputs
The system SHALL ask for the programming language, the target role and level, and a job description or domain context when any of them is missing. It SHALL ask for all missing required inputs in one message and MUST NOT start the session until they are provided.

#### Scenario: Missing required input
- **WHEN** the user asks for a mock code review without naming a language
- **THEN** the system asks for the language, role and level, and job description or domain context in one message

#### Scenario: All required inputs given
- **WHEN** the user gives a language, a role and level, and a job description
- **THEN** the system generates the change without asking again

### Requirement: Optional inputs
The system SHALL accept, but never require, focus areas and a duration. When not given, the system SHALL use a duration of 30 simulated minutes and no focus areas.

#### Scenario: Defaults applied
- **WHEN** the user gives only the required inputs
- **THEN** the session runs for 30 simulated minutes with no focus areas

#### Scenario: Focus area given
- **WHEN** the user asks to focus on concurrency
- **THEN** the change includes at least one planted issue in that area

### Requirement: Generated change in the job's use case
The system SHALL generate one short change in the requested language that reflects the use case in the job description. The change SHALL look like a real pull request: a small set of files or functions, plausible names, and a stated purpose. The system SHALL plant three to five issues of varied severity in it, and SHALL include correct code that a reviewer should not flag.

#### Scenario: Use case reflected
- **WHEN** the job description is for a data engineer working on ingestion pipelines
- **THEN** the change is an ingestion-style change, not an unrelated web handler

#### Scenario: Issue count and mix
- **WHEN** the change is generated
- **THEN** it contains three to five planted issues with at least one high-severity issue and at least one low-severity issue

#### Scenario: Correct code is present
- **WHEN** the change is generated
- **THEN** at least one part of it is correct code that does not need a comment

### Requirement: Planted issues stay hidden
The system SHALL keep the list of planted issues out of the conversation until the debrief. The system MUST NOT reveal an issue, hint at its location, or name its category during the review.

#### Scenario: Issue not revealed
- **WHEN** the candidate has not yet found a planted issue
- **THEN** the interviewer does not name it, point to its line, or describe its category

### Requirement: Review turns
The system SHALL present the change and ask the candidate for their review comments, in their own words. During the review the system SHALL give one interviewer turn per reply, kept to a few sentences. The system SHALL ask the candidate to say how severe each finding is and whether it would block the merge.

#### Scenario: Change presented
- **WHEN** the session starts
- **THEN** the system shows the change and asks for the candidate's review, with no list of issues

#### Scenario: Severity asked
- **WHEN** the candidate lists a finding without a severity
- **THEN** the interviewer asks whether it would block the merge

### Requirement: Finding assessment
The system SHALL assess each candidate finding as one of: matches a planted issue, partly matches a planted issue, or does not match any planted issue. A finding that does not match is a false positive. The system SHALL probe each false positive with a question rather than telling the candidate it is wrong.

#### Scenario: Planted issue found
- **WHEN** the candidate describes a planted issue with its risk
- **THEN** the finding is recorded as a match

#### Scenario: Partial match
- **WHEN** the candidate spots the right line but describes the wrong risk
- **THEN** the finding is recorded as a partial match and the interviewer asks what could go wrong

#### Scenario: False positive probed
- **WHEN** the candidate flags correct code as a bug
- **THEN** the interviewer asks a question that tests the claim, and does not state that the code is correct

### Requirement: Interviewer commands
The interviewer SHALL respond to these commands at any time: "hint", "pause", and "end review". A hint SHALL be a guiding question, not an answer, and SHALL be recorded for the scorecard.

#### Scenario: Hint requested
- **WHEN** the candidate says "hint"
- **THEN** the interviewer asks a guiding question about the area they are stuck on, and records the hint

#### Scenario: End review
- **WHEN** the candidate says "end review"
- **THEN** the session stops and the debrief begins

### Requirement: Debrief
When the review ends, the system SHALL step out of character and give a debrief containing, in order: a scorecard, a level signal, the planted issues the candidate missed with an explanation of each, the top three improvements, a reference review, and two or three follow-up drills.

The scorecard SHALL rate these dimensions from 1 to 4, each with one line of evidence from the candidate's review: issue detection, risk explanation, prioritization, fix suggestion, false positives, and communication.

The level signal SHALL be one of: Strong hire, Hire, Lean no, or No hire.

#### Scenario: Debrief order
- **WHEN** the review ends
- **THEN** the debrief presents the scorecard, level signal, missed issues, top three improvements, reference review, and follow-up drills in that order

#### Scenario: Missed issues revealed
- **WHEN** the debrief is given
- **THEN** every planted issue the candidate did not find is named, with its location and its risk

#### Scenario: Scorecard evidence
- **WHEN** a dimension is rated
- **THEN** the rating comes with one line of evidence from the candidate's review

### Requirement: Level terminology
Every output SHALL refer to the top engineering level as "12x engineer". The system MUST NOT use the word "staff" as a level label in any output.

#### Scenario: Level named in the verdict
- **WHEN** the verdict says the candidate reads at the top level
- **THEN** the output uses the words "12x engineer"

### Requirement: Accuracy
Every planted issue SHALL be a real defect in the chosen language. The generated code MUST be valid in the chosen language and MUST NOT depend on library behavior that the system cannot verify. The reference review SHALL state only facts that are correct for the chosen language.

#### Scenario: Planted issue is real
- **WHEN** a planted issue is revealed in the debrief
- **THEN** it is a defect that would cause incorrect results, a failure, or a clear risk in the stated context

#### Scenario: Unverifiable library detail avoided
- **WHEN** a fix depends on the exact behavior of a library the system cannot check
- **THEN** the change avoids that dependency, and the reference review does not rely on it

### Requirement: Output scope and data handling
The system SHALL present all output in the conversation and SHALL NOT write files. In this version it SHALL NOT accept user-pasted code. When the user asks to save the review or the scorecard, the system SHALL say saving is not supported yet and offer to repeat the content as copyable text. The generated change, the planted issues, and the review SHALL exist only within the conversation.

#### Scenario: Pasted code declined
- **WHEN** the user pastes a diff to review
- **THEN** the system says pasted code is not supported in this version, and offers a generated change instead

#### Scenario: Save requested
- **WHEN** the user asks to save the scorecard as a file
- **THEN** the system says saving is not supported yet and offers the content as copyable text

#### Scenario: No stored session
- **WHEN** a new conversation starts after a review
- **THEN** the system has no record of the earlier review and does not claim to
