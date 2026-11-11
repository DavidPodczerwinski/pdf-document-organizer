import os


FOLDER_MAPPING = {

    # Banking
    "Bank Statement": "Banking",
    "Bank Transaction History": "Banking",
    "Bank Deposit Confirmation": "Banking",
    "Bank Transfer Confirmation": "Banking",
    "Account Confirmation": "Banking",
    "Bank Reconciliation": "Banking",

    # Credit cards
    "Credit Card Statement": "Credit Cards",
    "Credit Card Transaction History": "Credit Cards",

    # Investments and retirement
    "Investment Statement": "Investments & Retirement",
    "Investment Trade Confirmation": "Investments & Retirement",
    "Dividend Statement": "Investments & Retirement",
    "Capital Gains Statement": "Investments & Retirement",
    "Retirement Account Statement": "Investments & Retirement",
    "Retirement Distribution Statement": "Investments & Retirement",
    "Retirement Contribution Statement": "Investments & Retirement",

    # Loans
    "Mortgage Statement": "Loans",
    "Auto Loan Statement": "Loans",
    "Personal Loan Statement": "Loans",
    "Business Loan Statement": "Loans",
    "Line of Credit Statement": "Loans",
    "Student Loan Statement": "Loans",
    "Loan Payment Confirmation": "Loans",
    "Loan Payoff Statement": "Loans",
    "Loan Agreement": "Loans",

    # Financial reports
    "Balance Sheet": "Financial Statements",
    "Income Statement": "Financial Statements",
    "Cash Flow Statement": "Financial Statements",
    "Financial Statement": "Financial Statements",
    "General Ledger": "Financial Statements",
    "Trial Balance": "Financial Statements",
    "Accounts Receivable Aging": "Financial Statements",
    "Accounts Payable Aging": "Financial Statements",
    "Accounts Receivable Report": "Financial Statements",
    "Accounts Payable Report": "Financial Statements",
    "Financial Account Summary": "Financial Statements",
    "Management Report": "Financial Statements",
    "Budget Report": "Financial Statements",
    "Audit Report": "Financial Statements",

    # Payment services
    "Payment Processor Statement": "Banking",
    "Merchant Account Statement": "Banking",
    "Digital Payment Statement": "Banking",

    # Payroll
    "Pay Stub": "Payroll",
    "Payroll Summary": "Payroll",
    "Payroll Tax Document": "Payroll",
    "Employee Benefits Statement": "Payroll",
    "Employee Reimbursement": "Payroll",
    "Employment Agreement": "Payroll",

    # Insurance
    "Insurance Policy": "Insurance",
    "Insurance Premium Statement": "Insurance",
    "Insurance Claim": "Insurance",
    "Insurance Certificate": "Insurance",

    # Business transactions and expenses
    "Sales Invoice": "Business Documents",
    "Vendor Invoice": "Business Documents",
    "Invoice": "Business Documents",
    "Receipt": "Business Documents",
    "Credit Memo": "Business Documents",
    "Debit Memo": "Business Documents",
    "Customer Statement": "Business Documents",
    "Vendor Statement": "Business Documents",
    "Bill": "Business Documents",
    "Purchase Order": "Business Documents",
    "Sales Order": "Business Documents",
    "Shipping Document": "Business Documents",
    "Expense Report": "Business Documents",
    "Travel Expense Report": "Business Documents",
    "Mileage Log": "Business Documents",
    "Business Expense Summary": "Business Documents",
    "Petty Cash Report": "Business Documents",
    "Independent Contractor Agreement": "Business Documents",
    "Business Contract": "Business Documents",
    "Non-Disclosure Agreement": "Business Documents",
    "Business Correspondence": "Business Documents",

    # Property and legal
    "Lease Agreement": "Property & Legal",
    "Rent Statement": "Property & Legal",
    "Property Tax Statement": "Property & Legal",
    "Property Deed": "Property & Legal",
    "Property Closing Statement": "Property & Legal",
    "Fixed Asset Record": "Property & Legal",
    "Articles of Incorporation": "Property & Legal",
    "Operating Agreement": "Property & Legal",
    "Partnership Agreement": "Property & Legal",
    "Corporate Resolution": "Property & Legal",
    "Certificate of Good Standing": "Property & Legal",

    # Other accounting records
    "Inventory Report": "Business Documents",
    "Sales Report": "Business Documents",
    "Purchase Report": "Business Documents",
    "Tax Workpaper": "Tax Documents"
}


def get_destination_folder(client_folder, information):

    # Never automatically route uncertain classifications
    if information.get("status") != "Classified":
        folder_name = "Review"

    else:

        category = information.get("category")
        document_type = information.get("document_type")

        if category == "Tax":
            folder_name = "Tax Documents"

        else:
            folder_name = FOLDER_MAPPING.get(
                document_type,
                "Review"
            )

    return os.path.join(
        client_folder,
        folder_name
    )

