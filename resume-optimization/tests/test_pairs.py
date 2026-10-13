"""Five synthetic resume and JD pairs with hand-computed expected scores.

Each expected score was worked out by hand from the weights and matches before
the scorer was run. The table is also recorded in core/README.md.
"""

import os
import sys
import unittest

CORE_DIR = os.path.join(os.path.dirname(__file__), "..", "skills", "ats-resume-optimizer", "core")
sys.path.insert(0, os.path.abspath(CORE_DIR))

import score  # noqa: E402

PAIRS = [
    {
        "name": "1. partial hard-skill match",
        "keywords": [
            {"term": "Python", "weight": 3, "alternates": []},
            {"term": "SQL", "weight": 2, "alternates": []},
        ],
        "resume": "Wrote Python services for the billing team.",
        # Matched: Python (3). Total: 3 + 2 = 5. 3/5 = 60.0
        "expected": 60.0,
    },
    {
        "name": "2. alternate abbreviation",
        "keywords": [
            {"term": "Kubernetes", "weight": 3, "alternates": ["k8s"]},
            {"term": "Go", "weight": 2, "alternates": []},
        ],
        "resume": "Deployed services on K8S clusters.",
        # Matched: Kubernetes via K8S (3). Go missed. Total: 5. 3/5 = 60.0
        "expected": 60.0,
    },
    {
        "name": "3. multi-word alternate and missed term",
        "keywords": [
            {"term": "CI/CD", "weight": 2, "alternates": ["continuous delivery"]},
            {"term": "Spark", "weight": 2, "alternates": ["pyspark"]},
            {"term": "Airflow", "weight": 2, "alternates": []},
        ],
        "resume": "Ran continuous   delivery for PySpark jobs.",
        # Matched: CI/CD via continuous delivery (2), Spark via PySpark (2).
        # Missed: Airflow (2). Total: 6. 4/6 = 66.7
        "expected": 66.7,
    },
    {
        "name": "4. full coverage",
        "keywords": [
            {"term": "Python", "weight": 1, "alternates": []},
            {"term": "AWS", "weight": 1, "alternates": []},
        ],
        "resume": "Built Python tooling on AWS.",
        # Matched: both (1 + 1). Total: 2. 2/2 = 100.0
        "expected": 100.0,
    },
    {
        "name": "5. no word-boundary false positive",
        "keywords": [
            {"term": "Java", "weight": 3, "alternates": []},
            {"term": "Excel", "weight": 1, "alternates": []},
        ],
        "resume": "Maintained JavaScript dashboards and Excel sheets.",
        # Java does not match inside JavaScript (boundary rule), so it is missed.
        # Matched: Excel (1). Total: 4. 1/4 = 25.0
        "expected": 25.0,
    },
]


class HandComputedPairTests(unittest.TestCase):
    def test_each_pair_matches_hand_computed_score(self):
        for pair in PAIRS:
            with self.subTest(pair=pair["name"]):
                keywords = score.validate_keywords({"keywords": pair["keywords"]})
                result = score.score_resume(keywords, pair["resume"])
                self.assertEqual(result.score, pair["expected"])


if __name__ == "__main__":
    unittest.main()
