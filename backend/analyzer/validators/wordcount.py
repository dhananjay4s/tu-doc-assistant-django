import re

SECTION_WORD_LIMITS = {
    "abstract": {"min": 150, "max": 300, "note": "TU guideline: 150-300 words"},
    "introduction": {"min": 500, "max": 1500, "note": "Should cover background, objectives, scope & limitations"},
    "background study": {"min": 200, "max": 1000, "note": "Cover fundamental concepts related to your project"},
    "literature review": {"min": 300, "max": 1500, "note": "Review similar systems/papers with citations [1],[2]..."},
    "system analysis": {"min": 300, "max": 2000, "note": "Include diagrams + descriptions"},
    "methodology": {"min": 200, "max": 1500, "note": "Development approach clearly stated"},
    "implementation": {"min": 300, "max": 2000, "note": "Module-by-module description with screenshots"},
    "conclusion": {"min": 150, "max": 700, "note": "Summarize achievements + future scope"},
    "future recommendations": {"min": 80, "max": 500, "note": "Realistic future improvements"},
}


def count_words(text):
    return len(text.strip().split()) if text.strip() else 0


def extract_section_text(full_text, section_keyword, end_markers=None):
    text_lower = full_text.lower()
    keyword_lower = section_keyword.lower()

    idx = -1
    search_start = 0

    while True:
        found = text_lower.find(keyword_lower, search_start)
        if found == -1:
            break

        after = text_lower[found + len(keyword_lower): found + len(keyword_lower) + 30]
        after_stripped = after.strip()
        is_toc = bool(re.match(r'^[\s\.…]{0,10}\d+\s*$', after_stripped))
        if is_toc:
            search_start = found + 1
            continue

        sample_check = full_text[found: found + 500]
        if len(sample_check.split()) > 30:
            idx = found
            break

        search_start = found + 1

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

    end_idx = min(len(full_text), idx + 15000)
    if end_markers:
        for marker in end_markers:
            search_pos = idx + len(keyword_lower) + 200
            while True:
                next_idx = text_lower.find(marker.lower(), search_pos)
                if next_idx == -1:
                    break
                after = text_lower[next_idx + len(marker): next_idx + len(marker) + 30]
                is_toc = bool(re.match(r'^[\s\.…]{0,10}\d+\s*$', after.strip()))
                if is_toc:
                    search_pos = next_idx + 1
                    continue
                if next_idx < end_idx:
                    end_idx = next_idx
                break

    return full_text[idx:end_idx]


def check_wordcount(text, doc_type="project_2"):

    PROJECT_MARKERS = {
        "abstract": ["chapter 1", "introduction", "table of"],
        "introduction": ["chapter 2", "background study", "literature review"],
        "background study": ["literature review", "2.2", "chapter 3"],
        "literature review": ["chapter 3", "system analysis", "3.1"],
        "system analysis": ["chapter 4", "implementation", "4.1"],
        "methodology": ["chapter 3", "system analysis", "chapter 4"],
        "implementation": ["testing", "4.2", "chapter 5"],
        "conclusion": ["future recommendation", "5.2", "references"],
        "future recommendations": ["references", "bibliography", "appendix"],
    }

    INTERNSHIP_MARKERS = {
        "abstract": ["chapter 1", "introduction", "table of"],
        "introduction": ["chapter 2", "organization", "2.1"],
        "organization details": ["background study", "literature review", "chapter 3", "3.1"],
        "background study": ["literature review", "3.2", "chapter 4"],
        "literature review": ["chapter 4", "internship activities", "roles", "4.1"],
        "roles and responsibilities": ["weekly log", "4.2"],
        "weekly log": ["description of project", "tasks", "4.3"],
        "conclusion": ["learning outcome", "5.2", "references"],
        "learning outcome": ["references", "bibliography", "appendix"],
    }

    INTERNSHIP_LIMITS = {
        "abstract": {"min": 150, "max": 300, "note": "Executive summary of internship work"},
        "introduction": {"min": 300, "max": 800, "note": "Introduce internship project/work done"},
        "organization details": {"min": 200, "max": 600, "note": "Company info, hierarchy, working domains"},
        "background study": {"min": 200, "max": 800, "note": "Fundamental concepts related to internship"},
        "literature review": {"min": 200, "max": 800, "note": "Similar projects/theories reviewed"},
        "roles and responsibilities": {"min": 150, "max": 500, "note": "Your role during internship"},
        "weekly log": {"min": 300, "max": 1500, "note": "Week-by-week technical activities"},
        "conclusion": {"min": 150, "max": 500, "note": "Summarize internship experience"},
        "learning outcome": {"min": 100, "max": 400, "note": "Skills and knowledge gained"},
    }

    if doc_type == "internship":
        limits = INTERNSHIP_LIMITS
        markers = INTERNSHIP_MARKERS
    else:
        limits = SECTION_WORD_LIMITS
        markers = PROJECT_MARKERS

    results = []
    total_words = count_words(text)

    for section, lim in limits.items():
        end_markers = markers.get(section, ["chapter"])
        sample = extract_section_text(text, section, end_markers)

        if sample is None:
            continue

        wc = count_words(sample)

        if wc < lim["min"]:
            results.append({
                "type": "info",
                "section": section.title(),
                "message": f"{section.title()}: ~{wc} words. Suggested minimum: {lim['min']} words. {lim['note']}",
            })
        elif wc > lim["max"]:
            results.append({
                "type": "info",
                "section": section.title(),
                "message": f"{section.title()}: ~{wc} words — slightly long. Consider keeping under {lim['max']} words.",
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