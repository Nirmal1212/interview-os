# resume-optimization core

Shared logic for the resume optimizer. The Claude skill, the ChatGPT version, and the Cursor version all call this core; none of them re-implement the rules.

## Contents

- `workflow.md`: the workflow rules (gates, truthful-edit rules, edit allowlist, report format)
- `score.py`: keyword-match scoring and a command-line entry point
- `changelog.py`: applies edits, measures each edit's ATS impact, and renders the change log with the disclaimer
- `docx_io.py`: reading and writing .docx and PDF through one adapter
- `requirements.txt`: pinned runtime dependencies
- `examples/`: a synthetic resume and keyword file for testing

## Dependencies

| Package | Version | Used for | License |
|---|---|---|---|
| python-docx | 1.2.0 | reading and writing .docx | MIT |
| pypdf | 6.6.0 | PDF text extraction | BSD-3-Clause |

Licenses were read from the installed packages' metadata. `score.py` uses the Python standard library only.

## Scoring

A keyword counts as matched when its term or any alternate appears in the resume as a whole phrase. Matching ignores case and extra whitespace. Word boundaries are required, so `k8s` does not match inside `k8sx`.

```
score = 100 * (sum of weights of matched keywords) / (sum of weights of all keywords)
```

Weights are 1, 2, or 3. The result is rounded to one decimal place.

This is a keyword-match proxy. It is not the output of any commercial ATS.

### Worked example

`examples/keywords.example.json` has five keywords with total weight 3 + 2 + 2 + 3 + 1 = 11.

| Keyword | Weight | Matched via | Counted |
|---|---|---|---|
| Kubernetes | 3 | `k8s` | yes |
| CI/CD | 2 | `continuous integration` | yes |
| Terraform | 2 | not present | no |
| Python | 3 | `Python` | yes |
| Leadership | 1 | not present | no |

Matched weight is 3 + 2 + 3 = 8, so the score is 8 / 11 = 72.7%.

Run it:

```
python skills/ats-resume-optimizer/core/score.py skills/ats-resume-optimizer/core/examples/keywords.example.json skills/ats-resume-optimizer/core/examples/resume.example.txt
```

Expected output:

```
Keyword-match score: 72.7%
Matched (3): Kubernetes, CI/CD, Python
Missed (2): Terraform, Leadership
```

### Hand-computed pairs

`tests/test_pairs.py` checks five synthetic resume and keyword pairs. Each expected score was computed by hand before the scorer ran.

| # | Case | Matched weight / total | Expected | Scorer |
|---|---|---|---|---|
| 1 | partial hard-skill match | 3 / 5 | 60.0 | 60.0 |
| 2 | alternate abbreviation (`K8S`) | 3 / 5 | 60.0 | 60.0 |
| 3 | multi-word alternate and a missed term | 4 / 6 | 66.7 | 66.7 |
| 4 | full coverage | 2 / 2 | 100.0 | 100.0 |
| 5 | no false positive inside `JavaScript` | 1 / 4 | 25.0 | 25.0 |

## Running the tests

From the `resume-optimization/` folder:

```
python -m unittest discover tests
```
