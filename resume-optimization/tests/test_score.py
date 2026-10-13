import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

CORE_DIR = os.path.join(os.path.dirname(__file__), "..", "skills", "ats-resume-optimizer", "core")
sys.path.insert(0, os.path.abspath(CORE_DIR))

import score  # noqa: E402

EXAMPLES = os.path.abspath(os.path.join(CORE_DIR, "examples"))


def kw(term, weight, alternates=None):
    return {"term": term, "weight": weight, "alternates": alternates or []}


class ScoreTests(unittest.TestCase):
    def test_full_coverage_is_100(self):
        keywords = [kw("Python", 3), kw("SQL", 2)]
        result = score.score_resume(keywords, "Python and SQL daily")
        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.missed, [])

    def test_no_coverage_is_0(self):
        keywords = [kw("Python", 3), kw("SQL", 2)]
        result = score.score_resume(keywords, "Gardening and painting")
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.matched, [])

    def test_matching_is_case_insensitive(self):
        result = score.score_resume([kw("Kubernetes", 3)], "KUBERNETES clusters")
        self.assertEqual(result.score, 100.0)

    def test_alternate_matches_term(self):
        keywords = [kw("Kubernetes", 3, ["k8s"])]
        result = score.score_resume(keywords, "Operated k8s in production")
        self.assertEqual(result.matched, ["Kubernetes"])

    def test_multi_word_alternate_matches_across_whitespace(self):
        keywords = [kw("CI/CD", 2, ["continuous integration"])]
        result = score.score_resume(keywords, "Set up Continuous\n   Integration for ETL")
        self.assertEqual(result.matched, ["CI/CD"])

    def test_term_with_slash_matches_as_a_unit(self):
        keywords = [kw("CI/CD", 2)]
        result = score.score_resume(keywords, "Owned the ci/cd pipeline")
        self.assertEqual(result.matched, ["CI/CD"])

    def test_match_requires_word_boundary(self):
        keywords = [kw("Kubernetes", 3, ["k8s"])]
        result = score.score_resume(keywords, "Used k8sx and xk8s internally")
        self.assertEqual(result.matched, [])

    def test_score_is_weighted(self):
        keywords = [kw("Python", 3), kw("Leadership", 1)]
        result = score.score_resume(keywords, "Python only")
        self.assertEqual(result.score, 75.0)

    def test_rounds_to_one_decimal(self):
        keywords = [kw("A", 1), kw("B", 1), kw("C", 1)]
        result = score.score_resume(keywords, "A B")
        self.assertEqual(result.score, 66.7)

    def test_same_input_gives_same_score(self):
        keywords = [kw("Python", 3, ["py"]), kw("SQL", 2)]
        text = "py and sql"
        self.assertEqual(score.score_resume(keywords, text), score.score_resume(keywords, text))


class ValidationTests(unittest.TestCase):
    def test_example_file_is_valid(self):
        with open(os.path.join(EXAMPLES, "keywords.example.json"), encoding="utf-8") as f:
            keywords = score.validate_keywords(json.load(f))
        self.assertEqual(len(keywords), 5)

    def test_rejects_missing_keywords_list(self):
        with self.assertRaises(ValueError):
            score.validate_keywords({})

    def test_rejects_empty_keywords_list(self):
        with self.assertRaises(ValueError):
            score.validate_keywords({"keywords": []})

    def test_rejects_weight_outside_1_to_3(self):
        with self.assertRaises(ValueError):
            score.validate_keywords({"keywords": [kw("Python", 4)]})

    def test_rejects_boolean_weight(self):
        with self.assertRaises(ValueError):
            score.validate_keywords({"keywords": [{"term": "Python", "weight": True}]})

    def test_rejects_missing_term(self):
        with self.assertRaises(ValueError):
            score.validate_keywords({"keywords": [{"weight": 2}]})

    def test_rejects_non_string_alternates(self):
        with self.assertRaises(ValueError):
            score.validate_keywords({"keywords": [kw("Python", 2, [1])]})


class ExampleFixtureTests(unittest.TestCase):
    """Hand-computed expected score for the synthetic example.

    Total weight is 3 + 2 + 2 + 3 + 1 = 11. Matched: Kubernetes (via k8s, 3),
    CI/CD (via continuous integration, 2), Python (3). Missed: Terraform (2),
    Leadership (1). Expected score = 8 / 11 = 72.7%.
    """

    def test_example_scores_72_7(self):
        with open(os.path.join(EXAMPLES, "keywords.example.json"), encoding="utf-8") as f:
            keywords = score.validate_keywords(json.load(f))
        with open(os.path.join(EXAMPLES, "resume.example.txt"), encoding="utf-8") as f:
            text = f.read()
        result = score.score_resume(keywords, text)
        self.assertEqual(result.score, 72.7)
        self.assertEqual(result.matched, ["Kubernetes", "CI/CD", "Python"])
        self.assertEqual(result.missed, ["Terraform", "Leadership"])


class CommandLineTests(unittest.TestCase):
    def test_prints_score_and_missed_terms(self):
        keywords_path = os.path.join(EXAMPLES, "keywords.example.json")
        resume_path = os.path.join(EXAMPLES, "resume.example.txt")
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = score.main(["score.py", keywords_path, resume_path])
        output = buf.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("Keyword-match score: 72.7%", output)
        self.assertIn("Missed (2): Terraform, Leadership", output)

    def test_usage_error_returns_2(self):
        self.assertEqual(score.main(["score.py"]), 2)


if __name__ == "__main__":
    unittest.main()
