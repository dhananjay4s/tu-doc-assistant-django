import re
import spacy
from functools import lru_cache

# Load spaCy model once
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None

# ─────────────────────────────────────────
# PASSIVE VOICE DETECTION via spaCy
# ─────────────────────────────────────────

def detect_passive_sentences(text):
    """
    spaCy dependency parsing use garera passive voice detect garne.
    Passive = nsubjpass dependency OR auxpass auxiliary verb.
    """
    if not nlp:
        return [], []

    doc = nlp(text[:50000])  # limit for performance
    passive_sentences = []
    active_first_person = []

    for sent in doc.sents:
        sent_text = sent.text.strip()
        if len(sent_text) < 10:
            continue

        has_passive = False
        has_first_person = False
        first_person_tokens = []

        for token in sent:
            # Passive detection
            if token.dep_ in ("nsubjpass", "auxpass"):
                has_passive = True

            # First person detection
            if token.text.lower() in ("i", "we", "my", "our", "mine", "ours"):
                if token.pos_ == "PRON":
                    has_first_person = True
                    first_person_tokens.append(token.text)

        # Active sentence with first person = problem
        if has_first_person and not has_passive:
            active_first_person.append({
                "sentence": sent_text[:200],
                "pronouns": list(set(first_person_tokens)),
                "suggested": _suggest_passive(sent_text),
            })

        elif has_passive:
            passive_sentences.append(sent_text[:200])

    return active_first_person, passive_sentences


def _suggest_passive(sentence):
    """
    Simple rule-based passive suggestion.
    """
    replacements = {
        r'\bI developed\b': 'The system was developed',
        r'\bI implemented\b': 'The implementation was carried out',
        r'\bI designed\b': 'The design was formulated',
        r'\bI created\b': 'The application was created',
        r'\bI used\b': 'The study employed',
        r'\bI tested\b': 'Testing was performed',
        r'\bI analyzed\b': 'An analysis was conducted',
        r'\bI built\b': 'The system was built',
        r'\bI made\b': 'The development was carried out',
        r'\bWe developed\b': 'The system was developed',
        r'\bWe implemented\b': 'The implementation was carried out',
        r'\bWe designed\b': 'The design was formulated',
        r'\bWe used\b': 'The study employed',
        r'\bWe tested\b': 'Testing was conducted',
        r'\bWe built\b': 'The system was built',
        r'\bWe created\b': 'The application was created',
        r'\bour system\b': 'the developed system',
        r'\bour project\b': 'the proposed project',
        r'\bour application\b': 'the developed application',
        r'\bmy project\b': 'the project',
    }

    result = sentence
    for pattern, replacement in replacements.items():
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    if result == sentence:
        return "Rewrite using passive voice. E.g., 'I did X' → 'X was performed'"
    return result


# ─────────────────────────────────────────
# GRAMMAR CHECK via LanguageTool
# ─────────────────────────────────────────

_lt = None

def _get_language_tool():
    """Lazy load LanguageTool — once only."""
    global _lt
    if _lt is None:
        try:
            import language_tool_python
            _lt = language_tool_python.LanguageTool('en-US')
        except Exception:
            _lt = False  # Mark as failed
    return _lt if _lt else None


def check_grammar(text):
    """
    LanguageTool use garera grammar errors detect garne.
    Academic writing specific rules focus garne.
    """
    lt = _get_language_tool()
    if not lt:
        return []

    # Sample first 8000 chars for performance
    sample = text[:8000]

    try:
        matches = lt.check(sample)
    except Exception:
        return []

    grammar_issues = []
    seen = set()

    # Filter relevant rules for academic writing
    ignore_rules = {
        "WHITESPACE_RULE",
        "COMMA_PARENTHESIS_WHITESPACE",
        "EN_QUOTES",
        "DASH_RULE",
        "WORD_CONTAINS_UNDERSCORE",
        "UPPERCASE_SENTENCE_START",  # headings often uppercase
        "MORFOLOGIK_RULE_EN_US",  # ← Nepali names spelling false positive hatauxa
        "SPELLING_RULE",           # ← General spelling checker off
        "I_LOWERCASE",              # ← Thap: Roman numeral "i" lai pronoun nabhanxa
        "UPPERCASE_ROMAN_NUMERAL",
    }

    academic_priority_rules = {
        "AGREEMENT_SENT_START",
        "EN_A_VS_AN",
        "ENGLISH_WORD_REPEAT_RULE",
        "TOO_LONG_SENTENCE",
        "PASSIVE_VOICE",
        "SENTENCE_FRAGMENT",
        "COMMA_SPLICE",
        "MISSING_COMMA_BEFORE_BUT",
        "DOUBLE_NEGATION",
        "ARTICLE_MISSING",
        "SUBJECT_VERB_AGREEMENT",
    }

    for match in matches:
        if match.rule_id in ignore_rules:
            continue
        error_text = sample[match.offset: match.offset + match.error_length].strip()
        if error_text.lower() in ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']:
            continue

        # Avoid duplicates
        key = f"{match.rule_id}_{match.offset}"
        if key in seen:
            continue
        seen.add(key)

        # Get context
        context_start = max(0, match.offset - 30)
        context_end = min(len(sample), match.offset + match.error_length + 30)
        context = sample[context_start:context_end].replace('\n', ' ').strip()

        # Get suggestion
        suggestion = match.replacements[0] if match.replacements else None

        priority = "high" if match.rule_id in academic_priority_rules else "normal"

        grammar_issues.append({
            "rule": match.rule_id,
            "message": match.message,
            "context": f"...{context}...",
            "error_text": sample[match.offset:match.offset + match.error_length],
            "suggestion": suggestion,
            "priority": priority,
        })

        if len(grammar_issues) >= 15:  # limit output
            break

    return grammar_issues


# ─────────────────────────────────────────
# INFORMAL LANGUAGE DETECTION
# ─────────────────────────────────────────

INFORMAL_MAP = {
    'gonna': 'going to',
    'wanna': 'want to',
    'kinda': 'somewhat / to some extent',
    'sort of': 'to some extent',
    'kind of': 'to some extent',
    'stuff': 'components / elements',
    'things': 'components / aspects',
    'a lot': 'numerous / significant',
    'lots of': 'numerous',
    'really': 'significantly / considerably',
    'basically': 'fundamentally / essentially',
    'literally': 'precisely / in fact',
    'awesome': 'highly effective',
    'cool': 'efficient',
    'nice': 'appropriate',
    'pretty much': 'largely / primarily',
    'you know': '[remove]',
    'like': '[review usage — avoid filler]',
    'just': '[remove or rephrase]',
    'very': 'considerably / significantly',
    'big': 'substantial / significant',
    'small': 'minimal / limited',
    'good': 'effective / adequate',
    'bad': 'inadequate / ineffective',
    'easy': 'straightforward / simplified',
    'hard': 'complex / challenging',
    'simple': 'straightforward',
    'show': 'demonstrate / illustrate',
    'use': 'employ / utilize',
    'get': 'obtain / retrieve',
    'make': 'develop / construct',
    'find out': 'determine / identify',
    'look at': 'examine / analyze',
    'deal with': 'address / handle',
}

def detect_informal_language(text):
    """Detect informal words with sentence context."""
    text_lower = text.lower()
    found = []

    for informal, formal in INFORMAL_MAP.items():
        pattern = r'\b' + re.escape(informal) + r'\b'
        matches = list(re.finditer(pattern, text_lower))
        if not matches:
            continue

        # Get first occurrence context
        m = matches[0]
        start = max(0, m.start() - 60)
        end = min(len(text), m.end() + 60)
        context = text[start:end].replace('\n', ' ').strip()

        found.append({
            "word": informal,
            "replace_with": formal,
            "count": len(matches),
            "context": f"...{context}...",
        })

    return found


# ─────────────────────────────────────────
# IEEE CITATION CHECK
# ─────────────────────────────────────────

def check_ieee_citations(text):
    """Check IEEE citation format [1], [2] presence and consistency."""
    results = []

    # In-text citations
    inline_citations = re.findall(r'\[(\d+)\]', text)
    citation_numbers = [int(n) for n in inline_citations]

    if not citation_numbers:
        results.append({
            "type": "error",
            "message": "No IEEE citations [1], [2] found in document body. "
                      "All sources must be cited inline as [1], [2], etc."
        })
        return results

    max_citation = max(citation_numbers)
    unique_citations = sorted(set(citation_numbers))

    # Check if citations are sequential
    expected = list(range(1, max_citation + 1))
    missing_nums = [n for n in expected if n not in unique_citations]

    results.append({
        "type": "success",
        "message": f"IEEE citations found: {len(unique_citations)} unique citations "
                  f"([1] to [{max_citation}]) — {len(inline_citations)} total uses."
    })

    if missing_nums:
        results.append({
            "type": "warning",
            "message": f"Citation numbers {missing_nums} missing. "
                      "Citations should be sequential [1],[2],[3]..."
        })

    # References section check
    ref_section = re.search(r'references?\s*\n(.*?)(?=appendix|bibliography|$)',
                           text, re.IGNORECASE | re.DOTALL)
    if ref_section:
        ref_text = ref_section.group(1)
        ref_entries = re.findall(r'\[(\d+)\]', ref_text)
        if len(ref_entries) < len(unique_citations):
            results.append({
                "type": "warning",
                "message": f"References section has {len(ref_entries)} entries but "
                          f"{len(unique_citations)} citations used. All citations must be listed."
            })
        else:
            results.append({
                "type": "success",
                "message": f"References section has {len(ref_entries)} entries ✓"
            })

    return results


# ─────────────────────────────────────────
# MAIN CHECK LANGUAGE FUNCTION
# ─────────────────────────────────────────

def check_language(text):
    issues = []
    warnings = []
    suggestions = []

    # 1. Passive voice & first person (spaCy)
    active_first_person, passive_sentences = detect_passive_sentences(text)

    if active_first_person:
        issues.append({
            "type": "error",
            "message": f"First-person active voice detected in {len(active_first_person)} sentence(s). "
                      "TU FOHSS requires passive voice or third-person throughout."
        })
    else:
        suggestions.append({
            "type": "success",
            "message": f"No first-person active voice detected ✓ "
                      f"({len(passive_sentences)} passive constructions found — good academic tone)"
        })

    # 2. Grammar (LanguageTool)
    grammar_issues = check_grammar(text)
    high_priority = [g for g in grammar_issues if g['priority'] == 'high']
    normal_priority = [g for g in grammar_issues if g['priority'] == 'normal']

    if high_priority:
        issues.append({
            "type": "error",
            "message": f"{len(high_priority)} significant grammar issue(s) detected."
        })
    if normal_priority:
        warnings.append({
            "type": "warning",
            "message": f"{len(normal_priority)} minor grammar suggestion(s) found."
        })
    if not grammar_issues:
        suggestions.append({
            "type": "success",
            "message": "No major grammar issues detected ✓"
        })

    # 3. Informal language
    informal = detect_informal_language(text)
    if informal:
        warnings.append({
            "type": "warning",
            "message": f"Informal vocabulary found: "
                      f"{[i['word'] for i in informal[:5]]}. Replace with academic terms."
        })

    # 4. IEEE citations
    ieee_results = check_ieee_citations(text)
    for r in ieee_results:
        if r['type'] == 'error':
            issues.append(r)
        elif r['type'] == 'warning':
            warnings.append(r)
        else:
            suggestions.append(r)

    return {
        "issues": issues,
        "warnings": warnings,
        "suggestions": suggestions,
        "all_feedback": issues + warnings + suggestions,
        # Detailed data for frontend
        "active_first_person": active_first_person[:5],
        "grammar_issues": grammar_issues[:10],
        "informal_words": informal,
        "ieee_results": ieee_results,
    }