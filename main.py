import os

from document_reader.pdf_reader import read_pdf
from extraction.information import extract_document_information

from organization.file_naming import generate_filename
from organization.folder_routing import get_destination_folder


def get_preview_destination(destination_folder, filename, reserved_destinations):

    # Start with the proposed filename
    name, extension = os.path.splitext(filename)

    destination_path = os.path.join(
        destination_folder,
        filename
    )

    counter = 2

    # Check both existing files and filenames already reserved
    while (
        os.path.exists(destination_path)
        or os.path.normcase(os.path.abspath(destination_path))
        in reserved_destinations
    ):

        new_filename = f"{name}_{counter}{extension}"

        destination_path = os.path.join(
            destination_folder,
            new_filename
        )

        counter += 1

    # Reserve this destination for the remaining preview documents
    reserved_destinations.add(
        os.path.normcase(os.path.abspath(destination_path))
    )

    return destination_path


def preview_client_folder(client_folder):

    # Verify that the selected client folder exists
    if not os.path.isdir(client_folder):
        raise ValueError("The selected client folder does not exist.")

    results = []

    # Track destinations already assigned during this preview
    reserved_destinations = set()

    # Only process PDFs directly inside the selected folder
    pdf_files = sorted([
        filename
        for filename in os.listdir(client_folder)
        if filename.lower().endswith(".pdf")
        and os.path.isfile(
            os.path.join(client_folder, filename)
        )
    ])

    # Process each PDF individually
    for filename in pdf_files:

        source_path = os.path.join(
            client_folder,
            filename
        )

        try:

            # Read the PDF
            text = read_pdf(source_path)

            if not text.strip():
                raise ValueError(
                    "No readable text could be extracted."
                )

            # Identify the document and extract information
            information = extract_document_information(text)

            # Generate the proposed filename
            new_filename = generate_filename(
                information,
                filename
            )

            # Determine the proposed destination folder
            destination_folder = get_destination_folder(
                client_folder,
                information
            )

            # Find a unique destination, including other preview documents
            destination_path = get_preview_destination(
                destination_folder,
                new_filename,
                reserved_destinations
            )

            results.append({

                "original_filename": filename,

                "source_path": source_path,

                "document_type": information["document_type"],

                "category": information["category"],

                "confidence": information["confidence"],

                "status": information["status"],

                "company": information.get("company"),

                "institution": information.get("institution"),

                "tax_year": information.get("tax_year"),

                "month_year": information.get("month_year"),

                "new_filename": os.path.basename(
                    destination_path
                ),

                "destination_folder": destination_folder,

                "destination_path": destination_path,

                "error": None

            })

        except Exception as error:

            # Keep failed documents in the preview for inspection
            results.append({

                "original_filename": filename,

                "source_path": source_path,

                "document_type": "Unknown",

                "category": "Review",

                "confidence": "Low",

                "status": "Failed",

                "company": None,

                "institution": None,

                "tax_year": None,

                "month_year": None,

                "new_filename": filename,

                "destination_folder": os.path.join(
                    client_folder,
                    "Review"
                ),

                "destination_path": None,

                "error": str(error)

            })

    return results


def get_preview_summary(results):

    summary = {
        "total": len(results),
        "classified": 0,
        "review": 0,
        "failed": 0
    }

    for result in results:

        if result["status"] == "Failed":
            summary["failed"] += 1

        elif result["status"] == "Review":
            summary["review"] += 1

        else:
            summary["classified"] += 1

    return summary

