import re

from classification.tax_documents import TAX_DOCUMENTS
from classification.financial_documents import FINANCIAL_DOCUMENTS
from classification.business_documents import BUSINESS_DOCUMENTS


DOCUMENT_REGISTRIES = {
    "Tax": TAX_DOCUMENTS,
    "Financial": FINANCIAL_DOCUMENTS,
    "Business": BUSINESS_DOCUMENTS
}


def normalize_text(text):

    text = text.lower()

    text = text.replace("’", "'")
    text = text.replace("‘", "'")
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(r"\s+", " ", text)

    return text


def get_form_pattern(document_type):

    # Special handling for partnership and S corporation K-1s
    if "Schedule K-1" in document_type:

        if document_type.startswith("1065"):
            return (
                r"(?:"
                r"\bform\s*1065\b.*?schedule\s*k\s*[- ]?\s*1"
                r"|"
                r"schedule\s*k\s*[- ]?\s*1.*?\bform\s*1065\b"
                r")"
            )

        if document_type.startswith("1120-S"):
            return (
                r"(?:"
                r"\bform\s*1120\s*[- ]?\s*s\b.*?schedule\s*k\s*[- ]?\s*1"
                r"|"
                r"schedule\s*k\s*[- ]?\s*1.*?\bform\s*1120\s*[- ]?\s*s\b"
                r")"
            )

    # Extract the form number from the document registry name
    match = re.search(
        r"\b(?:w-\d[a-z]?|\d{3,5}(?:-[a-z0-9]+)?)\b",
        document_type.lower()
    )

    if not match:
        return None

    form_number = match.group(0)

    # Allow OCR variations in spacing and hyphens
    parts = re.split(r"[-\s]+", form_number)

    pattern = r"[-\s]*".join(
        re.escape(part) for part in parts
    )

    # Require "Form" before the form number
    return (
        r"(?<![a-z0-9])"
        r"form\s*[-:]?\s*"
        + pattern
        + r"(?![a-z0-9-])"
    )


def find_explicit_tax_form(text):

    # Restrict explicit form detection to the first page.
    # This helps prevent incidental references on later pages
    # from overriding the actual document classification.
    first_page = re.split(
        r"---\s*page\s*2\s*---",
        text,
        maxsplit=1
    )[0]

    # Also limit the search length as a safeguard
    first_page = first_page[:5000]

    matches = []

    for document_type in TAX_DOCUMENTS:

        pattern = get_form_pattern(document_type)

        if pattern:

            match = re.search(pattern, first_page)

            if match:
                matches.append((
                    match.start(),
                    -(match.end() - match.start()),
                    document_type
                ))

    # Choose the earliest and most specific form match
    if matches:

        matches.sort()

        return matches[0][2]

    return None


def calculate_keyword_score(keyword, text):

    if keyword not in text:
        return 0

    words = len(keyword.split())

    # Specific phrases receive more weight
    if keyword.startswith("form "):
        return 12

    if words >= 4:
        return 7

    if words == 3:
        return 5

    if words == 2:
        return 3

    return 1


def identify_document(text):

    text = normalize_text(text)

    scores = {}
    matched_keywords = {}
    categories = {}

    # First, look for an explicit IRS form identifier
    explicit_form = find_explicit_tax_form(text)

    # Score every document type in all registries
    for category, registry in DOCUMENT_REGISTRIES.items():

        for document_type, keywords in registry.items():

            score = 0
            matches = []

            for keyword in keywords:

                normalized_keyword = normalize_text(keyword)

                keyword_score = calculate_keyword_score(
                    normalized_keyword,
                    text
                )

                if keyword_score > 0:

                    score += keyword_score
                    matches.append(normalized_keyword)

            # Explicit tax form identifiers receive priority
            if category == "Tax" and document_type == explicit_form:
                score += 30

            scores[document_type] = score
            matched_keywords[document_type] = matches
            categories[document_type] = category

    # Rank document types by their scores
    ranked_documents = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    best_document, best_score = ranked_documents[0]
    second_score = ranked_documents[1][1]

    best_category = categories[best_document]

    score_difference = best_score - second_score

    # Determine whether the evidence is sufficient
    if best_score < 5 or score_difference < 3:

        return {
            "category": "Review",
            "document_type": best_document if best_score > 0 else "Unknown",
            "confidence": "Low",
            "status": "Review",
            "matched_keywords": matched_keywords[best_document],
            "score": best_score
        }

    if best_score >= 12 and score_difference >= 5:
        confidence = "High"

    else:
        confidence = "Medium"

    return {
        "category": best_category,
        "document_type": best_document,
        "confidence": confidence,
        "status": "Classified",
        "matched_keywords": matched_keywords[best_document],
        "score": best_score
    }
