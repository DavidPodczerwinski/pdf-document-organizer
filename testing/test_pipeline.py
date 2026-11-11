import os
import sys

# Make the project root available for imports
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from config import SAMPLE_PDF_FOLDER

from document_reader.pdf_reader import read_pdf
from extraction.information import extract_document_information

from organization.file_naming import generate_filename
from organization.folder_routing import get_destination_folder
from organization.processing_logger import log_document


TEST_CLIENT_FOLDER = os.path.join(
    PROJECT_ROOT,
    "testing",
    "TEST_CLIENT"
)


def run_pipeline_tests():

    print("\nPDF ORGANIZER - SAMPLE TEST RUN")
    print("=" * 55)
    print("Original sample PDFs will not be modified.")

    if not os.path.isdir(SAMPLE_PDF_FOLDER):
        print("ERROR: Sample PDF folder not found.")
        return

    pdf_files = sorted([
        filename
        for filename in os.listdir(SAMPLE_PDF_FOLDER)
        if filename.lower().endswith(".pdf")
    ])

    if not pdf_files:
        print("No sample PDFs found.")
        return

    totals = {
        "processed": 0,
        "classified": 0,
        "review": 0,
        "failed": 0
    }

    for filename in pdf_files:

        source_path = os.path.join(
            SAMPLE_PDF_FOLDER,
            filename
        )

        print("\n" + "-" * 55)
        print(f"FILE: {filename}")

        information = {
            "category": "Review",
            "document_type": "Unknown",
            "confidence": "Low",
            "status": "Review",
            "company": None,
            "institution": None,
            "tax_year": None,
            "month_year": None
        }

        new_filename = filename
        destination = os.path.join(
            TEST_CLIENT_FOLDER,
            "Review"
        )

        try:

            # Read the PDF
            text = read_pdf(source_path)

            if not text.strip():
                raise ValueError(
                    "No readable text was extracted."
                )

            # Extract document information
            information = extract_document_information(text)

            # Generate the proposed filename
            new_filename = generate_filename(
                information,
                filename
            )

            # Determine the proposed folder
            destination = get_destination_folder(
                TEST_CLIENT_FOLDER,
                information
            )

            totals["processed"] += 1

            if information["status"] == "Classified":
                totals["classified"] += 1
            else:
                totals["review"] += 1

            print(f"Document type: {information['document_type']}")
            print(f"Category: {information['category']}")
            print(f"Confidence: {information['confidence']}")
            print(f"Status: {information['status']}")
            print(f"Company: {information['company']}")
            print(f"Institution: {information['institution']}")
            print(f"Tax year: {information['tax_year']}")
            print(f"Month/year: {information['month_year']}")
            print(f"Proposed filename: {new_filename}")
            print(f"Proposed folder: {destination}")

            # Record the result without moving the PDF
            log_document(
                information,
                "TEST_CLIENT",
                filename,
                new_filename,
                destination,
                "Test Only",
                "Sample pipeline test; original file unchanged."
            )

        except Exception as error:

            totals["failed"] += 1

            print(f"ERROR: {error}")

            try:

                log_document(
                    information,
                    "TEST_CLIENT",
                    filename,
                    new_filename,
                    destination,
                    "Failed",
                    str(error)
                )

            except Exception as log_error:
                print(f"Logging error: {log_error}")

    print("\n")
    print("=" * 55)
    print("TEST RUN SUMMARY")
    print("=" * 55)

    print(f"PDFs processed: {totals['processed']}")
    print(f"Classified: {totals['classified']}")
    print(f"Sent to review: {totals['review']}")
    print(f"Failed: {totals['failed']}")

    print("\nOriginal sample PDFs were not moved or changed.")
    print("Detailed results: logs/processing_history.csv")


if __name__ == "__main__":
    run_pipeline_tests()
