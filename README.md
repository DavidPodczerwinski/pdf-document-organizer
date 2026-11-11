# PDF Document Organizer

### Project Overview

The PDF Document Organizer is a Windows desktop application designed to help accounting professionals organize client documents more efficiently.

Accounting firms regularly receive large numbers of PDF documents, including bank statements, credit card statements, tax forms, investment statements, invoices, payroll records, and other financial documents. Manually reviewing, renaming, and organizing these files can be time-consuming.

This application automates much of that process by extracting text from PDFs, identifying document types, generating standardized filenames, and routing documents into appropriate folders.

The application also includes a manual review process so users can correct classifications before documents are processed.

### Key Features

PDF Text Extraction: Extracts text from PDFs using PyMuPDF and uses Tesseract OCR when documents are scanned or contain insufficient readable text.

Automatic Document Classification: Identifies tax, financial, and business documents using a rule-based classification system.

Information Extraction: Identifies relevant information such as document dates, tax years, financial institutions, and company names.

Standardized File Naming: Generates consistent filenames based on document type and available information.

Automatic Folder Organization: Routes documents into appropriate client subfolders.

Manual Review and Correction: Allows users to review uncertain classifications and manually correct document types or destinations.

Preview Before Processing: Displays proposed filenames and destinations before any documents are moved.

Processing History: Maintains a CSV log of processing activity, including document classifications and processing results.

Duplicate File Protection: Avoids overwriting existing files by generating unique filenames when necessary.

### How the Application Works

The application follows this workflow:

Select a Client Folder: The user selects the folder containing the client's PDFs.

Extract Document Text: The program extracts existing PDF text and uses OCR when necessary.

Identify Document Types: The classification system evaluates document content and assigns a document type and confidence level.

Extract Relevant Information: The program identifies dates, tax years, and financial institutions when available.

Generate Filenames: Documents receive standardized filenames based on their classification and extracted information.

Determine Destinations: Documents are assigned to appropriate subfolders within the selected client folder.

Review and Correct: The user can inspect the proposed results and manually correct classifications or destinations.

Approve Processing: The user approves the batch before documents are moved.

Record Results: Processing activity is saved in a CSV history log.

How the Application Works

The application follows this workflow:

Select a Client Folder: The user selects the folder containing the client's PDFs.

Extract Document Text: The program extracts existing PDF text and uses OCR when necessary.

Identify Document Types: The classification system evaluates document content and assigns a document type and confidence level.

Extract Relevant Information: The program identifies dates, tax years, and financial institutions when available.

Generate Filenames: Documents receive standardized filenames based on their classification and extracted information.

Determine Destinations: Documents are assigned to appropriate subfolders within the selected client folder.

Review and Correct: The user can inspect the proposed results and manually correct classifications or destinations.

Approve Processing: The user approves the batch before documents are moved.

Record Results: Processing activity is saved in a CSV history log.

### Folder Organization

The application creates subfolders within the selected client's existing folder as needed.

Examples include:

Banking

Credit Cards

Investments & Retirement

Loans

Financial Statements

Payroll

Insurance

Business Documents

Property & Legal

Tax Documents

Review

Documents that cannot be classified confidently are routed to the Review folder instead of being automatically assigned to an uncertain category.

How the Application Works

The application follows this workflow:

Select a Client Folder: The user selects the folder containing the client's PDFs.

Extract Document Text: The program extracts existing PDF text and uses OCR when necessary.

Identify Document Types: The classification system evaluates document content and assigns a document type and confidence level.

Extract Relevant Information: The program identifies dates, tax years, and financial institutions when available.

Generate Filenames: Documents receive standardized filenames based on their classification and extracted information.

Determine Destinations: Documents are assigned to appropriate subfolders within the selected client folder.

Review and Correct: The user can inspect the proposed results and manually correct classifications or destinations.

Approve Processing: The user approves the batch before documents are moved.

Record Results: Processing activity is saved in a CSV history log.

Folder Organization

The application creates subfolders within the selected client's existing folder as needed.

Examples include:

Banking

Credit Cards

Investments & Retirement

Loans

Financial Statements

Payroll

Insurance

Business Documents

Property & Legal

Tax Documents

Review

Documents that cannot be classified confidently are routed to the Review folder instead of being automatically assigned to an uncertain category.

File Naming Examples

The application generates standardized filenames based on document type.

Examples:

Document

Example Filename

Credit card statement

CC_Chase_01-2025.pdf

Bank statement

Bank_Statement_01-2025_Chase.pdf

W-2

W-2_2025.pdf

1099-INT

1099-INT_2025.pdf

Partnership Schedule K-1

1065_Schedule_K-1_2025.pdf

Mortgage statement

Mortgage_Statement_01-2025.pdf

Tax document filenames do not include company or financial institution names. If a tax year cannot be identified, the application uses a TaxYear_Unknown designation.

Safety and Error Prevention

Protecting original client documents is an important part of the application's design.

The application includes several safeguards:

Test mode allows users to simulate processing without moving original documents.

Documents with uncertain classifications are routed for manual review.

Users can inspect proposed filenames and destinations before approving processing.

Existing files are not intentionally overwritten.

Processing errors are recorded in the history log.

The application processes PDFs directly inside the selected client folder rather than recursively processing its output subfolders.

Test mode is currently enabled for demonstration and testing purposes.

### Project Structure

pdf-document-organizer/
│
├── app.py
├── main.py
├── config.py
├── requirements.txt
├── README.md
│
├── classification/
│   ├── document_identifier.py
│   ├── tax_documents.py
│   ├── financial_documents.py
│   └── business_documents.py
│
├── document_reader/
│   └── pdf_reader.py
│
├── extraction/
│   ├── dates.py
│   ├── institution.py
│   └── information.py
│
├── organization/
│   ├── file_naming.py
│   ├── folder_routing.py
│   ├── file_mover.py
│   └── processing_logger.py
│
├── testing/
│   ├── sample_pdfs/
│   ├── create_expected_results.py
│   ├── test_pipeline.py
│   ├── expected_results.csv
│   └── test_results.csv
│
├── logs/
├── Clients/
│
└── dist/
    └── PDFOrganizer/
        ├── PDFOrganizer.exe
        ├── _internal/
        └── Tesseract-OCR/

### Running the Application from Source

The project uses Python 3.12 and a virtual environment.

Install the dependencies listed in requirements.txt:

python -m pip install -r requirements.txt

Tesseract OCR must also be installed if running the application directly from source. The current configuration expects it at:

C:\Program Files\Tesseract-OCR\tesseract.exe

Launch the application from the project directory:

python app.py

### Running the Windows Application

A packaged Windows version is available in:

dist\PDFOrganizer\

Launch:

PDFOrganizer.exe

The complete distribution folder must remain together, including the _internal and Tesseract-OCR folders.

The packaged application includes the Tesseract OCR engine and English language data, so a separate Tesseract installation is not required.

### Testing

The application was tested using a collection of sample PDF documents representing different accounting, financial, and tax document types.

Testing included:

PDF text extraction and OCR.

Document classification.

Information and date extraction.

Standardized filename generation.

Folder routing.

Manual classification corrections.

Destination changes.

Test-mode processing.

Processing history generation.

Verification that original sample PDFs remained unchanged during testing.

The sample classification testing achieved approximately 90% accuracy. The manual review process provides an additional safeguard for documents that are uncertain or incorrectly classified.

### Future Improvements

Potential future improvements include:

Expanding the document classification registry based on real-world accounting firm documents.

Improving recognition of financial institutions and document dates.

Refining OCR for complex or low-quality scanned documents.

Incorporating feedback from a controlled accounting firm pilot.

Improving the application's installation and distribution process.

### Project Purpose

The goal of this project is to reduce repetitive administrative work in an accounting environment by automating document identification, naming, and organization.

By combining rule-based classification, OCR, and a manual review workflow, the application aims to improve efficiency while maintaining user oversight and protecting original client documents.