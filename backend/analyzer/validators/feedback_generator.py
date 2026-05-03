import re

# ============================================================
# SECTION CONTENT GUIDES
# K k lekhnu parxa har section ma
# ============================================================
SECTION_GUIDES = {
    "cover page": {
        "title": "Cover Page",
        "must_contain": [
            "Tribhuvan University",
            "Faculty of Humanities and Social Sciences",
            "Title of Project Report",
            "A PROJECT REPORT",
            "Submitted to: Department of Computer Application",
            "College Name",
            "In partial fulfillment of the requirements for BCA",
            "Submitted by: Full Name, Exam Roll No., TU Regd. No.",
            "Month and Year",
            "Under the Supervision of: Supervisor Name",
        ],
        "tip": "Cover page ma college ko official format exactly follow garnu parxa. Golden binding with black cover."
    },
    "abstract": {
        "title": "Abstract",
        "must_contain": [
            "Background / Problem context (1-2 sentences)",
            "Objectives of the project (what was aimed to achieve)",
            "Methodology / Development approach used",
            "Key results and findings",
            "Conclusion (1-2 sentences)",
        ],
        "word_limit": "150-300 words",
        "tip": "Abstract should be self-contained. Reader le abstract matra padera project bujhnu saknu parxa.",
        "template": """This project presents [system name], a [type of application] developed to [solve what problem].
The main objectives of this study are to [list objectives briefly].
The system was developed using [technologies] following [methodology e.g., waterfall/agile].
[Key feature] was implemented to [achieve what].
The system was tested using [testing method] and the results indicate [key findings].
The developed system successfully [conclusion statement]."""
    },
    "introduction": {
        "title": "Chapter 1: Introduction",
        "must_contain": [
            "1.1 Introduction — Background of the study domain",
            "1.2 Problem Statement — Specific problem being solved",
            "1.3 Objectives — General and specific objectives",
            "1.4 Scope and Limitation — What is and isn't covered",
            "1.5 Development Methodology — SDLC model used",
            "1.6 Report Organization — Brief description of each chapter",
        ],
        "word_limit": "800-1500 words",
        "tip": "Introduction le reader lai project ko full picture dinu parxa. Problem clearly define gara."
    },
    "background study": {
        "title": "2.1 Background Study",
        "must_contain": [
            "Fundamental theories related to the project domain",
            "General concepts and terminologies used",
            "Existing technologies / platforms relevant to the project",
            "Cited references [1], [2] for each concept",
        ],
        "tip": "Basic definitions avoid gara. Project sanga directly related concepts matra lekhnu parxa."
    },
    "literature review": {
        "title": "2.2 Literature Review",
        "must_contain": [
            "Minimum 5 related works / similar systems reviewed",
            "Each review: Author name [citation], system name, approach, findings, limitation",
            "Comparison table of reviewed systems (optional but good)",
            "Gap identification — what your project addresses that others didn't",
        ],
        "tip": "Format: '[1] Author et al. proposed a system that... The limitation of this system is...'"
    },
    "system analysis": {
        "title": "Chapter 3: System Analysis and Design",
        "must_contain": [
            "3.1.1 Functional Requirements (Use case diagram + descriptions)",
            "3.1.2 Non-functional Requirements (performance, security, etc.)",
            "3.1.3 Feasibility Analysis (Technical, Operational, Economic)",
            "3.1.4 Data/Object Modelling (ER diagram or Class diagram)",
            "3.1.5 Process Modelling (DFD or Activity diagram)",
            "3.2 System Design (Architectural, Database schema, Interface design)",
        ],
        "tip": "Proj I/II: Structured approach (ER+DFD). Proj III: OO approach (Class+Sequence+Activity diagrams)."
    },
    "implementation": {
        "title": "4.1 Implementation",
        "must_contain": [
            "4.1.1 Tools Used — programming language, framework, database, CASE tools",
            "4.1.2 Module-by-module description",
            "Each module: purpose, key functions/classes, code snippets (important parts only)",
            "Screenshots of implemented interfaces",
        ],
        "tip": "Avoid dumping all source code. Describe key algorithms and module logic only."
    },
    "testing": {
        "title": "4.2 Testing",
        "must_contain": [
            "4.2.1 Unit Testing — test cases for individual modules/functions",
            "4.2.2 System Testing — end-to-end test cases",
            "Test case table: Test Case ID | Description | Input | Expected Output | Actual Output | Status",
        ],
        "tip": "Minimum 5 unit test cases ra 5 system test cases include gara."
    },
    "conclusion": {
        "title": "Chapter 5: Conclusion",
        "must_contain": [
            "5.1 Conclusion — Summary of what was achieved",
            "5.2 Lesson Learnt / Outcome — Skills and knowledge gained",
            "5.3 Future Recommendations — Specific improvements possible",
        ],
        "word_limit": "300-600 words",
        "tip": "Conclusion ma new information nalekhnu. Achievements summarize gara ra future scope realistic rakha."
    },
    "references": {
        "title": "References (IEEE Format)",
        "must_contain": [
            "All sources cited in the document must be listed",
            "IEEE format: [1] A. Author, 'Title of paper,' Journal Name, vol. X, no. Y, pp. ZZ-ZZ, Year.",
            "For websites: [1] A. Author, 'Page title,' Website Name. [Online]. Available: URL. [Accessed: Month DD, YYYY].",
            "Minimum 8-10 references for Project II, 10-15 for Project III",
        ],
        "tip": "References list alphabetically by citation number [1], [2], [3]... not by author name."
    },
}

# ============================================================
# PASSIVE VOICE SUGGESTIONS
# First person → passive/third person
# ============================================================
PASSIVE_SUGGESTIONS = {
    r'\bI developed\b': 'The system was developed',
    r'\bI implemented\b': 'The implementation was carried out',
    r'\bI used\b': 'The study employed',
    r'\bI created\b': 'The application was created',
    r'\bI designed\b': 'The design was formulated',
    r'\bI analyzed\b': 'An analysis was conducted',
    r'\bI tested\b': 'Testing was performed',
    r'\bwe developed\b': 'The system was developed',
    r'\bwe implemented\b': 'The implementation was carried out',
    r'\bwe used\b': 'The study employed',
    r'\bwe created\b': 'The application was created',
    r'\bwe designed\b': 'The design was formulated',
    r'\bwe found\b': 'The findings indicate',
    r'\bwe tested\b': 'Testing was conducted',
    r'\bour system\b': 'The developed system',
    r'\bour project\b': 'The proposed project',
    r'\bour application\b': 'The developed application',
    r'\bmy project\b': 'The project',
}

INFORMAL_REPLACEMENTS = {
    'gonna': 'going to',
    'wanna': 'want to',
    'kinda': 'somewhat',
    'sort of': 'to some extent',
    'kind of': 'to some extent',
    'stuff': 'components / elements',
    'things': 'components / aspects',
    'a lot': 'numerous / significant',
    'lots of': 'numerous',
    'really': 'significantly / considerably',
    'basically': 'fundamentally / essentially',
    'literally': 'precisely',
    'awesome': 'highly effective',
    'cool': 'efficient',
    'nice': 'appropriate',
    'great': 'significant',
    'easy': 'straightforward / simplified',
    'hard': 'challenging / complex',
    'simple': 'straightforward',
    'just': '[remove or rephrase]',
    'pretty much': 'largely / primarily',
    'you know': '[remove]',
}


def extract_problematic_sentences(text, patterns):
    """Find sentences containing problematic patterns."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    problematic = []
    for sent in sentences:
        sent = sent.strip()
        if not sent or len(sent) < 10:
            continue
        for pattern in patterns:
            if re.search(pattern, sent, re.IGNORECASE):
                problematic.append(sent[:150])
                break
    return problematic[:5]  # max 5 examples


def generate_passive_fixes(text):
    """Find first-person sentences and suggest passive voice fixes."""
    first_person_patterns = [
        r'\bI\b', r'\bwe\b', r'\bour\b', r'\bmy\b'
    ]
    sentences = re.split(r'(?<=[.!?])\s+', text)
    fixes = []

    for sent in sentences:
        sent = sent.strip()
        if not sent or len(sent) < 10:
            continue

        has_first_person = any(
            re.search(p, sent) for p in first_person_patterns
        )
        if not has_first_person:
            continue

        # Try to auto-suggest fix
        fixed = sent
        for pattern, replacement in PASSIVE_SUGGESTIONS.items():
            fixed = re.sub(pattern, replacement, fixed, flags=re.IGNORECASE)

        if fixed != sent:
            fixes.append({
                "original": sent[:120],
                "suggested": fixed[:120]
            })
        else:
            fixes.append({
                "original": sent[:120],
                "suggested": "Rewrite using passive voice. E.g., 'I did X' → 'X was performed / The system performs X'"
            })

        if len(fixes) >= 4:
            break

    return fixes


def generate_informal_fixes(text):
    """Find informal words and suggest formal replacements."""
    text_lower = text.lower()
    fixes = []

    for informal, formal in INFORMAL_REPLACEMENTS.items():
        if informal in text_lower:
            # Find example sentence
            idx = text_lower.find(informal)
            start = max(0, idx - 60)
            end = min(len(text), idx + 80)
            context = text[start:end].replace('\n', ' ').strip()
            fixes.append({
                "word": informal,
                "replace_with": formal,
                "context": f"...{context}..."
            })
            if len(fixes) >= 5:
                break

    return fixes


def generate_section_feedback(missing_sections, found_sections, text):
    """For each missing section, provide detailed content guide."""
    feedback = []

    for section in missing_sections[:8]:  # limit to 8
        guide = SECTION_GUIDES.get(section.lower())
        if guide:
            feedback.append({
                "section": guide["title"],
                "status": "missing",
                "must_contain": guide["must_contain"],
                "tip": guide.get("tip", ""),
                "word_limit": guide.get("word_limit", ""),
                "template": guide.get("template", ""),
            })
        else:
            feedback.append({
                "section": section.title(),
                "status": "missing",
                "must_contain": [f"Add '{section}' section as per TU FOHSS guidelines"],
                "tip": "",
            })

    return feedback


def generate_wordcount_feedback(wordcount_results):
    """Add specific suggestions for short sections."""
    enhanced = []
    for result in wordcount_results:
        enhanced_result = dict(result)
        section_lower = result['section'].lower()

        if result['type'] == 'warning' and 'short' in result['message'].lower():
            guide = SECTION_GUIDES.get(section_lower)
            if guide:
                enhanced_result['how_to_fix'] = guide.get('must_contain', [])
                enhanced_result['tip'] = guide.get('tip', '')
            else:
                enhanced_result['how_to_fix'] = [
                    f"Expand the {result['section']} section with more detailed content",
                    "Add citations and references to support your points",
                    "Include relevant diagrams and their descriptions",
                ]

        enhanced.append(enhanced_result)
    return enhanced