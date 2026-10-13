"""Change log for an optimized resume.

Edits are applied one at a time in the order given. Each edit's ATS impact is
the change in keyword-match score it causes, measured against the score just
before that edit. Impacts therefore depend on order; the report says so.

render_markdown() produces the fixed template every target shows to the user.
"""

from dataclasses import dataclass

from docx_io import Block
from score import score_resume

DISCLAIMER = (
    "Disclaimer: the ATS algorithm used by the target company may be different "
    "from the keyword-match logic used in this report. The scores here are a "
    "proxy for keyword coverage and do not predict the result in any specific ATS."
)

ORDER_NOTE = (
    "Impact is measured in the order the edits were applied, so it can change "
    "if the order changes. Values are rounded to one decimal place."
)


@dataclass(frozen=True)
class Edit:
    block_index: int
    new_text: str
    change: str  # short description of what changed
    why: str  # one-line reason


@dataclass(frozen=True)
class ChangeRow:
    number: int
    section: str
    change: str
    impact: float  # keyword-match points, signed
    why: str


@dataclass(frozen=True)
class ChangeReport:
    before: float
    after: float
    rows: list
    gaps: list


def _section_for(blocks, index):
    for position in range(index, -1, -1):
        if blocks[position].kind == "heading":
            return blocks[position].text
    return "Top of resume"


def apply_edits(keywords, blocks, edits):
    """Apply edits and return (edited_blocks, ChangeReport).

    Raises ValueError for an out-of-range block index or an edit that does not
    change the text.
    """
    current = list(blocks)
    baseline = score_resume(keywords, _text(current)).exact
    previous = baseline
    rows = []
    for number, edit in enumerate(edits, start=1):
        if not 0 <= edit.block_index < len(current):
            raise ValueError(f"edit {number}: block index {edit.block_index} is out of range")
        original = current[edit.block_index]
        if original.text == edit.new_text:
            raise ValueError(f"edit {number}: new text is identical to the original")
        section = _section_for(current, edit.block_index)
        current[edit.block_index] = Block(original.kind, edit.new_text)
        after_edit = score_resume(keywords, _text(current))
        rows.append(
            ChangeRow(
                number=number,
                section=section,
                change=edit.change,
                impact=round(after_edit.exact - previous, 1),
                why=edit.why,
            )
        )
        previous = after_edit.exact

    final = score_resume(keywords, _text(current))
    report = ChangeReport(
        before=round(baseline, 1),
        after=final.score,
        rows=rows,
        gaps=final.missed,
    )
    return current, report


def _text(blocks):
    return "\n".join(b.text for b in blocks)


def _signed(value):
    if value == 0:
        return "0.0"
    return f"{value:+.1f}"


def render_markdown(report):
    """Render the fixed change-log template, ending with the disclaimer."""
    lines = [
        f"**Keyword-match score:** {report.before}% -> {report.after}% "
        f"({_signed(round(report.after - report.before, 1))} points)",
        "",
        "| # | Section | Change | ATS impact | Why |",
        "|---|---|---|---|---|",
    ]
    for row in report.rows:
        lines.append(
            f"| {row.number} | {row.section} | {row.change} | {_signed(row.impact)} | {row.why} |"
        )
    if not report.rows:
        lines.append("| - | - | No edits were needed | - | - |")
    lines += [
        "",
        f"*{ORDER_NOTE}*",
        "",
        "**Genuine gaps (not added, no supporting evidence):** "
        + (", ".join(report.gaps) if report.gaps else "none"),
        "",
        f"*{DISCLAIMER}*",
    ]
    return "\n".join(lines)
