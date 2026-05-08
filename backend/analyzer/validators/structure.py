# TU FOHSS BCA — Official Section Templates
# Sources: TUCDC official PDFs + United College Guidelines 2024

TEMPLATES = {
    "project_1": {
        "name": "BCA Project I (CACS256) — 4th Semester",
        "code": "CACS256",
        "semester": "4th",
        "referencing": "IEEE",
        "required_sections": [
            "cover page",
            "title page",
            "supervisor's recommendation",
            "letter of approval",
            "abstract",
            "acknowledgement",
            "table of contents",
            "list of abbreviations",
            "list of figures",
            "list of tables",
            "chapter 1",
            "introduction",
            "problem statement",
            "objectives",
            "scope and limitation",
            "report organization",
            "chapter 2",
            "background study",
            "literature review",
            "chapter 3",
            "system analysis",
            "requirement analysis",
            "functional requirements",
            "non-functional requirements",
            "feasibility",
            "er diagram",
            "dfd",
            "system design",
            "architectural design",
            "database schema",
            "interface design",
            "chapter 4",
            "implementation",
            "tools used",
            "testing",
            "unit testing",
            "system testing",
            "chapter 5",
            "conclusion",
            "future recommendations",
            "references",
            "appendices",
        ],
        "optional_sections": ["bibliography"],
        "chapter_structure": {
            "chapter 1": [
                "1.1 Introduction",
                "1.2 Problem Statement",
                "1.3 Objectives",
                "1.4 Scope and Limitation",
                "1.5 Report Organization",
            ],
            "chapter 2": [
                "2.1 Background Study",
                "2.2 Literature Review",
            ],
            "chapter 3": [
                "3.1 System Analysis",
                "3.1.1 Requirement Analysis",
                "3.1.2 Feasibility Analysis",
                "3.1.3 Data Modelling (ER Diagram)",
                "3.1.4 Process Modelling (DFD)",
                "3.2 System Design",
                "3.2.1 Architectural Design",
                "3.2.2 Database Schema Design",
                "3.2.3 Interface Design",
                "3.2.4 Physical DFD",
            ],
            "chapter 4": [
                "4.1 Implementation",
                "4.1.1 Tools Used",
                "4.1.2 Implementation Details of Modules",
                "4.2 Testing",
                "4.2.1 Test Cases for Unit Testing",
                "4.2.2 Test Cases for System Testing",
            ],
            "chapter 5": [
                "5.1 Lesson Learnt / Outcome",
                "5.2 Conclusion",
                "5.3 Future Recommendations",
            ],
        },
    },

    "project_2": {
        "name": "BCA Project II (CAPJ356) — 6th Semester",
        "code": "CAPJ356",
        "semester": "6th",
        "referencing": "IEEE",
        "required_sections": [
            "cover page",
            "title page",
            "supervisor's recommendation",
            "letter of approval",
            "abstract",
            "acknowledgement",
            "table of contents",
            "list of abbreviations",
            "list of figures",
            "list of tables",
            "chapter 1",
            "introduction",
            "problem statement",
            "objectives",
            "scope and limitation",
            "development methodology",
            "report organization",
            "chapter 2",
            "background study",
            "literature review",
            "chapter 3",
            "system analysis",
            "requirement analysis",
            "functional requirements",
            "non-functional requirements",
            "feasibility",
            "system design",
            "architectural design",
            "database schema",
            "interface design",
            "chapter 4",
            "implementation",
            "tools used",
            "testing",
            "unit testing",
            "system testing",
            "chapter 5",
            "conclusion",
            "future recommendations",
            "references",
            "appendices",
        ],
        "optional_sections": ["bibliography", "algorithm details"],
        "chapter_structure": {
            "chapter 1": [
                "1.1 Introduction",
                "1.2 Problem Statement",
                "1.3 Objectives",
                "1.4 Scope and Limitation",
                "1.5 Development Methodology",
                "1.6 Report Organization",
            ],
            "chapter 2": [
                "2.1 Background Study",
                "2.2 Literature Review",
            ],
            "chapter 3": [
                "3.1 System Analysis",
                "3.1.1 Requirement Analysis",
                "3.1.2 Feasibility Analysis",
                "3.2 System Design",
                "3.3 Algorithm Details (if used)",
            ],
            "chapter 4": [
                "4.1 Implementation",
                "4.1.1 Tools Used",
                "4.1.2 Implementation Details of Modules",
                "4.2 Testing",
                "4.2.1 Test Cases for Unit Testing",
                "4.2.2 Test Cases for System Testing",
            ],
            "chapter 5": [
                "5.1 Conclusion",
                "5.2 Lesson Learnt / Outcome",
                "5.3 Future Recommendations",
            ],
        },
    },

    "internship": {
        "name": "BCA Internship Report (CAIN403) — 7th Semester",
        "code": "CAIN403",
        "semester": "7th",
        "referencing": "APA",  # ← IEEE HOINA, APA ho internship ma
        "required_sections": [
            # Preliminary
            "cover page",
            "title page",
            "mentor's recommendation",      # ← Company bata
            "supervisor's recommendation",  # ← College bata
            "letter of approval",           # ← Examiner approval
            "acknowledgement",
            "abstract",
            "table of contents",
            "list of abbreviations",
            "list of figures",
            "list of tables",
            # Main chapters
            "chapter 1",
            "introduction",
            "problem statement",
            "objectives",
            "scope and limitation",
            "report organization",
            "chapter 2",
            "organization details",
            "organizational hierarchy",
            "working domains",
            "intern department",
            "chapter 3",
            "background study",
            "literature review",
            "chapter 4",
            "roles and responsibilities",
            "weekly log",
            "tasks",
            "chapter 5",
            "conclusion",
            "learning outcome",
            "references",
        ],
        "optional_sections": [
            "bibliography",
            "appendices",
        ],
        "chapter_structure": {
            "chapter 1": [
                "1.1 Introduction",
                "1.2 Problem Statement",
                "1.3 Objectives",
                "1.4 Scope and Limitation",
                "1.5 Report Organization",
                # NOTE: No Development Methodology — internship ma chhaina
            ],
            "chapter 2": [
                "2.1 Organization Details",
                "2.2 Organizational Hierarchy",
                "2.3 Working Domains of Organization",
                "2.4 Description of Intern Department/Unit",
            ],
            "chapter 3": [
                "3.1 Background Study",
                "3.2 Literature Review",
            ],
            "chapter 4": [
                "4.1 Roles and Responsibilities",
                "4.2 Weekly Log (Technical Details)",
                "4.3 Description of Project(s) Involved",
                "4.4 Tasks / Activities Performed",
            ],
            "chapter 5": [
                "5.1 Conclusion",
                "5.2 Learning Outcome",
                # NOTE: Future Recommendations chhaina internship ma
            ],
        },
    },

    "project_3": {
        "name": "BCA Project III (CACS452) — 8th Semester",
        "code": "CACS452",
        "semester": "8th",
        "referencing": "IEEE",
        "required_sections": [
            "cover page",
            "title page",
            "supervisor's recommendation",
            "letter of approval",
            "abstract",
            "acknowledgement",
            "table of contents",
            "list of abbreviations",
            "list of figures",
            "list of tables",
            "chapter 1",
            "introduction",
            "problem statement",
            "objectives",
            "scope and limitation",
            "development methodology",
            "report organization",
            "chapter 2",
            "background study",
            "literature review",
            "chapter 3",
            "system analysis",
            "requirement analysis",
            "functional requirements",
            "non-functional requirements",
            "feasibility",
            "class diagram",
            "object diagram",
            "state diagram",
            "sequence diagram",
            "activity diagram",
            "component diagram",
            "deployment diagram",
            "system design",
            "chapter 4",
            "implementation",
            "tools used",
            "testing",
            "result analysis",
            "chapter 5",
            "conclusion",
            "future recommendations",
            "references",
            "appendices",
        ],
        "optional_sections": ["bibliography", "algorithm details"],
        "chapter_structure": {
            "chapter 1": [
                "1.1 Introduction",
                "1.2 Problem Statement",
                "1.3 Objectives",
                "1.4 Scope and Limitation",
                "1.5 Development Methodology",
                "1.6 Report Organization",
            ],
            "chapter 2": [
                "2.1 Background Study",
                "2.2 Literature Review",
            ],
            "chapter 3": [
                "3.1 System Analysis",
                "3.1.1 Requirement Analysis",
                "3.1.2 Feasibility Analysis",
                "Object Modelling (Class & Object Diagrams)",
                "Dynamic Modelling (State & Sequence Diagrams)",
                "Process Modelling (Activity Diagrams)",
                "3.2 System Design",
                "Component Diagrams",
                "Deployment Diagrams",
                "3.3 Algorithm Details (if any)",
            ],
            "chapter 4": [
                "4.1 Implementation",
                "4.1.1 Tools Used",
                "4.1.2 Implementation Details of Modules",
                "4.2 Testing",
                "4.2.1 Test Cases for Unit Testing",
                "4.2.2 Test Cases for System Testing",
                "4.3 Result Analysis",
            ],
            "chapter 5": [
                "5.1 Conclusion",
                "5.2 Future Recommendations",
            ],
        },
    },
}

# Official TU FOHSS Formatting Standards (same for all projects)
FORMATTING_STANDARDS = {
    "font": "Times New Roman",
    "font_sizes": {
        "chapter_heading": 16,  # Bold, Center aligned
        "section_heading": 14,  # Bold, Left aligned
        "subsection_heading": 12,  # Bold
        "body": 12,  # Regular, Justified
        "caption": 12,  # Bold (figures & tables)
    },
    "margins_inches": {
        "left": 1.25,    # 35mm
        "right": 1.0,    # 20mm
        "top": 1.0,      # 25mm (some docs say 35mm — TU CDC says 1 inch)
        "bottom": 1.0,   # 20mm
    },
    "line_spacing": 1.5,
    "alignment": "Justified",
    "page_numbering": {
        "front_matter": "Roman (i, ii, iii...)",
        "main_body": "Arabic (1, 2, 3...)",
        "position": "Bottom Center",
        "start_from": "Certificate page",
        "arabic_from": "Chapter 1",
    },
    "paper_size": "A4",
    "binding": "Golden Embracing with Black Binding",
    "copies": 3,
    "copies_to": ["College Library", "Self", "Dean Office (Exam Section, FOHSS)"],
    "referencing": "IEEE",
    "figure_caption": "Centered BELOW the figure (Bold, 12pt)",
    "table_caption": "Centered ABOVE the table (Bold, 12pt)",
}


def check_structure(text, doc_type="project_2"):
    template = TEMPLATES.get(doc_type, TEMPLATES["project_2"])
    
    # Specific normalize — sabai hyphen hoina, chapter matra
    text_lower = text.lower()
    text_lower = text_lower.replace('chapter-', 'chapter ')
    text_lower = text_lower.replace('chapter –', 'chapter ')
    text_lower = text_lower.replace('chapter —', 'chapter ')
    
    found = []
    missing = []

    for section in template["required_sections"]:
        # Flexible matching — exact + partial
        section_lower = section.lower()

        # Direct match
        if section_lower in text_lower:
            found.append(section)
            continue

        # Flexible match — split keywords
        words = section_lower.split()
        if len(words) >= 2:
            # Check if main keywords exist nearby
            first_word_idx = text_lower.find(words[0])
            if first_word_idx != -1:
                nearby = text_lower[first_word_idx:first_word_idx + 60]
                if all(w in nearby for w in words[1:]):
                    found.append(section)
                    continue
        # Doc type anusar section number mapping farak
        if doc_type == "internship":
            section_num_map = {
                "background study": "3.1",
                "literature review": "3.2",
                "organization details": "2.1",
                "organizational hierarchy": "2.2",
                "working domains": "2.3",
                "intern department": "2.4",
                "roles and responsibilities": "4.1",
                "weekly log": "4.2",
                "conclusion": "5.1",
                "learning outcome": "5.2",
            }
        else:
            section_num_map = {
                "background study": "2.1",
                "literature review": "2.2",
                "system analysis": "3.1",
                "tools used": "4.1.1",
                "unit testing": "4.2.1",
                "system testing": "4.2.2",
                "future recommendations": "5.3",
        }
        # Abbreviation / alternate forms
        alternates = {
            "cover page": [
                "cover page", "title page", "tribhuvan university",
                "a project report", "project report", "department of computer application",
                "in partial fulfillment", "submitted to"
            ],
            "title page": [
                "title page", "cover page", "tribhuvan university",
                "a project report", "submitted to", "department of computer application"
            ],
            "supervisor's recommendation": [
                "supervisor", "recommendation", "hereby recommend",
                "under my supervision", "recomm"
            ],
            "letter of approval": [
                "letter of approval", "approval sheet", "approval letter",
                "this is to certify", "letter of appro"
            ],
            "declaration": [
                "declaration", "hereby declare", "self-declaration"
            ],
            "acknowledgement": [
                "acknowledgement", "acknowledgment", "acknowledge"
            ],
            "table of contents": [
                "table of contents", "contents", "toc"
            ],
            "list of abbreviations": [
                "abbreviation", "list of abbr", "acronym"
            ],
            "list of figures": [
                "list of figure", "figure list", "figures"
            ],
            "list of tables": [
                "list of table", "table list"
            ],
            "abstract": [
                "abstract"
            ],
            "background study": [
                "background study", "background and",
                "background of", "theoretical background", section_num_map.get("background study", "2.1")
            ],
            "literature review": [
                "literature review", "related work",
                "related studies", "review of literature", section_num_map.get("literature review", "2.2")
            ],
            "system analysis": [
                "system analysis", "3.1", "requirement analysis",
                "analysis and design"
            ],
            "functional requirements": [
                "functional requirement", "use case", "use-case"
            ],
            "non-functional requirements": [
                "non-functional", "nonfunctional", "non functional"
            ],
            "feasibility": [
                "feasibility", "feasible"
            ],
            "er diagram": [
                "er diagram", "entity relationship", "erd", "e-r diagram",
                "entity-relationship"
            ],
            "dfd": [
                "dfd", "data flow diagram", "data flow"
            ],
            "class diagram": [
                "class diagram", "uml class", "object diagram"
            ],
            "sequence diagram": [
                "sequence diagram", "sequence model"
            ],
            "activity diagram": [
                "activity diagram"
            ],
            "component diagram": [
                "component diagram"
            ],
            "deployment diagram": [
                "deployment diagram"
            ],
            "architectural design": [
                "architectural design", "architecture design",
                "system architecture", "architectural"
            ],
            "database schema": [
                "database schema", "db schema", "schema design",
                "database design"
            ],
            "interface design": [
                "interface design", "ui design", "ui/ux", "user interface"
            ],
            "algorithm details": [
                "algorithm detail", "algorithm", "3.3"
            ],
            "tools used": [
                "tools used", "tool used", "4.1.1", "technologies used",
                "programming language", "development tools"
            ],
            "unit testing": [
                "unit test", "unit testing", "4.2.1"
            ],
            "system testing": [
                "system test", "system testing", "4.2.2",
                "integration test"
            ],
            "result analysis": [
                "result analysis", "results and analysis",
                "analysis of result", "4.3"
            ],
            "lesson learnt": [
                "lesson learnt", "lesson learned", "outcome",
                "5.2", "lessons learned"
            ],
            "future recommendations": [
                "future recommendation", "future work",
                "future scope", "5.3"
            ],
            "references": [
                "references", "bibliography", "reference list"
            ],
            "appendices": [
                "appendix", "appendices", "screen shot",
                "screenshot", "source code"
            ],
            "mentor's recommendation": [
                "mentor", "mentor's recommendation", "mentors recommendation",
                "recommendation from company", "company mentor"
            ],
            "organization details": [
                "organization details", "organisation details",
                "introduction to organization", section_num_map.get("organization details", "2.1"),
            ],
            "organizational hierarchy": [
                "organizational hierarchy", "organisational hierarchy",
                "org hierarchy", section_num_map.get("organizational hierarchy", "2.2"),
            ],
            "working domains": [
                "working domains", "domain of organization", section_num_map.get("working domains", "2.3")
            ],
            "intern department": [
                "intern department", "internship department",
                "description of intern", section_num_map.get("intern department", "2.4"),
            ],
            "roles and responsibilities": [
                "roles and responsibilities", "role and responsibility", section_num_map.get("roles and responsibilities", "4.1")
            ],
            "weekly log": [
                "weekly log", "weekly diary", "weekly activity", section_num_map.get("weekly log", "4.2"),
            ],
            "tasks": [
                "tasks", "activities performed", "task performed", section_num_map.get("tasks", "4.4"),
            ],
            "learning outcome": [
                "learning outcome", "lesson learnt", "lesson learned",
                "outcome", section_num_map.get("learning outcome", "5.2"),
            ],
            "scope and limitation": [
                "scope and limitation",
                "scope and limitations", 
                "scope of the system",
                "1.4",                 # ← section number
                "scope",                  # ← single word
                "limitation",             # ← single word   
            ],
            "report organization": [
                "report organization",
                "organization of report",
                "report organisation",
                "1.5", "1.6",            # ← project_1 ma 1.5, project_2 ma 1.6
            ],
        }

        alt_list = alternates.get(section_lower, [])
        matched = any(alt in text_lower for alt in alt_list)
        if matched:
            found.append(section)
        else:
            missing.append(section)

    # Chapters found
    chapters_found = []
    for i in range(1, 6):
        patterns = [f"chapter {i}", f"chapter{i}",f"chapter-{i}", f"ch {i}", f"ch.{i}", f"ch-{i}",]
        if any(p in text_lower for p in patterns):
            chapters_found.append(f"Chapter {i}")

    # Subsection issues — flexible matching
    subsection_issues = []
    for chapter, subsections in template["chapter_structure"].items():
        if chapter not in text_lower:
            continue
        for sub in subsections:
            sub_lower = sub.lower()

            # Extract title part after section number (e.g. "3.3 algorithm details" -> "algorithm details")
            parts = sub_lower.split(' ', 1)
            title_part = parts[1] if len(parts) > 1 and parts[0][0].isdigit() else sub_lower

            # Clean optional markers for matching
            clean_title = title_part.replace('(if used)', '').replace('(if any)', '').strip()

            # Check if exists
            is_found = (
                clean_title in text_lower or
                sub_lower.split('(')[0].strip() in text_lower or
                all(w in text_lower for w in clean_title.split()[:3])
            )

            if not is_found:
                # Only flag as missing if NOT optional
                if '(if used)' not in sub_lower and '(if any)' not in sub_lower:
                    subsection_issues.append(f"{sub} (under {chapter.title()})")
                # Optional ones — skip silently (user ko choice)

    return {
        "template": template["name"],
        "semester": template["semester"],
        "course_code": template["code"],
        "found": found,
        "missing": missing,
        "sections_found": len(found),
        "total_required": len(template["required_sections"]),
        "chapters_found": chapters_found,
        "subsection_issues": subsection_issues[:8],
    }
import re

def detect_group_members(text):
    text_lower = text.lower()
    submitted_idx = text_lower.find("submitted by")
    if submitted_idx == -1:
        return {"count": None, "names": [], "roll_nos": []}

    sample = text[submitted_idx: submitted_idx + 400]

    # Exam symbol no — 9 digits (e.g. 122802072)
    symbol_pattern = re.compile(r'\b\d{9}\b')

    # TU Regd No — e.g. 6-2-1228-15-2022
    regd_pattern = re.compile(r'\d{1,2}-\d{1,2}-\d{3,4}-\d{1,3}-\d{4}')

    # Old roll pattern — 76-230-001
    roll_pattern = re.compile(r'\b\d{2}[-/]\d{3}[-/]\d{3}\b')
    
    rolls = roll_pattern.findall(sample)
    regds = regd_pattern.findall(sample)
    symbols = symbol_pattern.findall(sample)

    lines = [l.strip() for l in sample.split('\n') if l.strip()]
    name_lines = []
    skip_keywords = [
        'submitted', 'roll', 'regd', 'exam', 'month', 'year',
        'tribhuvan', 'department', 'college', 'supervisor',
        'under', 'faculty', 'partial', 'fulfillment',
        'supervision', 'supervised', 'january', 'february',
        'march', 'april', 'may', 'june', 'july', 'august',
        'september', 'october', 'november', 'december',
        'report', 'project', 'internship', 'bachelor',
        'computer', 'application', 'technology', 'management',
        'information', 'science', 'engineering',
    ]

    for line in lines[1:]:
        line_lower = line.lower()
        if 'supervision' in line_lower or 'supervisor' in line_lower:
            break
        if any(kw in line_lower for kw in skip_keywords):
            continue
        if re.match(r'^\d', line):
            continue
        if line.isupper() and len(line) > 5:
            continue
        if len(line) > 50:
            continue
        if len(line) < 4:
            continue

        # Fix 2 — bracket content hatauera name check garne
        # "Naran Khadka [TU Regd. No. 6-2-1228]" → "Naran Khadka"
        clean_line = re.sub(r'\[.*?\]|\(.*?\)', '', line).strip()
        if not clean_line:
            continue

        words = clean_line.split()
        if len(words) >= 1 and any(w[0].isupper() for w in words if w):
            name_lines.append(clean_line)

        if len(name_lines) >= 2:
            break

    # Fix 3 — regd numbers most reliable for count
    all_ids = regds or rolls or symbols
    count = len(all_ids) if all_ids else len(name_lines) if name_lines else None
    count = min(count, 2) if count else None

    return {
        "count": count,
        "names": name_lines[:2],
        "roll_nos": (regds or rolls or symbols)[:2],
    } 

def validate_group(text, doc_type="project_2"):
    """
    Group size validate garne — TU BCA max 2 members.
    Individual vs group formatting check.
    """
    
    member_info = detect_group_members(text)
    count = member_info.get("count")
    issues = []

    # TU rule: max 2 members for Project I & II
    if doc_type in ("project_1", "project_2", "internship"):
        if count and count > 2:
            issues.append({
                "type": "error",
                "message": (
                    f"{count} members detected. TU BCA allows "
                    "maximum 2 members per project group."
                )
            })
        elif count == 2:
            issues.append({
                "type": "info",
                "message": (
                    f"Group project detected (2 members). "
                    "Ensure both members' names, Roll No., and TU Regd. No. "
                    "are on the cover page. "
                    "Both must demonstrate equal individual contribution."
                )
            })
        elif count == 1:
            issues.append({
                "type": "success",
                "message": "Individual project detected ✓"
            })
        else:
            issues.append({
                "type": "warning",
                "message": (
                    "Could not detect member count from cover page. "
                    "Ensure 'Submitted by' section includes full name(s), "
                    "Exam Roll No., and TU Regd. No. for all members."
                )
            })
    # Internship — must be individual (TU CDC explicitly says "Individual Report" for CAIN403)
    elif doc_type == "internship":
        if count and count > 1:
            issues.append({
                "type": "error",
                "message": (
                    f"{count} members detected. "
                    "TU BCA Internship report must be INDIVIDUAL. "
                    "Even if internship was done in groups at same organization, "
                    "each student must submit a separate individual report."
                )
            })
        elif count == 1:
            issues.append({
                "type": "success",
                "message": "Individual internship report detected ✓"
            })
        else:
            issues.append({
                "type": "warning",
                "message": (
                    "Could not detect member count. "
                    "Internship report must be individual — "
                    "only one student's name should appear in 'Submitted by' section."
                )
            })
    # Project III — individual only
    elif doc_type == "project_3":
        if count and count > 1:
            issues.append({
                "type": "error",
                "message": (
                    "Project III (8th semester) must be individual. "
                    f"{count} members detected — not allowed."
                )
            })
        else:
            issues.append({
                "type": "success",
                "message": "Individual project — correct for Project III ✓"
            })

    return {
        "member_count": count,
        "member_names": member_info.get("names", []),
        "roll_nos": member_info.get("roll_nos", []),
        "group_feedback": issues,
    }

def check_numbering_consistency(text, doc_type="project_2"):
    issues = []
    text_lower = text.lower()

    # ── PROPOSAL vs FINAL REPORT DETECTION ──
    
    # Internship proposal keywords
    internship_proposal_keywords = [
        'expected outcome of internship',
        'internship proposal defense',
        'description of internship work',
        'expected outcome',
        'internship plan',
        'proposal defense',
    ]

    # Project proposal keywords
    project_proposal_keywords = [
        'gantt chart',
        'expected outcome',
        'proposal defense',
        'high level design of system',
        'requirement identification',
        'feasibility study',  # proposal ma hunxa tara context farak
        'project proposal',
    ]

    # Final report must-have keywords
    final_report_keywords = {
        "project_1": ['implementation', 'testing', 'test cases', 'source code', 'conclusion'],
        "project_2": ['implementation', 'testing', 'test cases', 'source code', 'conclusion'],
        "project_3": ['implementation', 'testing', 'result analysis', 'conclusion'],
        "internship": ['roles and responsibilities', 'weekly log', 'learning outcome', 'conclusion'],
    }

    if doc_type == "internship":
        found_proposal = [kw for kw in internship_proposal_keywords if kw in text_lower]
        if found_proposal:
            issues.append({
                "type": "error",
                "message": (
                    "🚨 This appears to be an INTERNSHIP PROPOSAL, not a Final Report. "
                    f"Proposal content detected: '{found_proposal[0]}'. "
                    "Final internship report must have: "
                    "Ch2=Organization Intro, Ch3=Background Study & Lit Review, "
                    "Ch4=Internship Activities, Ch5=Conclusion & Learning Outcome."
                )
            })
    else:
        found_proposal = [kw for kw in project_proposal_keywords if kw in text_lower]
        must_have = final_report_keywords.get(doc_type, [])
        has_final_content = any(kw in text_lower for kw in must_have)

        if found_proposal and not has_final_content:
            issues.append({
                "type": "error",
                "message": (
                    f"🚨 This appears to be a PROJECT PROPOSAL, not a Final Report. "
                    f"Proposal content detected: '{found_proposal[0]}'. "
                    "Final report must include implementation, testing, and conclusion chapters."
                )
            })
        elif found_proposal and has_final_content:
            issues.append({
                "type": "warning",
                "message": (
                    f"⚠️ Some proposal-specific content detected ('{found_proposal[0]}'). "
                    "Ensure this is intentional — final reports should not include proposal sections."
                )
            })

    # ── WRONG CHAPTER NUMBERING ──
    for chap_num in range(2, 6):
        pattern = rf'chapter\s*[-–]?\s*{chap_num}[^\n]*\n+\s*1\.\d+\s+\w+'
        match = re.search(pattern, text_lower[:8000])
        if match:
            issues.append({
                "type": "warning",
                "message": (
                    f"Chapter {chap_num} sub-sections use wrong numbering (1.x). "
                    f"Should be {chap_num}.1, {chap_num}.2, {chap_num}.3..."
                )
            })
            break

    # ── DEVELOPMENT METHODOLOGY in Internship ──
    if doc_type == "internship" and '1.5 development methodology' in text_lower:
        issues.append({
            "type": "warning",
            "message": (
                "Development Methodology (1.5) detected — this belongs in Project reports. "
                "Internship Chapter 1: 1.1 Introduction, 1.2 Problem Statement, "
                "1.3 Objectives, 1.4 Scope & Limitation, 1.5 Report Organization."
            )
        })

    return issues