from classification.document_identifier import identify_document
from extraction.dates import extract_dates
from extraction.institution import extract_company, extract_institution


def extract_document_information(text):

    # Identify the document
    classification = identify_document(text)

    document_type = classification["document_type"]
    category = classification["category"]

    # Extract dates using the document type
    dates = extract_dates(
        text,
        document_type
    )

    # Tax documents do not need company or institution names
    if category == "Tax":
        company = None
        institution = None

    else:
        company = extract_company(
            text,
            document_type
        )

        institution = extract_institution(text, document_type)

    information = {
        "category": category,
        "document_type": document_type,
        "confidence": classification["confidence"],
        "status": classification["status"],
        "matched_keywords": classification["matched_keywords"],
        "score": classification["score"],
        "company": company,
        "institution": institution,
        "month_year": dates["month_year"],
        "tax_year": dates["tax_year"],
        "statement_period_start": dates["statement_period_start"],
        "statement_period_end": dates["statement_period_end"]
    }

    return information
