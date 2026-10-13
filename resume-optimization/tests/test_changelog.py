import os
import sys
import unittest

CORE_DIR = os.path.join(os.path.dirname(__file__), "..", "skills", "ats-resume-optimizer", "core")
sys.path.insert(0, os.path.abspath(CORE_DIR))

import changelog  # noqa: E402
from changelog import DISCLAIMER, Edit, apply_edits, render_markdown  # noqa: E402
from docx_io import Block  # noqa: E402
from score import validate_keywords  # noqa: E402

KEYWORDS = validate_keywords({"keywords": [
    {"term": "Kubernetes", "weight": 3, "alternates": ["k8s"]},
    {"term": "Python", "weight": 3, "alternates": []},
    {"term": "Spark", "weight": 2, "alternates": ["pyspark"]},
    {"term": "CI/CD", "weight": 2, "alternates": ["continuous integration"]},
    {"term": "Airflow", "weight": 2, "alternates": []},
    {"term": "Terraform", "weight": 2, "alternates": []},
    {"term": "Leadership", "weight": 1, "alternates": ["led a team"]},
]})

MASTER = [
    Block("heading", "Summary"),
    Block("paragraph", "Data engineer with six years building batch pipelines."),
    Block("heading", "Experience"),
    Block("bullet", "Built pipeline deployments on k8s clusters, cutting release time by 40 percent."),
    Block("bullet", "Introduced CI pipelines for all ETL repositories."),
    Block("bullet", "Wrote data quality tools in PySpark used by four teams."),
    Block("bullet", "Scheduled warehouse loads with Airflow DAGs."),
    Block("heading", "Skills"),
    Block("paragraph", "Python, SQL, Airflow, Git"),
]

EDITS = [
    Edit(4, "Introduced CI/CD pipelines for all ETL repositories.",
         "CI pipelines -> CI/CD pipelines", "JD term; candidate did this work"),
    Edit(6, "Scheduled nightly warehouse loads with Airflow DAGs.",
         "Added 'nightly'", "Clearer scheduling detail"),
]


class ApplyEditsTests(unittest.TestCase):
    def test_impacts_add_up_to_total_change(self):
        _, report = apply_edits(KEYWORDS, MASTER, EDITS)
        self.assertEqual(report.before, 66.7)
        self.assertEqual(report.after, 80.0)
        impacts = [row.impact for row in report.rows]
        self.assertEqual(impacts, [13.3, 0.0])
        self.assertAlmostEqual(sum(impacts), round(report.after - report.before, 1), places=1)

    def test_section_comes_from_nearest_heading(self):
        _, report = apply_edits(KEYWORDS, MASTER, EDITS)
        self.assertEqual([row.section for row in report.rows], ["Experience", "Experience"])

    def test_gaps_are_the_missed_keywords(self):
        _, report = apply_edits(KEYWORDS, MASTER, EDITS)
        self.assertEqual(report.gaps, ["Terraform", "Leadership"])

    def test_edited_blocks_are_returned(self):
        edited, _ = apply_edits(KEYWORDS, MASTER, EDITS)
        self.assertEqual(edited[4].text, "Introduced CI/CD pipelines for all ETL repositories.")
        self.assertEqual(MASTER[4].text, "Introduced CI pipelines for all ETL repositories.")

    def test_identical_text_is_rejected(self):
        bad = [Edit(4, MASTER[4].text, "No-op", "None")]
        with self.assertRaises(ValueError):
            apply_edits(KEYWORDS, MASTER, bad)

    def test_out_of_range_index_is_rejected(self):
        bad = [Edit(99, "anything", "Bad", "None")]
        with self.assertRaises(ValueError):
            apply_edits(KEYWORDS, MASTER, bad)


class RenderTests(unittest.TestCase):
    def setUp(self):
        _, self.report = apply_edits(KEYWORDS, MASTER, EDITS)
        self.text = render_markdown(self.report)
        self.lines = self.text.splitlines()

    def test_header_line_states_before_after_and_change(self):
        self.assertEqual(
            self.lines[0],
            "**Keyword-match score:** 66.7% -> 80.0% (+13.3 points)",
        )

    def test_table_uses_fixed_columns(self):
        self.assertIn("| # | Section | Change | ATS impact | Why |", self.lines)
        self.assertIn(
            "| 1 | Experience | CI pipelines -> CI/CD pipelines | +13.3 | JD term; candidate did this work |",
            self.lines,
        )
        self.assertIn("| 2 | Experience | Added 'nightly' | 0.0 | Clearer scheduling detail |", self.lines)

    def test_gaps_are_listed(self):
        self.assertIn(
            "**Genuine gaps (not added, no supporting evidence):** Terraform, Leadership",
            self.lines,
        )

    def test_disclaimer_is_the_last_line(self):
        last_non_empty = [line for line in self.lines if line.strip()][-1]
        self.assertEqual(last_non_empty, f"*{DISCLAIMER}*")

    def test_no_edits_still_renders_a_row_and_disclaimer(self):
        _, report = apply_edits(KEYWORDS, MASTER, [])
        text = render_markdown(report)
        self.assertIn("| - | - | No edits were needed | - | - |", text.splitlines())
        self.assertTrue(text.rstrip().endswith(f"*{DISCLAIMER}*"))


if __name__ == "__main__":
    unittest.main()
