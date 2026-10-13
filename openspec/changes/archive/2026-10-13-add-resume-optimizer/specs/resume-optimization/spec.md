# Spec Delta

## Purpose

Tailors a candidate's master resume to one job description at a time, using only experience the resume or the candidate already supports, and reports keyword-match coverage before and after.

## ADDED Requirements

### Requirement: Master resume input
The system SHALL accept a master resume in .docx or PDF format as the source for optimization. The system MUST NOT modify the master resume file.

#### Scenario: Accepted formats
- **WHEN** the user provides a .docx or PDF resume
- **THEN** the system reads the full text, including section headers, dates, titles, and skills

#### Scenario: Unsupported format
- **WHEN** the user provides a file in any other format
- **THEN** the system asks for a .docx or PDF and performs no optimization

#### Scenario: Master preserved
- **WHEN** an optimization run completes
- **THEN** the master resume file is byte-identical to its state before the run

### Requirement: Job description input
The system SHALL accept a full job description as text. If only a role title is supplied, the system SHALL ask whether a full job description is available.

#### Scenario: Role title without JD
- **WHEN** the user supplies only a role title and declines to provide a JD
- **THEN** the system builds a representative keyword set and tells the user it did so

#### Scenario: Multiple JDs
- **WHEN** the user supplies more than one JD in one request
- **THEN** the system asks which single JD to target and optimizes for one JD at a time

### Requirement: Input quality gate
The system SHALL check the resume for structural problems before optimizing and SHALL report each major issue with the issue, its effect, and a one-line fix.

#### Scenario: Major issue reported
- **WHEN** the resume has a major issue such as missing contact information, undated roles, multi-column or table-based layout, or no measurable outcomes
- **THEN** the system reports the issue and still proceeds if the content permits

#### Scenario: Blocking issue
- **WHEN** the extracted resume text is unreadable or the resume contains only a skills list
- **THEN** the system stops and asks the user to fix the input before optimizing

### Requirement: Deviation gate
The system SHALL compare the candidate's domain, seniority, and core competencies with the JD before editing, and SHALL classify the match as aligned, adjacent, or major deviation.

#### Scenario: Major deviation stops optimization
- **WHEN** the JD's must-have core is absent from the resume
- **THEN** the system does not optimize, lists the 3 to 5 missing must-haves, and offers a closer target role or asks the candidate to confirm unlisted experience

#### Scenario: Adjacent match proceeds
- **WHEN** the resume is in the same domain family with some core gaps
- **THEN** the system proceeds, notes the genuine gaps, and optimizes only supported content

### Requirement: Truthful edits only
The system MUST NOT add employers, roles, projects, credentials, tools, metrics, or outcomes that are not present in the master resume or explicitly confirmed by the candidate in the current session.

#### Scenario: Unsupported keyword
- **WHEN** a high-weight JD keyword cannot be supported by the resume or a confirmation
- **THEN** the system leaves the keyword unmatched and lists it as a genuine gap

#### Scenario: Confirmed skill added
- **WHEN** the candidate explicitly confirms a skill not evidenced in the resume
- **THEN** the system may add that skill and records the confirmation in its reply

### Requirement: Keyword-match scoring
The system SHALL extract weighted keywords from the JD, with alternates for synonyms and abbreviations, and SHALL compute a keyword-match score for the resume before and after editing. The system MUST describe the score as a keyword-match proxy, not as the output of any specific commercial ATS.

#### Scenario: Baseline and final score reported
- **WHEN** an optimization run completes
- **THEN** the system reports the keyword-match score before and after editing

#### Scenario: Target reached
- **WHEN** the score after editing exceeds 85%
- **THEN** the system reports success with the final score

#### Scenario: Target not reachable truthfully
- **WHEN** the score cannot exceed 85% without untruthful edits
- **THEN** the system delivers the best truthful version and reports the achieved score and the remaining gap keywords

### Requirement: Minimal targeted edits
The system SHALL limit edits to terminology swaps, making evidenced content explicit, skills additions backed by experience, headline or summary alignment, and reordering. The system SHALL leave voice, structure, achievements, and working formatting unchanged.

#### Scenario: Minimal diff
- **WHEN** the resume already scores above 85%
- **THEN** the system makes only clearly beneficial micro-edits or none, and reports that no major change was needed

### Requirement: ATS-safe .docx output
The system SHALL produce a single-column .docx with standard fonts, clear section headers, and no tables, text boxes, or images for main content. The system SHALL name the file `<CandidateName>_<Role>_ATS.docx` with spaces replaced by underscores, and SHALL write it as a new file separate from the master.

#### Scenario: Output naming
- **WHEN** the candidate is named "Jane Doe" and the role is "Data Engineer"
- **THEN** the output file is named `Jane_Doe_Data_Engineer_ATS.docx`

#### Scenario: Layout rebuilt for hostile input
- **WHEN** the input is a PDF or has ATS-hostile formatting
- **THEN** the system rebuilds the content in an ATS-safe template instead of editing in place

### Requirement: Change log and disclaimer
After every optimization run, the system SHALL show a change log in the fixed template: a header with the keyword-match score before and after, a table with one row per change, the genuine gaps, and a disclaimer at the bottom. The table SHALL have the columns `#`, `Section`, `Change`, `ATS impact`, and `Why`.

The ATS impact of each change SHALL be the change in keyword-match score it causes when applied in sequence, so that the impacts add up to the total change, within rounding. The system SHALL state that impacts depend on the order in which edits were applied.

The disclaimer SHALL state that the target company's ATS algorithm may differ from the keyword-match logic used in the report. The disclaimer SHALL NOT be placed inside the resume document.

#### Scenario: Change log shown by default
- **WHEN** an optimization run completes without any commentary request
- **THEN** the reply contains the change log table, with one row per change

#### Scenario: ATS impact per change
- **WHEN** an edit raises the keyword-match score from 66.7% to 80.0%
- **THEN** that row's ATS impact is +13.3 points

#### Scenario: Zero-impact change
- **WHEN** an edit does not add or remove any matched keyword
- **THEN** that row's ATS impact is 0.0

#### Scenario: Impacts add up to total
- **WHEN** the change log is rendered
- **THEN** the sum of the row impacts equals the total score change, within 0.1 points

#### Scenario: Disclaimer at the bottom
- **WHEN** the change log is rendered
- **THEN** the disclaimer is the last line of the report

#### Scenario: No edits needed
- **WHEN** the resume already meets the target and no edits are made
- **THEN** the change log shows a single row stating that no edits were needed, and still ends with the disclaimer

### Requirement: Data handling
The system SHALL NOT retain uploaded resumes or job descriptions beyond the session unless the user opts in.

#### Scenario: Default retention
- **WHEN** a session ends without an opt-in
- **THEN** no copy of the resume text persists outside the user's own output file
