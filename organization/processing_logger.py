import csv
import os
from datetime import datetime

from config import BASE_DIR


LOG_FOLDER = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(
    LOG_FOLDER,
    "processing_history.csv"
)


LOG_HEADERS = [
    "timestamp",
    "client",
    "original_filename",
    "document_type",
    "category",
    "confidence",
    "status",
    "company",
    "institution",
    "tax_year",
    "month_year",
    "new_filename",
    "destination",
    "result",
    "message"
]


def log_document(information, client, original_filename,
                 new_filename, destination, result, message=""):

    # Create the log folder if it doesn't exist
    os.makedirs(LOG_FOLDER, exist_ok=True)

    file_exists = os.path.isfile(LOG_FILE)

    with open(
        LOG_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=LOG_HEADERS
        )

        # Write column headings for a new log
        if not file_exists:
            writer.writeheader()

        writer.writerow({

            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),

            "client": client,

            "original_filename": original_filename,

            "document_type": information.get(
                "document_type", "Unknown"
            ),

            "category": information.get(
                "category", "Review"
            ),

            "confidence": information.get(
                "confidence", "Low"
            ),

            "status": information.get(
                "status", "Review"
            ),

            "company": information.get("company"),

            "institution": information.get("institution"),

            "tax_year": information.get("tax_year"),

            "month_year": information.get("month_year"),

            "new_filename": new_filename,

            "destination": destination,

            "result": result,

            "message": message
        })
