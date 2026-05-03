import re

SECTION_WORD_LIMITS = {
    "abstract": {
        "min": 150, "max": 300,
        "note": "TU guideline: 150-300 words"
    },
    "introduction": {
        "min": 500, "max": 1500,
        "note": "Should cover background, objectives, scope & limitations"
    },
    "background study": {
        "min": 200, "max": 1000,
        "note": "Cover fundamental concepts related to your project"
    },
    "literature review": {
        "min": 300, "max": 1500,
        "note": "Review similar systems/papers with citations [1],[2]..."
    },
    "system analysis": {
        "min": 300, "max": 2000,
        "note": "Include diagrams + descriptions"
    },
    "methodology": {
        "min": 200, "max": 1500,
        "note": "Development approach clearly stated"
    },
    "implementation": {
        "min": 300, "max": 2000,
        "note": "Module-by-module description with screenshots"
    },
    "conclusion": {
        "min": 150, "max": 700,
        "note": "Summarize achievements + future scope"
    },
    "future recommendations": {
        "min": 80, "max": 500,
        "note": "Realistic future improvements"
    },
}

# Section end markers — yo section dekhinasamma content lini rakhne
SECTION_END_MARKERS = {
    "abstract": ["chapter 1", "introduction", "acknowledgement", "table of"],
    "introduction": ["chapter 2", "background study", "literature review"],
    "background study": ["literature review", "2.2", "chapter 3"],
    "literature review": ["chapter 3", "system analysis", "3.1"],
    "system analysis": ["chapter 4", "implementation", "4.1"],
    "methodology": ["chapter 3", "system analysis", "chapter 4"],
    "implementation": ["testing", "4.2", "chapter 5"],
    "conclusion": ["future recommendation", "5.2", "5.3", "references"],
    "future recommendations": ["references", "bibliography", "appendix"],
}


def count_words(text):
    return len(text.strip().split()) if text.strip() else 0


def extract_section_text(full_text, section_keyword, end_markers=None):
    """
    Improved: handles '2.1 Background Study', '2.2 Literature Review' prefixes.
    """
    text_lower = full_text.lower()
    keyword_lower = section_keyword.lower()

    # TOC ma short match hunxa — skip garnu parxa
    # Actual content = keyword pachhi minimum 100 chars content hunu parxa
    idx = -1
    search_start = 0

    while True:
        found = text_lower.find(keyword_lower, search_start)
        if found == -1:
            break

        # Check: yo TOC entry ho ki actual content?
        # TOC entry ma keyword pachhi page number (digits) hunchha
        after = text_lower[found + len(keyword_lower): found + len(keyword_lower) + 30]
        after_stripped = after.strip()

        # TOC entry skip garne — e.g. "introduction .... 1"
        is_toc = bool(re.match(r'^[\s\.…]{0,10}\d+\s*$', after_stripped))
        if is_toc:
            search_start = found + 1
            continue

        # Actual content — minimum 100 words pachhi hunu parxa
        sample_check = full_text[found: found + 500]
        if len(sample_check.split()) > 30:
            idx = found
            break

        search_start = found + 1

    # Fallback: numbered prefix try — "1.1 introduction", "chapter 1"
    if idx == -1:
        patterns = [
            r'\d+\.\d+\s+' + re.escape(keyword_lower),
            r'chapter\s+\d+[:\s]+' + re.escape(keyword_lower),
        ]
        for pat in patterns:
            m = re.search(pat, text_lower)
            if m:
                idx = m.start()
                break

    if idx == -1:
        return None

    # End boundary — TOC entries skip garxa
    end_idx = min(len(full_text), idx + 15000)
    if end_markers:
        for marker in end_markers:
            search_pos = idx + len(keyword_lower) + 200  # minimum 200 chars skip
            while True:
                next_idx = text_lower.find(marker.lower(), search_pos)
                if next_idx == -1:
                    break

                # TOC entry ho bhane skip
                after = text_lower[next_idx + len(marker): next_idx + len(marker) + 30]
                after_stripped = after.strip()
                is_toc = bool(re.match(r'^[\s\.…]{0,10}\d+\s*$', after_stripped))

                if is_toc:
                    search_pos = next_idx + 1
                    continue

                # Real section heading — cut here
                if next_idx < end_idx:
                    end_idx = next_idx
                break

    return full_text[idx:end_idx]

def check_wordcount(text):
    results = []
    total_words = count_words(text)

    for section, limits in SECTION_WORD_LIMITS.items():
        end_markers = SECTION_END_MARKERS.get(section, ["chapter"])
        sample = extract_section_text(text, section, end_markers)

        if sample is None:
            continue

        wc = count_words(sample)

        if wc < limits["min"]:
            # Suggestion only — not error
            results.append({
                "type": "info",  # ← warning bata info ma change
                "section": section.title(),
                "message": (
                    f"{section.title()}: ~{wc} words detected. "
                    f"Suggested minimum: {limits['min']} words. "
                    f"{limits['note']}"
                ),
            })
        elif wc > limits["max"]:
            results.append({
                "type": "info",  # ← error hoina, just suggestion
                "section": section.title(),
                "message": (
                    f"{section.title()}: ~{wc} words — slightly long. "
                    f"Consider keeping under {limits['max']} words for conciseness."
                ),
            })
        else:
            results.append({
                "type": "success",
                "section": section.title(),
                "message": f"{section.title()}: ~{wc} words — within suggested range ✓",
            })

    return {
        "total_words": total_words,
        "section_results": results,
    }