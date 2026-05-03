import re

# Official TU FOHSS formatting standards
TU_FORMATTING_STANDARDS = {
    "font": "Times New Roman",
    "chapter_heading_size": 16,
    "section_heading_size": 14,
    "subsection_heading_size": 12,
    "body_size": 12,
    "line_spacing": 1.5,
    "alignment": "Justified",
    "margin_left_inches": 1.25,
    "margin_right_inches": 1.0,
    "margin_top_inches": 1.0,
    "margin_bottom_inches": 1.0,
    "page_size": "A4",
    "referencing": "IEEE",
    "page_num_front_matter": "Roman (i, ii, iii)",
    "page_num_body": "Arabic (1, 2, 3)",
    "page_num_position": "Bottom Center",
}

# Common formatting mistakes in plain text we can detect
def check_formatting_hints(text):
    """
    Note: Full formatting (fonts, margins, spacing) can only be checked
    in .docx files. This checks what's detectable from plain text.
    """
    feedback = []
    text_lower = text.lower()

    # Check: Chapter headings should not be in lowercase
    chapter_matches = re.findall(r'chapter\s+\d+', text, re.IGNORECASE)
    lowercase_chapters = [c for c in chapter_matches if c == c.lower() and c[0].islower()]
    if lowercase_chapters:
        feedback.append({
            "type": "warning",
            "message": (
                "Chapter headings detected in lowercase. "
                "Per TU standard: chapter titles should be formatted as 16pt Bold. "
                "E.g., 'CHAPTER 1: INTRODUCTION' or 'Chapter 1: Introduction' (title case)."
            ),
        })
    else:
        feedback.append({
            "type": "info",
            "message": (
                "Formatting reminder: Times New Roman required throughout. "
                "Chapter headings: 16pt Bold (Center). "
                "Section headings: 14pt Bold (Left). "
                "Sub-section: 12pt Bold. Body text: 12pt Regular (Justified)."
            ),
        })

    # Check: Margins reminder
    feedback.append({
        "type": "info",
        "message": (
            "Margin requirement: Left = 1.25 inch (35mm), Right = 1 inch (20mm), "
            "Top = 1 inch, Bottom = 1 inch. Verify in your Word document."
        ),
    })

    # Check: Page numbering
    feedback.append({
        "type": "info",
        "message": (
            "Page numbering: Roman numerals (i, ii, iii) from Certificate page to List of Tables/Figures. "
            "Arabic numerals (1, 2, 3) from Chapter 1 onwards. Position: Bottom Center."
        ),
    })

    # Check: IEEE references section
    has_references = "references" in text_lower
    has_ieee_bracket = bool(re.search(r'\[\d+\]', text))

    if has_references and has_ieee_bracket:
        feedback.append({
            "type": "success",
            "message": "References section present with IEEE-style citations detected.",
        })
    elif has_references and not has_ieee_bracket:
        feedback.append({
            "type": "error",
            "message": (
                "References section found but no IEEE citation format [1], [2] detected. "
                "TU FOHSS mandates IEEE referencing. Format: [1] Author, 'Title', Journal, vol., pp., year."
            ),
        })
    else:
        feedback.append({
            "type": "error",
            "message": (
                "References section missing. IEEE referencing is mandatory for all TU BCA projects. "
                "Submission copies: 3 (College Library + Self + Dean Office). "
                "Binding: Golden Embracing with Black Binding."
            ),
        })

    # Check: Appendices
    if "appendix" not in text_lower and "appendices" not in text_lower:
        feedback.append({
            "type": "warning",
            "message": (
                "Appendices section not detected. "
                "Should include: screenshots, source code excerpts, supervisor visit log sheets."
            ),
        })

    # Check: Figure/Table captions pattern
    if re.search(r'figure\s+\d+', text_lower):
        feedback.append({
            "type": "info",
            "message": (
                "Figures detected. Reminder: Figure captions must be centered BELOW the figure. "
                "Table captions must be centered ABOVE the table. Both in 12pt Bold."
            ),
        })

    return {"formatting_hints": feedback}