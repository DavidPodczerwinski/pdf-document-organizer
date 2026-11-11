import pymupdf
import pytesseract

from PIL import Image
from config import TESSERACT_PATH, OCR_LANGUAGE, OCR_CONFIG, PDF_SCALE

# Connect Python to the local Tesseract installation
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def calculate_text_quality(text):

    if not text:
        return 0

    # Count useful characters and words
    useful_characters = sum(
        character.isalnum()
        for character in text
    )

    words = len(text.split())

    # Penalize text containing unusual replacement characters
    unusual_characters = text.count("\ufffd")

    quality_score = (
        useful_characters
        + (words * 2)
        - (unusual_characters * 10)
    )

    return max(quality_score, 0)


def calculate_image_coverage(page):

    page_area = page.rect.get_area()

    if page_area == 0:
        return 0

    image_area = 0

    # Identify images present on the page
    for image in page.get_images(full=True):

        image_xref = image[0]

        try:
            image_rectangles = page.get_image_rects(image_xref)

            for rectangle in image_rectangles:
                image_area += rectangle.get_area()

        except Exception:
            continue

    coverage = image_area / page_area

    return min(coverage, 1.0)


def perform_ocr(page):

    matrix = pymupdf.Matrix(
        PDF_SCALE,
        PDF_SCALE
    )

    pixmap = page.get_pixmap(
        matrix=matrix,
        colorspace=pymupdf.csRGB,
        alpha=False
    )

    image = Image.frombytes(
        "RGB",
        [pixmap.width, pixmap.height],
        pixmap.samples
    )

    ocr_text = pytesseract.image_to_string(
        image,
        lang=OCR_LANGUAGE,
        config=OCR_CONFIG
    )

    return ocr_text.strip()


def read_pdf(pdf_path):

    document_text = ""

    with pymupdf.open(pdf_path) as pdf:

        for page_number, page in enumerate(pdf, start=1):

            # First attempt to extract existing PDF text
            native_text = page.get_text("text").strip()

            # Determine whether OCR may be necessary
            image_coverage = calculate_image_coverage(page)

            needs_ocr = (
                len(native_text) < 120
                or image_coverage >= 0.25
            )

            page_text = native_text

            if needs_ocr:

                try:

                    ocr_text = perform_ocr(page)

                    # Keep whichever version contains better text
                    native_quality = calculate_text_quality(
                        native_text
                    )

                    ocr_quality = calculate_text_quality(
                        ocr_text
                    )

                    if ocr_quality > native_quality:
                        page_text = ocr_text

                except Exception as error:

                    print(
                        f"OCR warning on page {page_number}: {error}"
                    )

            # Preserve page boundaries
            document_text += (
                f"\n\n--- PAGE {page_number} ---\n\n"
            )

            document_text += page_text

    return document_text
