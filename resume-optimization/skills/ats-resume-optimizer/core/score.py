"""Keyword-match scoring for resume optimization.

A keyword counts as matched when its term or any alternate appears in the
resume text as a whole phrase, ignoring case and extra whitespace. The score
is the matched weight divided by the total weight, as a percentage rounded to
one decimal place. This is a keyword-match proxy, not the output of any
commercial ATS.

Usage: python score.py keywords.json resume.txt
"""

import json
import re
import sys
from dataclasses import dataclass

ALLOWED_WEIGHTS = (1, 2, 3)


@dataclass(frozen=True)
class ScoreResult:
    score: float  # rounded to one decimal place, for display
    matched: list
    missed: list
    exact: float  # unrounded, so per-change impacts add up to the total


def _normalize(text):
    return re.sub(r"\s+", " ", text).strip().lower()


def _phrase_pattern(phrase):
    # Boundaries are alphanumeric on both sides, so "k8s" does not match inside
    # "k8sx" and "CI/CD" still matches as a unit.
    return re.compile(r"(?<![a-z0-9])" + re.escape(_normalize(phrase)) + r"(?![a-z0-9])")


def validate_keywords(data):
    """Check a parsed keywords.json object and return its keyword list."""
    if not isinstance(data, dict) or not isinstance(data.get("keywords"), list):
        raise ValueError('keywords.json must be an object with a "keywords" list')
    if not data["keywords"]:
        raise ValueError("keywords list is empty")
    for index, item in enumerate(data["keywords"]):
        if not isinstance(item, dict):
            raise ValueError(f"keyword {index} must be an object")
        term = item.get("term")
        if not isinstance(term, str) or not term.strip():
            raise ValueError(f"keyword {index} needs a non-empty term")
        if item.get("weight") not in ALLOWED_WEIGHTS or isinstance(item.get("weight"), bool):
            raise ValueError(f'keyword "{term}" weight must be 1, 2, or 3')
        alternates = item.get("alternates", [])
        if not isinstance(alternates, list) or not all(isinstance(a, str) for a in alternates):
            raise ValueError(f'keyword "{term}" alternates must be a list of strings')
    return data["keywords"]


def score_resume(keywords, resume_text):
    """Score resume_text against a validated keyword list."""
    text = _normalize(resume_text)
    total = 0
    matched_weight = 0
    matched, missed = [], []
    for item in keywords:
        weight = item["weight"]
        total += weight
        phrases = [item["term"]] + item.get("alternates", [])
        if any(_phrase_pattern(p).search(text) for p in phrases):
            matched_weight += weight
            matched.append(item["term"])
        else:
            missed.append(item["term"])
    if total == 0:
        raise ValueError("total keyword weight is zero")
    exact = 100 * matched_weight / total
    return ScoreResult(score=round(exact, 1), matched=matched, missed=missed, exact=exact)


def main(argv):
    if len(argv) != 3:
        print("usage: python score.py keywords.json resume.txt", file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        keywords = validate_keywords(json.load(f))
    with open(argv[2], encoding="utf-8") as f:
        resume_text = f.read()
    result = score_resume(keywords, resume_text)
    print(f"Keyword-match score: {result.score}%")
    print(f"Matched ({len(result.matched)}): {', '.join(result.matched) or 'none'}")
    print(f"Missed ({len(result.missed)}): {', '.join(result.missed) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
