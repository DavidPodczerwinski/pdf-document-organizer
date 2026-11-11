import os
import sys

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TESTING_FOLDER = os.path.join(
    BASE_DIR,
    "testing"
)

SAMPLE_PDF_FOLDER = os.path.join(
    TESTING_FOLDER,
    "sample_pdfs"
)

CLIENTS_FOLDER = os.path.join(
    BASE_DIR,
    "Clients"
)

if getattr(sys, "frozen", False):
    TESSERACT_PATH = os.path.join(
        BASE_DIR,
        "Tesseract-OCR",
        "tesseract.exe"
    )
else:
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

OCR_LANGUAGE = "eng"

OCR_CONFIG = "--psm 6"

PDF_SCALE = 4

TEST_MODE = True

MINIMUM_CONFIDENCE = 80
