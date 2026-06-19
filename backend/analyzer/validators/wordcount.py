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

    # All positions find
    all_positions = []
    start = 0
    while True:
        pos = text_lower.find(keyword_lower, start)
        if pos == -1:
            break
        all_positions.append(pos)
        start = pos + 1

    if not all_positions:
        # Numbered prefix fallback
        patterns = [
            r'\d+\.\d+\s+' + re.escape(keyword_lower),
            r'chapter\s*[-–]?\s*\d+[:\s]+' + re.escape(keyword_lower),
        ]
        for pat in patterns:
            m = re.search(pat, text_lower)
            if m:
                all_positions.append(m.start())
                break

    if not all_positions:
        return None

    # Best position — TOC skip, actual chapter heading find
    idx = -1
    for pos in all_positions:
        after = text_lower[pos + len(keyword_lower): pos + len(keyword_lower) + 80]
        after_clean = after.strip()

        # TOC entry patterns
        toc_patterns = [
            r'^[\s\.…\-]{0,20}\d+\s*$',
            r'^[\s\.…\-]{0,20}\d+\s*\n',
            r'^\s*\d{1,3}\s*$',
            r'^[\s\.]{3,}\d+',
        ]
        is_toc = any(re.match(p, after_clean) for p in toc_patterns)

        # Before keyword — dots/spaces = TOC
        if not is_toc:
            before = text_lower[max(0, pos - 60):pos]
            if re.search(r'\.{3,}|\s{8,}', before):
                is_toc = True

        if is_toc:
            continue

        # Valid — must have real content after (not just injected keywords)
        ahead = full_text[pos: pos + 300]
        real_words = [w for w in ahead.split() 
                     if len(w) > 2 and w.lower() not in 
                     ['the', 'and', 'for', 'are', 'was', 'page', 'cover', 'title']]
        if len(real_words) < 15:
            continue

        idx = pos
        break

    # Fallback — last position
    if idx == -1 and all_positions:
    # First non-TOC position khoj  ← indent fix
        for pos in all_positions:
            ahead = full_text[pos: pos + 200]
            if len(ahead.split()) > 20:
                idx = pos
                break
        if idx == -1:
            idx = all_positions[0]

    # Smart end boundary
    end_idx = min(len(full_text), idx + 12000)

    if end_markers:
        for marker in end_markers:
            search_pos = idx + len(keyword_lower) + 100
            while search_pos < end_idx:
                next_pos = text_lower.find(marker.lower(), search_pos)
                if next_pos == -1:
                    break

                # TOC skip
                after = text_lower[next_pos + len(marker): next_pos + len(marker) + 80]
                after_clean = after.strip()
                toc_patterns = [
                    r'^[\s\.…\-]{0,20}\d+\s*$',
                    r'^[\s\.]{3,}\d+',
                ]
                is_toc = any(re.match(p, after_clean) for p in toc_patterns)

                if not is_toc:
                    before = text_lower[max(0, next_pos - 60): next_pos]
                    if re.search(r'\.{3,}|\s{8,}', before):
                        is_toc = True

                if is_toc:
                    search_pos = next_pos + 1
                    continue

                if next_pos < end_idx:
                    end_idx = next_pos
                break

    extracted = full_text[idx:end_idx]

    # Abstract specific — injected keywords hatau
    # "abstract\ncover page\ntitle page\n..." jasto injected content skip
    if keyword_lower == "abstract":
        
        lines = extracted.split('\n')
        real_lines = []
        inject_kws = [
            'cover page', 'title page', 'table of contents',
            'submitted by', 'tribhuvan university', 'acknowledgement',
            'list of figures', 'list of tables', 'list of abbreviations',
        ]
        for line in lines:
            line_lower = line.lower().strip()
            if any(kw in line_lower for kw in inject_kws):
                continue  # injected content skip

            # "keywords:" line pachhi skip
            if line_lower.startswith('keyword'):
                break
            real_lines.append(line)
        extracted = '\n'.join(real_lines)

    if len(extracted.split()) < 5:
        return None

    return extracted


def check_wordcount(text, doc_type="project_2"):

    PROJECT_MARKERS = {
        "abstract": [
            "acknowledgement", "acknowledgment",
            "table of contents", "chapter 1",
        ],
        "introduction": [
            "chapter 2", "background study",
            "2.1 background",
        ],
        "background study": [
            "literature review", "2.2 literature",
            "related work",
        ],
        "literature review": [
            "chapter 3", "system analysis",
            "3. system", "3.1",
        ],
        "system analysis": [
            "chapter 4", "implementation", "4.1",
        ],
        "methodology": [
            "chapter 3", "system analysis", "chapter 4",
        ],
        "implementation": [
            "testing", "4.2", "chapter 5",
        ],
        "conclusion": [
            "future recommendation", "5.2",
            "5.3", "references",
        ],
        "future recommendations": [
            "references", "bibliography", "appendix",
        ],
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
            # print(f"DEBUG [{section}]: NOT FOUND")
            continue

        wc = count_words(sample)
        # print(f"DEBUG [{section}]: {wc} words | sample: {sample[:100].strip()}")

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