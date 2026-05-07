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
def check_formatting_hints(text, doc_type="project_2"):
    """
    Note: Full formatting (fonts, margins, spacing) can only be checked
    in .docx files. This checks what's detectable from plain text.
    """
    feedback = []
    text_lower = text.lower()
    is_internship = doc_type == "internship"

    # Chapter heading check
    chapter_matches = re.findall(r'chapter\s+\d+', text, re.IGNORECASE)
    lowercase_chapters = [c for c in chapter_matches if c == c.lower() and c[0].islower()]
    if lowercase_chapters:
        feedback.append({"type": "warning", "message": "Chapter headings lowercase detected. Use 16pt Bold — 'Chapter 1: Introduction'."})
    else:
        feedback.append({"type": "info", "message": "Formatting reminder: Times New Roman | Chapter: 16pt Bold Center | Section: 14pt Bold Left | Sub-section: 12pt Bold | Body: 12pt Justified."})

    # Margins
    feedback.append({"type": "info", "message": "Margin: Left=1.25\" (35mm), Right=Top=Bottom=1.0\". Verify in Word document."})

    # Page numbering
    feedback.append({"type": "info", "message": "Page numbering: Roman (i,ii,iii) front matter → Arabic (1,2,3) from Chapter 1. Position: Bottom Center."})

    # Citation check — APA for internship, IEEE for others
    has_references = "references" in text_lower

    if is_internship:
        apa_found = bool(re.search(
            r'([A-Z][a-zA-Z]+[\.,]\s*\(?\d{4}|'   # Author. (2024)
            r'[A-Z][a-zA-Z]+[\.,]\s*\(?n\.d\.|'   # Author. (n.d.)
            r'\([A-Z][a-zA-Z]+,\s*\d{4}\)|'       # (Author, 2024)
            r'\([A-Z][a-zA-Z]+,\s*n\.d\.\))',     # (Author, n.d.)
            text
        ))
        if has_references and apa_found:
            feedback.append({"type": "success", "message": "References section with APA citations detected ✓"})
        elif has_references and not apa_found:
            feedback.append({"type": "error", "message": "References found but no APA citations detected. Internship requires APA format: (Author, Year)."})
        else:
            feedback.append({"type": "error", "message": "References section missing. APA referencing mandatory for internship report."})
    else:
        has_ieee = bool(re.search(r'\[\d+\]', text))
        if has_references and has_ieee:
            feedback.append({"type": "success", "message": "References section with IEEE citations detected ✓"})
        elif has_references and not has_ieee:
            feedback.append({"type": "error", "message": "References found but no IEEE citations [1],[2] detected. Format: [1] Author, 'Title', Journal, vol., pp., year."})
        else:
            feedback.append({"type": "error", "message": "References section missing. IEEE referencing mandatory. Binding: Golden Embracing with Black Cover. Copies: 3."})

    # Appendices
    if not is_internship:
        if "appendix" not in text_lower and "appendices" not in text_lower:
            feedback.append({"type": "warning", "message": "Appendices not detected. Should include: screenshots, source code, supervisor visit log."})
    else:
        feedback.append({"type": "info", "message": "Internship appendices: Screen shots + Source codes (optional but recommended)."})

    # Figures
    if re.search(r'figure\s+\d+', text_lower):
        feedback.append({"type": "info", "message": "Figures detected. Caption: centered BELOW figure. Table caption: centered ABOVE. Both 12pt Bold."})

    return {"formatting_hints": feedback}