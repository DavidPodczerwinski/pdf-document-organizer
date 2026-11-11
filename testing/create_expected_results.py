import csv
from pathlib import Path


# Locate the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Locate the sample PDFs and expected results file
PDF_FOLDER = BASE_DIR / "testing" / "sample_pdfs"
CSV_FILE = BASE_DIR / "testing" / "expected_results.csv"


def create_expected_results():

    # Find all PDFs directly inside the sample folder
    pdf_files = sorted([
        file.name
        for file in PDF_FOLDER.iterdir()
        if file.is_file()
        and file.suffix.lower() == ".pdf"
    ])

    if not pdf_files:
        print("No PDF files were found.")
        return

    # Preserve classifications from an existing CSV
    existing_results = {}

    if CSV_FILE.exists():

        with open(
            CSV_FILE,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                existing_results[row["filename"]] = (
                    row["expected_document_type"]
                )

    # Write the updated CSV
    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "filename",
                "expected_document_type"
            ]
        )

        writer.writeheader()

        for filename in pdf_files:

            writer.writerow({

                "filename": filename,

                "expected_document_type": (
                    existing_results.get(filename, "")
                )

            })

    print(f"Found {len(pdf_files)} PDF documents.")

    print(f"Expected results file created: {CSV_FILE}")


if __name__ == "__main__":
    create_expected_results()
