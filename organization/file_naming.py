import os
import re


DOCUMENT_NAMES = {

    "Bank Statement": "Bank_Statement",
    "Bank Transaction History": "Bank_Transactions",
    "Bank Deposit Confirmation": "Bank_Deposit",
    "Bank Transfer Confirmation": "Bank_Transfer",
    "Account Confirmation": "Account_Confirmation",

    "Credit Card Statement": "Credit_Card_Statement",
    "Credit Card Transaction History": "Credit_Card_Transactions",

    "Investment Statement": "Investment_Statement",
    "Investment Trade Confirmation": "Investment_Trade",
    "Dividend Statement": "Dividend_Statement",
    "Capital Gains Statement": "Capital_Gains",

    "Retirement Account Statement": "Retirement_Statement",
    "Retirement Distribution Statement": "Retirement_Distribution",
    "Retirement Contribution Statement": "Retirement_Contribution",

    "Mortgage Statement": "Mortgage_Statement",
    "Auto Loan Statement": "Auto_Loan_Statement",
    "Personal Loan Statement": "Personal_Loan_Statement",
    "Business Loan Statement": "Business_Loan_Statement",
    "Line of Credit Statement": "Line_of_Credit",
    "Student Loan Statement": "Student_Loan_Statement",
    "Loan Payment Confirmation": "Loan_Payment",
    "Loan Payoff Statement": "Loan_Payoff",

    "Balance Sheet": "Balance_Sheet",
    "Income Statement": "Income_Statement",
    "Cash Flow Statement": "Cash_Flow_Statement",
    "Financial Statement": "Financial_Statement",
    "General Ledger": "General_Ledger",
    "Trial Balance": "Trial_Balance",
    "Accounts Receivable Aging": "AR_Aging",
    "Accounts Payable Aging": "AP_Aging",
    "Bank Reconciliation": "Bank_Reconciliation",

    "Payment Processor Statement": "Payment_Processor",
    "Merchant Account Statement": "Merchant_Account",
    "Digital Payment Statement": "Digital_Payment",
    "Financial Account Summary": "Financial_Account_Summary",

    "Sales Invoice": "Sales_Invoice",
    "Vendor Invoice": "Vendor_Invoice",
    "Invoice": "Invoice",
    "Receipt": "Receipt",
    "Credit Memo": "Credit_Memo",
    "Debit Memo": "Debit_Memo",
    "Customer Statement": "Customer_Statement",
    "Vendor Statement": "Vendor_Statement",
    "Bill": "Bill",
    "Purchase Order": "Purchase_Order",
    "Sales Order": "Sales_Order",
    "Shipping Document": "Shipping_Document",

    "Pay Stub": "Pay_Stub",
    "Payroll Summary": "Payroll_Summary",
    "Payroll Tax Document": "Payroll_Tax",
    "Employee Benefits Statement": "Employee_Benefits",
    "Employee Reimbursement": "Employee_Reimbursement",
    "Employment Agreement": "Employment_Agreement",
    "Independent Contractor Agreement": "Contractor_Agreement",

    "Expense Report": "Expense_Report",
    "Travel Expense Report": "Travel_Expense_Report",
    "Mileage Log": "Mileage_Log",
    "Business Expense Summary": "Business_Expense_Summary",
    "Petty Cash Report": "Petty_Cash",

    "Insurance Policy": "Insurance_Policy",
    "Insurance Premium Statement": "Insurance_Premium",
    "Insurance Claim": "Insurance_Claim",
    "Insurance Certificate": "Insurance_Certificate",

    "Lease Agreement": "Lease_Agreement",
    "Rent Statement": "Rent_Statement",
    "Property Tax Statement": "Property_Tax",
    "Property Deed": "Property_Deed",
    "Property Closing Statement": "Property_Closing",
    "Fixed Asset Record": "Fixed_Asset_Record",

    "Articles of Incorporation": "Articles_of_Incorporation",
    "Operating Agreement": "Operating_Agreement",
    "Partnership Agreement": "Partnership_Agreement",
    "Corporate Resolution": "Corporate_Resolution",
    "Certificate of Good Standing": "Certificate_of_Good_Standing",
    "Business Contract": "Business_Contract",
    "Loan Agreement": "Loan_Agreement",
    "Non-Disclosure Agreement": "NDA",

    "Accounts Receivable Report": "AR_Report",
    "Accounts Payable Report": "AP_Report",
    "Inventory Report": "Inventory_Report",
    "Sales Report": "Sales_Report",
    "Purchase Report": "Purchase_Report",
    "Budget Report": "Budget_Report",
    "Management Report": "Management_Report",
    "Audit Report": "Audit_Report",
    "Tax Workpaper": "Tax_Workpaper",
    "Business Correspondence": "Business_Correspondence"
}


def generate_filename(information, original_filename):

    import os
    import re

    document_type = information["document_type"]
    category = information["category"]

    tax_year = information.get("tax_year")
    month_year = information.get("month_year")

    institution = information.get("institution")
    company = information.get("company")

    extension = os.path.splitext(original_filename)[1]

    # Clean individual filename components
    def clean_part(value):

        if not value:
            return None

        value = str(value)

        # Remove invalid Windows filename characters
        value = re.sub(r'[<>:"/\\|?*]', "", value)

        # Remove long account or identification numbers
        value = re.sub(r"\b\d{5,}\b", "", value)

        value = re.sub(r"\s+", "_", value.strip())

        return value.strip("_")

    # Tax forms: FormType_TaxYear
    if category == "Tax":

        form_type = clean_part(
            document_type.replace(" ", "_")
        )

        if tax_year:
            filename = f"{form_type}_{tax_year}"
        else:
            filename = f"{form_type}_TaxYear_Unknown"

    # Credit cards: CC_Institution_MM-YYYY
    elif document_type == "Credit Card Statement":

        institution_name = clean_part(
            institution or company
        )

        filename = "CC"

        if institution_name:
            filename += f"_{institution_name}"

        if month_year:
            filename += f"_{month_year}"

    # Other documents retain the existing naming structure
    else:

        document_name = DOCUMENT_NAMES.get(
            document_type,
            document_type.replace(" ", "_")
        )

        if category == "Financial":
            organization = institution or company
        else:
            organization = company or institution

        filename_parts = [document_name]

        if tax_year and category == "Tax":
            filename_parts.append(str(tax_year))

        elif month_year:
            filename_parts.append(str(month_year))

        if organization:
            filename_parts.append(organization)

        filename = "_".join(
            clean_part(part)
            for part in filename_parts
            if clean_part(part)
        )

    return filename + extension

