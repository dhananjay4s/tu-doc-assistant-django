import re
import spacy

# Load spaCy model once
try:
    nlp = spacy.load("en_core_web_md")  # md > sm
except OSError:
    try:
        nlp = spacy.load("en_core_web_sm")  # fallback
    except OSError:
        nlp = None

# ─────────────────────────────────────────
# PASSIVE VOICE DETECTION via spaCy
# ─────────────────────────────────────────

def detect_passive_sentences(text):
    if not nlp:
        return [], []

    # Process in chunks — full document cover garne
    chunk_size = 50000
    all_active = []
    all_passive = []

    for i in range(0, min(len(text), 150000), chunk_size):
        chunk = text[i:i+chunk_size]
        doc = nlp(chunk)

        for sent in doc.sents:
            sent_text = sent.text.strip()
            if len(sent_text) < 10:
                continue

            has_passive = False
            has_first_person = False
            first_person_tokens = []

            for token in sent:
                # spaCy v3 passive detection — multiple signals
                if token.dep_ in ("nsubjpass", "auxpass"):
                    has_passive = True
                # Alternative passive signal
                if token.lemma_ == "be" and token.head.pos_ == "VERB":
                    if any(c.dep_ == "agent" for c in token.head.children):
                        has_passive = True

                if token.text.lower() in ("i", "we", "my", "our", "mine", "ours"):
                    if token.pos_ == "PRON":
                        has_first_person = True
                        first_person_tokens.append(token.text)

            if has_first_person and not has_passive:
                # Skip acknowledgement section — first person allowed there
                if 'acknowledge' not in sent_text.lower():
                    all_active.append({
                        "sentence": sent_text[:200],
                        "pronouns": list(set(first_person_tokens)),
                        "suggested": _suggest_passive(sent_text),
                    })

            elif has_passive:
                all_passive.append(sent_text[:200])

    return all_active[:5], all_passive


def _suggest_passive(sentence):
    # spaCy subject/verb extract garxa bhane specific suggestion
    if nlp:
        try:
            doc = nlp(sentence[:200])
            subj = next((t.text for t in doc if t.dep_ in ('nsubj', 'nsubjpass')), None)
            verb = next((t.lemma_ for t in doc if t.pos_ == 'VERB'), None)
            if subj and verb and subj.lower() in ('i', 'we', 'my', 'our'):
                return (f"Consider: 'The {verb} was performed' or "
                        f"restructure to remove '{subj}' as subject.")
        except Exception:
            pass

    # Fallback — rule based
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

    # Multiple chunks — 8000 chars bata 3 sections check
    total_len = len(text)
    step = max(6000, total_len // 4)
    chunk_points = list(range(0, min(total_len, 30000), step))
    
    grammar_issues = []
    seen = set()

    # Filter relevant rules for academic writing
    ignore_rules = {
        "WHITESPACE_RULE",
        "COMMA_PARENTHESIS_WHITESPACE",
        "EN_QUOTES", "DASH_RULE",
        "WORD_CONTAINS_UNDERSCORE",
        "UPPERCASE_SENTENCE_START",
        "MORFOLOGIK_RULE_EN_US",
        "SPELLING_RULE",
        "I_LOWERCASE",
        "UPPERCASE_ROMAN_NUMERAL",
        "PUNCTUATION_PARAGRAPH_END",
        "UNLIKELY_OPENING_PUNCTUATION",
        "COMMA_COMPOUND_SENTENCE",
        "EN_UNPAIRED_BRACKETS",
        "SENTENCE_WHITESPACE",
        "DOUBLE_PUNCTUATION",
        "CURRENCY",
        "ARROWS",
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

    for start in chunk_points:
        if len(grammar_issues) >= 15:
            break
        sample = text[start:start+8000]
        if not sample.strip():
            continue

        try:
            matches = lt.check(sample)
        except Exception:
            continue

        for match in matches:
            if match.rule_id in ignore_rules:
                continue

            error_text = sample[match.offset: match.offset + match.error_length].strip()
            if error_text.lower() in ['i','ii','iii','iv','v','vi','vii','viii','ix','x']:
                continue

            key = f"{match.rule_id}_{error_text}"
            if key in seen:
                continue
            seen.add(key)

            context_start = max(0, match.offset - 40)
            context_end = min(len(sample), match.offset + match.error_length + 40)
            context = sample[context_start:context_end].replace('\n', ' ').strip()

            grammar_issues.append({
                "rule": match.rule_id,
                "message": match.message,
                "context": f"...{context}...",
                "error_text": error_text,
                "suggestion": match.replacements[0] if match.replacements else None,
                "priority": "high" if match.rule_id in academic_priority_rules else "normal",
            })

            if len(grammar_issues) >= 15:
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

def check_citations(text, referencing="IEEE"):
    """Check citation format — IEEE for projects, APA for internship."""
    results = []

    if referencing == "APA":
        # APA: (Author, Year) pattern
        apa_citations = re.findall(
            r'([A-Z][a-zA-Z]+[\.,]\s*\(?\d{4}|'   # Author. (2024)
            r'[A-Z][a-zA-Z]+[\.,]\s*\(?n\.d\.|'   # Author. (n.d.)
            r'\([A-Z][a-zA-Z]+,\s*\d{4}\)|'       # (Author, 2024)
            r'\([A-Z][a-zA-Z]+,\s*n\.d\.\))',     # (Author, n.d.)
            text
        )
        if not apa_citations:
            results.append({
                "type": "error",
                "message": (
                    "No APA citations found. Internship report requires APA format. "
                    "Example: (Sharma, 2023) or (Smith & Jones, 2022)"
                )
            })
        else:
            results.append({
                "type": "success",
                "message": f"APA citations detected: {len(apa_citations)} found ✓"
            })
        return results

    # IEEE format — [1], [2]
    inline_citations = re.findall(r'\[(\d+)\]', text)
    citation_numbers = [int(n) for n in inline_citations]

    if not citation_numbers:
        results.append({
            "type": "error",
            "message": "No IEEE citations [1], [2] found. All sources must be cited inline."
        })
        return results

    max_citation = max(citation_numbers)
    unique_citations = sorted(set(citation_numbers))
    missing_nums = [n for n in range(1, max_citation + 1) if n not in unique_citations]

    results.append({
        "type": "success",
        "message": (
            f"IEEE citations found: {len(unique_citations)} unique "
            f"([1] to [{max_citation}]) — {len(inline_citations)} total uses ✓"
        )
    })
    if missing_nums:
        results.append({
            "type": "warning",
            "message": f"Citation numbers {missing_nums} missing — should be sequential."
        })

    # References section check
    ref_match = re.search(r'references?\s*\n(.*?)(?=appendix|bibliography|$)',
                          text, re.IGNORECASE | re.DOTALL)
    if ref_match:
        ref_entries = re.findall(r'\[(\d+)\]', ref_match.group(1))
        if len(ref_entries) < len(unique_citations):
            results.append({
                "type": "warning",
                "message": (
                    f"References section has {len(ref_entries)} entries but "
                    f"{len(unique_citations)} citations used."
                )
            })
        else:
            results.append({
                "type": "success",
                "message": f"References section: {len(ref_entries)} entries ✓"
            })

    return results

# ─────────────────────────────────────────
# MAIN CHECK LANGUAGE FUNCTION
# ─────────────────────────────────────────

def check_language(text, doc_type):
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

    # 4. Citations — IEEE for projects, APA for internship
    referencing = "APA" if doc_type == "internship" else "IEEE"
    citation_results = check_citations(text, referencing)
    for r in citation_results:
        if r['type'] == 'error':     issues.append(r)
        elif r['type'] == 'warning': warnings.append(r)
        else:                        suggestions.append(r)

    # 5. Academic tone specific checks
    academic_tone_issues = check_academic_tone(text)
    for issue in academic_tone_issues:
        if issue['type'] == 'error':
            issues.append(issue)
        else:
            warnings.append(issue)

    return {
        "issues": issues,
        "warnings": warnings,
        "suggestions": suggestions,
        "all_feedback": issues + warnings + suggestions,
        "active_first_person": active_first_person[:5],
        "grammar_issues": grammar_issues[:15],
        "informal_words": informal,
        "ieee_results": citation_results,
        "academic_tone": academic_tone_issues,
    }

def check_academic_tone(text):
    """Academic writing specific issues detect garne."""
    issues = []
    text_lower = text.lower()

    # 1. Tense consistency — academic reports past/present tense mix
    future_in_body = re.findall(
        r'\b(will be|will have|shall be|going to)\b',
        text_lower
    )
    if len(future_in_body) > 5:
        issues.append({
            "type": "warning",
            "message": (
                f"Future tense used {len(future_in_body)} times. "
                "Academic reports use past tense for completed work. "
                "E.g., 'will be implemented' → 'was implemented'."
            )
        })

    # 2. Vague quantifiers
    vague = re.findall(
        r'\b(some|many|several|various|numerous|a number of|few)\b',
        text_lower
    )
    if len(vague) > 8:
        issues.append({
            "type": "warning",
            "message": (
                f"Vague quantifiers found {len(vague)} times: {list(set(vague))[:4]}. "
                "Use specific numbers where possible. "
                "E.g., 'several tests' → '12 unit tests'."
            )
        })

    # 3. Unsupported claims
    unsupported = re.findall(
        r'\b(clearly|obviously|it is known|everyone knows|it is clear that)\b',
        text_lower
    )
    if unsupported:
        issues.append({
            "type": "warning",
            "message": (
                f"Unsupported claim language: {list(set(unsupported))}. "
                "Academic writing requires evidence-based statements with citations."
            )
        })

    # 4. Contractions
    contractions = re.findall(
        r"\b(don't|doesn't|isn't|aren't|wasn't|weren't|"
        r"can't|couldn't|won't|wouldn't|it's|that's|there's)\b",
        text_lower
    )
    if contractions:
        issues.append({
            "type": "error",
            "message": (
                f"Contractions detected: {list(set(contractions))[:5]}. "
                "Academic writing requires full forms. "
                "E.g., 'don't' → 'do not', 'isn't' → 'is not'."
            )
        })

    # 5. Short paragraphs (less than 3 sentences)
    paragraphs = [p.strip() for p in re.split(r'\n{2,}|\n(?=[A-Z])', text) if len(p.strip()) > 50]
    short_paras = [p[:60] for p in paragraphs if len(p.split('.')) < 3]
    if len(short_paras) > 5:
        issues.append({
            "type": "info",
            "message": (
                f"{len(short_paras)} very short paragraphs detected. "
                "Academic paragraphs should have minimum 3-4 sentences with clear topic sentence."
            )
        })

    return issues