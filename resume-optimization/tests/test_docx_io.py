import hashlib
import os
import sys
import tempfile
import unittest
import zipfile

CORE_DIR = os.path.join(os.path.dirname(__file__), "..", "skills", "ats-resume-optimizer", "core")
sys.path.insert(0, os.path.abspath(CORE_DIR))

import docx_io  # noqa: E402
from docx import Document  # noqa: E402
from docx_io import Block, UnreadableResumeError  # noqa: E402


def make_text_pdf(path, lines):
    """Write a minimal single-page PDF whose text layer holds the given lines.

    Pass an empty list for a page with no text layer (a stand-in for a scan).
    """
    stream_parts = ["BT", "/F1 11 Tf", "14 TL", "50 750 Td"]
    for line in lines:
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream_parts.append(f"({escaped}) Tj T*")
    stream_parts.append("ET")
    stream = "\n".join(stream_parts).encode("latin-1")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 5 0 R /Resources << /Font << /F1 4 0 R >> >> >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"
    xref_at = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_at}\n%%EOF\n"
    ).encode()
    with open(path, "wb") as f:
        f.write(bytes(out))


class RoundTripTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_written_headings_survive_round_trip(self):
        blocks = [
            Block("heading", "Summary"),
            Block("paragraph", "Data engineer with six years of pipelines."),
            Block("heading", "Experience"),
            Block("bullet", "Built deployment pipelines on Kubernetes."),
            Block("heading", "Skills"),
            Block("paragraph", "Python, SQL"),
        ]
        path = os.path.join(self.tmp.name, "out.docx")
        docx_io.write_resume_docx(path, blocks)
        read_back = docx_io.read_resume(path)
        headings = [b.text for b in read_back if b.kind == "heading"]
        self.assertEqual(headings, ["Summary", "Experience", "Skills"])
        self.assertIn(Block("bullet", "Built deployment pipelines on Kubernetes."), read_back)

    def test_unsupported_extension_is_rejected(self):
        path = os.path.join(self.tmp.name, "resume.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("Summary and experience text that is long enough to pass")
        with self.assertRaises(ValueError):
            docx_io.read_resume(path)


class TemplateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_generated_file_has_no_tables_text_boxes_or_images(self):
        blocks = [
            Block("heading", "Experience"),
            Block("bullet", "Led a team of four engineers."),
        ]
        path = os.path.join(self.tmp.name, "template.docx")
        docx_io.write_resume_docx(path, blocks)

        document = Document(path)
        self.assertEqual(len(document.tables), 0)
        self.assertEqual(len(document.inline_shapes), 0)

        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        self.assertNotIn("txbxContent", xml)
        self.assertNotIn("<w:drawing", xml)
        self.assertNotIn("<w:pict", xml)


class OutputRulesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_file_name_uses_underscores(self):
        self.assertEqual(
            docx_io.ats_filename("Jane Doe", "Data Engineer"),
            "Jane_Doe_Data_Engineer_ATS.docx",
        )

    def test_file_name_strips_path_characters(self):
        self.assertEqual(
            docx_io.ats_filename("Jane/Doe", "Data:Engineer"),
            "JaneDoe_DataEngineer_ATS.docx",
        )

    def test_file_name_needs_candidate_and_role(self):
        with self.assertRaises(ValueError):
            docx_io.ats_filename("   ", "Data Engineer")

    def test_master_is_unchanged_after_a_full_run(self):
        master = os.path.join(self.tmp.name, "master.docx")
        docx_io.write_resume_docx(
            master,
            [
                Block("heading", "Experience"),
                Block("bullet", "Built batch and streaming pipelines in Python for four product teams."),
            ],
        )
        with open(master, "rb") as f:
            before = hashlib.sha256(f.read()).hexdigest()

        out_dir = os.path.join(self.tmp.name, "out")
        os.makedirs(out_dir)
        blocks = docx_io.read_resume(master)
        written = docx_io.write_tailored_resume(master, out_dir, "Jane Doe", "Data Engineer", blocks)

        with open(master, "rb") as f:
            after = hashlib.sha256(f.read()).hexdigest()
        self.assertEqual(before, after)
        self.assertEqual(os.path.basename(written), "Jane_Doe_Data_Engineer_ATS.docx")
        self.assertTrue(os.path.exists(written))

    def test_refuses_to_write_over_the_master(self):
        master = os.path.join(self.tmp.name, "Jane_Doe_Data_Engineer_ATS.docx")
        docx_io.write_resume_docx(master, [Block("heading", "Experience")])
        with self.assertRaises(ValueError):
            docx_io.write_tailored_resume(master, self.tmp.name, "Jane Doe", "Data Engineer", [])


class PdfTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_text_pdf_yields_section_headers(self):
        path = os.path.join(self.tmp.name, "text.pdf")
        make_text_pdf(
            path,
            [
                "Jane Doe",
                "SUMMARY",
                "Data engineer with six years of batch and streaming pipelines.",
                "EXPERIENCE",
                "- Built pipeline deployments on k8s clusters",
            ],
        )
        blocks = docx_io.read_resume(path)
        headings = [b.text for b in blocks if b.kind == "heading"]
        self.assertEqual(headings, ["SUMMARY", "EXPERIENCE"])
        self.assertIn(Block("bullet", "Built pipeline deployments on k8s clusters"), blocks)

    def test_scanned_pdf_is_rejected_with_blocking_message(self):
        path = os.path.join(self.tmp.name, "scan.pdf")
        make_text_pdf(path, [])
        with self.assertRaises(UnreadableResumeError) as ctx:
            docx_io.read_resume(path)
        self.assertEqual(str(ctx.exception), docx_io.BLOCKING_MESSAGE)


if __name__ == "__main__":
    unittest.main()
