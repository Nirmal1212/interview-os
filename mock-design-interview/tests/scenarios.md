# Mock design interview: scenarios

Run each scenario by hand against the installed skill, in a fresh conversation. Record the result in the last column as `pass`, `fail` (with a short note), or `not run`.

Each row covers one behavior from `openspec/changes/add-mock-design-interview/specs/mock-design-interview/spec.md`. Requirement names match the spec.

## Inputs

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S1 | Required inputs | Ask: "Run a mock system design interview." Give no track, role, or job description. | One message asks for track, role and level, and job description or company context. The interview does not start. | not run |
| S2 | Optional inputs | Give track, role, and a job description only. | The interview runs 45 simulated minutes with a standard interviewer style. | not run |
| S3 | Resume input | Upload a scanned PDF with no text layer (for example, an image export). | The skill says the file has no readable text and asks the user to paste the resume. It does not guess at content. | not run |
| S4 | Resume input | Upload a .docx resume with a Skills and an Experience section. | The skill reads the file and refers to its experience in at least one probe. | not run |
| S5 | Resume input | Upload a resume that does not mention Kafka, and a job description that asks for Kafka. | The skill probes Kafka fairly and does not say the candidate has it. | not run |
| S6 | Optional inputs | Ask for a tough bar-raiser interviewer style. | Probes are harder and hints are sparser than in the standard style. | not run |

## Problem selection

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S7 | Problem proposal | Give all required inputs; name no problem. | A table of six to eight problems with columns #, Problem, What it tests, Link to the job description. An order is recommended, the user is asked which to start with, and the skill stops. | not run |
| S8 | Problem proposal | Give all required inputs and name "design a streaming ingest pipeline". | No table. The interview starts with that problem. | not run |

## Interview turns

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S9 | Interviewer turns | Start the interview on a named problem. | The problem statement is two to four sentences, lists no requirements, and the turn is short. | not run |
| S10 | Interviewer turns | Ask: "What would your design be?" in the first turn. | The interviewer asks what the candidate would propose. The reference design is not given. | not run |

## Interview structure

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S11 | Interview structure and timing | Ask the interviewer for the expected volume. | A specific figure is given. | not run |
| S12 | Interview structure and timing | Give an estimate of 2,000 events per second. Then reach the curveball phase. | The 10x curveball is 20,000 events per second, matching the earlier figure. | not run |
| S13 | Interview structure and timing | Skip all clarifying questions and go straight to a design. | The interviewer notes the skipped clarification for the scorecard and lets the candidate continue. | not run |
| S14 | Interview structure and timing | Run an interview for about 15 simulated minutes. | Elapsed time is announced lightly, for example "about 15 minutes in", and the phases follow the order in the skill. | not run |

## Interviewer behavior

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S15 | Interviewer behavior | Type "hint" during the design phase. | A guiding question is asked, not an answer. The hint is recorded for the scorecard. | not run |
| S16 | Interviewer behavior | State a wrong claim, for example that a consumer group delivers each message exactly once with no configuration. | The interviewer asks a question that tests the claim. The correction is not stated. | not run |
| S17 | Interviewer behavior | Type "end interview". | The interview stops and the debrief begins. | not run |
| S18 | Interviewer behavior | Type "pause" mid-interview. | The interview pauses without a debrief. | not run |

## Debrief

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S19 | Debrief | End an interview. | The debrief appears in this order: scorecard, level signal, top three improvements, reference design, follow-up drills. | not run |
| S20 | Debrief | Read the scorecard. | Each rated dimension has one line of evidence quoted or paraphrased from the candidate's answers. | not run |
| S21 | Debrief | Run an interview for an individual contributor role. | The leadership dimension is omitted from the scorecard. | not run |
| S22 | Debrief | Run an interview for an engineering manager role. | The leadership dimension is present and rated. | not run |

## Terminology

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S23 | Level terminology | Finish an interview where the answers read at the top level. | The verdict says "12x engineer". The word "staff" does not appear as a level label anywhere in the output. | not run |

## Accuracy

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S24 | Accuracy | Name a tool that does not exist, for example "FluxDB cluster mode". | The interviewer asks the candidate to explain it. It is not confirmed and no details are invented. | not run |
| S25 | Accuracy | Finish an interview; read the reference design and the interview numbers. | The reference design uses the same volumes as the interview, and the facts are real. | not run |

## Output and data

| ID | Requirement | Setup | Expected behavior | Result |
|---|---|---|---|---|
| S26 | Output scope and data handling | Ask: "Save the scorecard as a file." | The skill says saving is not supported yet and offers the content as text to copy. No file is written. | not run |
| S27 | Output scope and data handling | Start a new conversation and ask about the earlier interview. | The skill has no record of the earlier interview and does not claim to. | not run |
