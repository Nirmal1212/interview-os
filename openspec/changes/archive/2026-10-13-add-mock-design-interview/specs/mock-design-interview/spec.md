# Spec Delta

## Purpose

Runs a realistic, interactive system design mock interview tailored to a track, a role, and optionally a job description and resume. It ends with a scorecard, a level signal, improvement advice, and a reference design, so the candidate can practice without a human interviewer.

## ADDED Requirements

### Requirement: Required inputs
The system SHALL ask for the track, the target role and level, and a job description or company and team context when any of them is missing. It SHALL ask for all missing required inputs in one message and MUST NOT start the interview until they are provided.

#### Scenario: Missing required input
- **WHEN** the user asks for a mock design interview without naming a track
- **THEN** the system asks for the track, role and level, and job description or company context in one message

#### Scenario: All required inputs given
- **WHEN** the user gives a track, a role and level, and a job description
- **THEN** the system proceeds to problem selection without asking again

### Requirement: Optional inputs
The system SHALL accept, but never require, a resume, a named problem, a duration, an interviewer style, and focus areas. When not given, the system SHALL use a duration of 45 simulated minutes, a standard interviewer style, and no focus areas.

#### Scenario: Defaults applied
- **WHEN** the user gives only the required inputs
- **THEN** the interview runs for 45 simulated minutes with a standard interviewer style

#### Scenario: Interviewer style chosen
- **WHEN** the user asks for a tough bar-raiser interviewer
- **THEN** the interviewer probes harder on each answer and gives less guidance on hints

### Requirement: Resume input
The system SHALL accept the candidate's resume as pasted text or as an uploaded .docx or PDF file. The system SHALL reference only experience that the resume states. When an uploaded file has no readable text, the system SHALL say so and ask the user to paste the resume.

#### Scenario: Uploaded .docx
- **WHEN** the user uploads a .docx resume
- **THEN** the system reads its text and uses it to tailor probes

#### Scenario: Scanned PDF
- **WHEN** the user uploads a PDF with no text layer
- **THEN** the system says the file has no readable text and asks the user to paste the resume

#### Scenario: Gap in the resume
- **WHEN** the job description asks for a skill the resume does not mention
- **THEN** the system probes that area fairly and does not assume the candidate has the experience

### Requirement: Problem proposal
When the user has not named a problem, the system SHALL propose six to eight problems in a table with the columns number, problem, what it tests, and link to the job description. It SHALL recommend an order, ask which problem to start with, and then stop until the user answers.

#### Scenario: Problems proposed
- **WHEN** the user has given the required inputs and named no problem
- **THEN** the system shows six to eight problems in the table, recommends an order, and asks which to start with

#### Scenario: Problem named
- **WHEN** the user names a specific problem
- **THEN** the system skips the proposal and starts the interview with that problem

### Requirement: Interviewer turns
During the interview the system SHALL give one interviewer turn per reply, kept to a few sentences. The problem statement SHALL be under-specified and SHALL NOT list requirements. The system MUST NOT reveal or describe the reference design while the interview is in progress.

#### Scenario: Problem statement
- **WHEN** the interview starts
- **THEN** the system gives two to four sentences of problem statement with no list of requirements

#### Scenario: Design withheld
- **WHEN** the candidate asks how the system should be built
- **THEN** the interviewer asks the candidate what they would propose, and does not give the design

### Requirement: Interview structure and timing
The interview SHALL follow these phases, in order: clarification, estimates, high-level design, deep dives, curveballs, and wrap-up. The system SHALL announce elapsed simulated time lightly, for example "about 15 minutes in". Answers to clarifying questions SHALL use concrete numbers, and those numbers SHALL stay consistent when later curveballs refer to them.

#### Scenario: Clarification answered with numbers
- **WHEN** the candidate asks about expected volume
- **THEN** the interviewer answers with a specific figure

#### Scenario: Estimates requested
- **WHEN** the candidate reaches design without estimating scale
- **THEN** the interviewer asks for rough scale calculations

#### Scenario: Curveball stays consistent
- **WHEN** the interviewer introduces a 10x volume increase after a volume figure was given
- **THEN** the new volume is ten times the figure given earlier

#### Scenario: Skipped clarification
- **WHEN** the candidate skips clarifying questions and moves to design
- **THEN** the interviewer records that for the scorecard and lets the candidate continue

### Requirement: Interviewer behavior
The interviewer SHALL ask why behind each major design choice and ask for the alternative the candidate rejected. When the candidate asks for a hint, the interviewer SHALL give a question rather than an answer, and SHALL record that a hint was used. When the candidate says something technically wrong, the interviewer SHALL probe it rather than correct it on the spot.

The interviewer SHALL respond to these commands at any time: "pause", "hint", and "end interview".

#### Scenario: Hint requested
- **WHEN** the candidate says "hint"
- **THEN** the interviewer asks a guiding question and records the hint for the scorecard

#### Scenario: Incorrect statement
- **WHEN** the candidate makes a technically wrong claim
- **THEN** the interviewer asks a question that tests the claim, such as "what happens when the consumer restarts?", and does not state the correction

#### Scenario: End interview
- **WHEN** the candidate says "end interview"
- **THEN** the system leaves the interview and moves to the debrief

### Requirement: Debrief
When the interview ends, the system SHALL step out of character and give a debrief containing, in order: a scorecard, a level signal, the top three improvements, a reference design, and two or three follow-up drills.

The scorecard SHALL rate these dimensions from 1 to 4, with one line of evidence from the candidate's answers: requirements and scoping, estimation, architecture, depth, trade-offs, reliability and operations, cost awareness, and communication. For engineering manager roles it SHALL also rate leadership, which is the ninth dimension. For other roles the leadership dimension SHALL be omitted.

The level signal SHALL be one of: Strong hire, Hire, Lean no, or No hire.

The reference design SHALL state where the candidate's design matched and where it diverged.

#### Scenario: Debrief order
- **WHEN** the interview ends
- **THEN** the debrief presents the scorecard, level signal, top three improvements, reference design, and follow-up drills in that order

#### Scenario: Scorecard evidence
- **WHEN** a dimension is rated
- **THEN** the rating comes with one line of evidence from the candidate's own answers

#### Scenario: Leadership dimension for an individual contributor role
- **WHEN** the target role is not an engineering manager role
- **THEN** the leadership dimension is omitted from the scorecard

### Requirement: Level terminology
Every output SHALL refer to the top engineering level as "12x engineer". The system MUST NOT use the word "staff" as a level label in any output.

#### Scenario: Level named in the verdict
- **WHEN** the verdict says the candidate reads at the top level
- **THEN** the output uses the words "12x engineer"

### Requirement: Accuracy
The system SHALL use real mechanics, configuration, and version facts. It MUST NOT describe features that do not exist. It SHALL keep numbers consistent across the whole interview.

#### Scenario: Unknown feature
- **WHEN** the candidate names a tool or feature the system cannot verify
- **THEN** the interviewer asks the candidate to explain it rather than confirming or inventing details

### Requirement: Output scope and data handling
The system SHALL present all output in the conversation. In this version it SHALL NOT write files. When the user asks to save the scorecard or reference design, the system SHALL say that saving is not supported yet and offer to repeat the content as text the user can copy. Resume text and interview transcripts SHALL exist only within the conversation and SHALL NOT be stored by the system.

#### Scenario: Save requested
- **WHEN** the user asks to save the scorecard as a file
- **THEN** the system says saving is not supported in this version and offers the content as copyable text

#### Scenario: No stored transcript
- **WHEN** a new session starts after an interview
- **THEN** the system has no record of the earlier interview
