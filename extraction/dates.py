import re
import calendar
from datetime import datetime


MONTHS = {
    month.lower(): number
    for number, month in enumerate(calendar.month_name)
    if month
}

MONTHS.update({
    month.lower(): number
    for number, month in enumerate(calendar.month_abbr)
    if month
})


# Recognize written and numeric date formats
DATE_PATTERN = (
    r"\b(?:"
    r"(?:January|February|March|April|May|June|July|August|"
    r"September|October|November|December|"
    r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)"
    r"\s+\d{1,2},?\s+20\d{2}"
    r"|"
    r"\d{1,2}[/-]\d{1,2}[/-](?:20\d{2}|\d{2})"
    r"|"
    r"\d{1,2}[/-](?:20\d{2}|\d{2})"
    r")\b"
)


def parse_date(date_text):

    date_text = date_text.strip()

    # Try written month dates
    for date_format in [
        "%B %d, %Y",
        "%B %d %Y",
        "%b %d, %Y",
        "%b %d %Y"
    ]:

        try:
            return datetime.strptime(
                date_text,
                date_format
            )

        except ValueError:
            continue

    # Try numeric dates with four-digit and two-digit years
    for date_format in [
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%m/%d/%y",
        "%m-%d-%y",
        "%m/%Y",
        "%m-%Y",
        "%m/%y",
        "%m-%y"
    ]:

        try:
            return datetime.strptime(
                date_text,
                date_format
            )

        except ValueError:
            continue

    return None


def find_dates(text):

    dates = []

    for match in re.finditer(
        DATE_PATTERN,
        text,
        re.IGNORECASE
    ):

        parsed_date = parse_date(match.group())

        if parsed_date:
            dates.append({
                "text": match.group(),
                "date": parsed_date,
                "position": match.start()
            })

    return dates


def extract_tax_year(text):

    patterns = [
        r"tax year\s*[:\-]?\s*(20\d{2})",
        r"taxable year\s*[:\-]?\s*(20\d{2})",
        r"for the (?:calendar )?year\s+(20\d{2})",
        r"calendar year\s*[:\-]?\s*(20\d{2})",
        r"year ended\s+[a-z]+\s+\d{1,2},?\s+(20\d{2})"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return None


def extract_statement_period(text):

    period_patterns = [
        r"statement period\s*[:\-]?\s*(.{0,100})",
        r"billing period\s*[:\-]?\s*(.{0,100})",
        r"period covered\s*[:\-]?\s*(.{0,100})",
        r"statement cycle\s*[:\-]?\s*(.{0,100})"
    ]

    for pattern in period_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            dates = find_dates(match.group(1))

            if dates:

                return {
                    "start": dates[0]["date"],
                    "end": dates[-1]["date"]
                }

    return None


def extract_month_year(text, document_type=None):

    # First prioritize statement and billing periods
    period = extract_statement_period(text)

    if period:

        return period["end"].strftime("%m-%Y")

    # Look for explicitly labeled statement dates
    priority_patterns = [
        r"statement date\s*[:\-]?\s*",
        r"closing date\s*[:\-]?\s*",
        r"statement closing date\s*[:\-]?\s*",
        r"period ending\s*[:\-]?\s*",
        r"as of\s*"
    ]

    for pattern in priority_patterns:

        match = re.search(
            pattern + DATE_PATTERN,
            text,
            re.IGNORECASE
        )

        if match:

            dates = find_dates(match.group())

            if dates:
                return dates[0]["date"].strftime("%m-%Y")

    # Use a labeled invoice date for invoices
    if document_type in [
        "Invoice",
        "Vendor Invoice",
        "Sales Invoice",
        "Receipt",
        "Bill"
    ]:

        match = re.search(
            r"(?:invoice date|receipt date|transaction date|"
            r"date issued)\s*[:\-]?\s*" + DATE_PATTERN,
            text,
            re.IGNORECASE
        )

        if match:

            dates = find_dates(match.group())

            if dates:
                return dates[0]["date"].strftime("%m-%Y")

    return None


def extract_dates(text, document_type=None):

    tax_year = extract_tax_year(text)

    month_year = extract_month_year(
        text,
        document_type
    )

    period = extract_statement_period(text)

    statement_period_start = None
    statement_period_end = None

    if period:

        statement_period_start = (
            period["start"].strftime("%m-%d-%Y")
        )

        statement_period_end = (
            period["end"].strftime("%m-%d-%Y")
        )

    return {
        "month_year": month_year,
        "tax_year": tax_year,
        "statement_period_start": statement_period_start,
        "statement_period_end": statement_period_end
    }
