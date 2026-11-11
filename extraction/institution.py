import re


KNOWN_INSTITUTIONS = {

    # Major national banks
    "Chase": [
        "jpmorgan chase bank",
        "jpmorgan chase",
        "chase bank",
        "chase"
    ],

    "Bank of America": [
        "bank of america",
        "bofa"
    ],

    "Wells Fargo": [
        "wells fargo"
    ],

    "Citibank": [
        "citibank",
        "citi bank",
        "citi"
    ],

    "Capital One": [
        "capital one"
    ],

    "U.S. Bank": [
        "u.s. bank",
        "us bank",
        "usbank"
    ],

    "PNC": [
        "pnc bank",
        "pnc financial",
        "pnc"
    ],

    "Truist": [
        "truist bank",
        "truist"
    ],

    "TD Bank": [
        "td bank",
        "toronto dominion"
    ],

    # Regional and mid-sized banks
    "Fifth Third Bank": [
        "fifth third bank",
        "fifth third"
    ],

    "Huntington": [
        "huntington national bank",
        "huntington bank",
        "huntington"
    ],

    "Regions Bank": [
        "regions bank",
        "regions financial"
    ],

    "KeyBank": [
        "keybank",
        "key bank"
    ],

    "M&T Bank": [
        "m&t bank",
        "m and t bank"
    ],

    "Citizens Bank": [
        "citizens bank",
        "citizens financial"
    ],

    "BMO": [
        "bmo bank",
        "bmo harris",
        "bmo"
    ],

    "Comerica": [
        "comerica bank",
        "comerica"
    ],

    "First Citizens": [
        "first citizens bank",
        "first citizens"
    ],

    "Santander": [
        "santander bank",
        "santander"
    ],

    "Ally": [
        "ally bank",
        "ally financial"
    ],

    "Frost Bank": [
        "frost bank"
    ],

    "Webster Bank": [
        "webster bank"
    ],

    "KeyBank": [
        "keybank",
        "key bank"
    ],

    "Popular Bank": [
        "popular bank",
        "popular inc"
    ],

    "New York Community Bank": [
        "new york community bank",
        "flagstar bank"
    ],

    # Credit unions
    "Navy Federal": [
        "navy federal credit union",
        "navy federal"
    ],

    "Alliant Credit Union": [
        "alliant credit union",
        "alliant"
    ],

    "PenFed": [
        "pentagon federal credit union",
        "penfed"
    ],

    "State Employees Credit Union": [
        "state employees credit union",
        "secu"
    ],

    "America First Credit Union": [
        "america first credit union"
    ],

    "BECU": [
        "boeing employees credit union",
        "becu"
    ],

    "Golden 1 Credit Union": [
        "golden 1 credit union"
    ],

    "SchoolsFirst Federal Credit Union": [
        "schoolsfirst federal credit union"
    ],

    "Consumers Credit Union": [
        "consumers credit union"
    ],

    # Credit card issuers and financial companies
    "American Express": [
        "american express",
        "amex"
    ],

    "Discover": [
        "discover financial",
        "discover bank",
        "discover"
    ],

    "Barclays": [
        "barclays bank",
        "barclays"
    ],

    "Synchrony": [
        "synchrony bank",
        "synchrony financial",
        "synchrony"
    ],

    "Comenity": [
        "comenity bank",
        "comenity"
    ],

    "Bread Financial": [
        "bread financial"
    ],

    # Investment and brokerage firms
    "Fidelity": [
        "fidelity investments",
        "fidelity brokerage",
        "fidelity"
    ],

    "Charles Schwab": [
        "charles schwab",
        "schwab"
    ],

    "Vanguard": [
        "vanguard group",
        "vanguard"
    ],

    "Morgan Stanley": [
        "morgan stanley"
    ],

    "Merrill": [
        "merrill lynch",
        "merrill"
    ],

    "Edward Jones": [
        "edward jones"
    ],

    "Raymond James": [
        "raymond james"
    ],

    "E*TRADE": [
        "e*trade",
        "etrade"
    ],

    "T. Rowe Price": [
        "t. rowe price",
        "t rowe price"
    ],

    "Interactive Brokers": [
        "interactive brokers"
    ],

    "Principal": [
        "principal financial",
        "principal"
    ],

    "Empower": [
        "empower retirement",
        "empower"
    ],

    # Payroll and financial service providers
    "ADP": [
        "automatic data processing",
        "adp"
    ],

    "Paychex": [
        "paychex"
    ],

    "Gusto": [
        "gusto"
    ],

    "Intuit": [
        "intuit",
        "quickbooks"
    ],

    "PayPal": [
        "paypal"
    ],

    "Square": [
        "square"
    ],

    "Stripe": [
        "stripe"
    ],

    # Insurance providers
    "State Farm": [
        "state farm"
    ],

    "Allstate": [
        "allstate"
    ],

    "GEICO": [
        "geico"
    ],

    "Progressive": [
        "progressive insurance",
        "progressive"
    ],

    "Liberty Mutual": [
        "liberty mutual"
    ],

    "Nationwide": [
        "nationwide insurance",
        "nationwide"
    ],

    "USAA": [
        "usaa"
    ],

    "Travelers": [
        "travelers insurance"
    ],

    "MetLife": [
        "metlife"
    ],

    "Prudential": [
        "prudential financial",
        "prudential"
    ]
}


BANKS_AND_CREDIT_UNIONS = {
    "Chase", "Bank of America", "Wells Fargo", "Citibank",
    "Capital One", "U.S. Bank", "PNC", "Truist", "TD Bank",
    "Fifth Third Bank", "Huntington", "Regions Bank", "KeyBank",
    "M&T Bank", "Citizens Bank", "BMO", "Comerica",
    "First Citizens", "Santander", "Ally", "Frost Bank",
    "Webster Bank", "Popular Bank", "New York Community Bank",
    "Navy Federal", "Alliant Credit Union", "PenFed",
    "State Employees Credit Union", "America First Credit Union",
    "BECU", "Golden 1 Credit Union",
    "SchoolsFirst Federal Credit Union", "Consumers Credit Union",
    "Discover"
}

INVESTMENT_FIRMS = {
    "Fidelity", "Charles Schwab", "Vanguard", "Morgan Stanley",
    "Merrill", "Edward Jones", "Raymond James", "E*TRADE",
    "T. Rowe Price", "Interactive Brokers", "Principal", "Empower"
}

CREDIT_CARD_ISSUERS = {
    "American Express", "Discover", "Barclays", "Synchrony",
    "Comenity", "Bread Financial", "Capital One", "Chase",
    "Citibank", "Bank of America", "Wells Fargo", "U.S. Bank",
    "PNC", "Navy Federal"
}

PAYROLL_PROVIDERS = {
    "ADP", "Paychex", "Gusto"
}

INSURANCE_COMPANIES = {
    "State Farm", "Allstate", "GEICO", "Progressive",
    "Liberty Mutual", "Nationwide", "USAA", "Travelers",
    "MetLife", "Prudential"
}


def find_institution_matches(text, allowed_institutions=None):

    matches = []

    for institution, keywords in KNOWN_INSTITUTIONS.items():

        if (
            allowed_institutions is not None
            and institution not in allowed_institutions
        ):
            continue

        for keyword in keywords:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(keyword)
                + r"(?![a-z0-9])"
            )

            for match in re.finditer(
                pattern,
                text,
                re.IGNORECASE
            ):

                matches.append({
                    "institution": institution,
                    "position": match.start(),
                    "length": len(keyword)
                })

    return matches


def extract_institution(text, document_type=None):

    if not text:
        return None

    # Select institutions that make sense for the document
    if document_type in [
        "Bank Statement",
        "Checking Account Statement",
        "Savings Account Statement"
    ]:
        allowed = BANKS_AND_CREDIT_UNIONS

    elif document_type == "Credit Card Statement":
        allowed = CREDIT_CARD_ISSUERS

    elif document_type in [
        "Investment Statement",
        "Retirement Account Statement"
    ]:
        allowed = INVESTMENT_FIRMS

    elif document_type in [
        "Mortgage Statement",
        "Loan Statement",
        "Line of Credit Statement"
    ]:
        allowed = BANKS_AND_CREDIT_UNIONS

    elif document_type in [
        "Pay Stub",
        "Payroll Summary"
    ]:
        allowed = PAYROLL_PROVIDERS

    elif document_type in [
        "Insurance Policy",
        "Insurance Statement"
    ]:
        allowed = INSURANCE_COMPANIES

    else:
        allowed = None

    # Search the document header first
    header_text = text[:3000]

    header_matches = find_institution_matches(
        header_text,
        allowed
    )

    if header_matches:

        header_matches.sort(
            key=lambda item: (
                item["position"],
                -item["length"]
            )
        )

        return header_matches[0]["institution"]

    # Search the rest of the document if necessary
    remaining_text = text[3000:]

    remaining_matches = find_institution_matches(
        remaining_text,
        allowed
    )

    if remaining_matches:

        remaining_matches.sort(
            key=lambda item: (
                item["position"],
                -item["length"]
            )
        )

        return remaining_matches[0]["institution"]

    return None


def extract_labeled_company(text, labels):

    # Look for company names following recognizable labels
    for label in labels:

        pattern = (
            r"\b"
            + label
            + r"\b\s*[:\-]?\s*"
            r"([A-Z][A-Za-z0-9&.,' -]{2,70})"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            company = match.group(1).strip()

            company = re.split(
                r"\b(?:address|city|state|zip|phone|"
                r"account number|identification number)\b",
                company,
                flags=re.IGNORECASE
            )[0].strip()

            company = company.rstrip(" ,.-")

            if company:
                return company

    return None


def extract_company(text, document_type=None):

    employer_documents = [
        "W-2",
        "W-2C",
        "Pay Stub",
        "Payroll Summary",
        "Employment Agreement"
    ]

    payer_documents = [
        "1099-INT",
        "1099-DIV",
        "1099-NEC",
        "1099-MISC",
        "1099-R",
        "1099-B",
        "1099-G",
        "1099-K"
    ]

    if document_type in employer_documents:

        company = extract_labeled_company(
            text,
            ["employer's name", "employer name", "employer"]
        )

        if company:
            return company

    if document_type in payer_documents:

        company = extract_labeled_company(
            text,
            ["payer's name", "payer name", "payer"]
        )

        if company:
            return company

    company = extract_labeled_company(
        text,
        [
            "vendor name",
            "supplier name",
            "issued by",
            "provided by",
            "company name"
        ]
    )

    if company:
        return company

    return extract_institution(text, document_type)
